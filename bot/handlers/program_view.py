import asyncio
import logging
from aiogram import Router, F, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from sqlalchemy.orm import selectinload

from bot.models.program import Program
from bot.models.lead import Lead
from bot.ui.main_menu import get_main_menu_keyboard
from bot.services.program_runner import run_program_job # Import the job worker
from bot.handlers.auth import start_auth_flow
from bot.ui.lead_card import format_lead_card, get_lead_card_keyboard

logger = logging.getLogger(__name__)
router = Router()

# --- Keyboards ---

def get_program_card_keyboard(program_id: int, leads_count: int = 0) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    if leads_count > 0:
        builder.button(text=f"👀 Посмотреть лидов ({leads_count})", callback_data=f"view_program_leads_{program_id}")
    builder.button(text="▶️ Запустить сейчас", callback_data=f"run_program_{program_id}")
    builder.button(text="✏️ Изменить", callback_data=f"edit_program_{program_id}")
    builder.button(text="🗑 Удалить", callback_data=f"delete_program_{program_id}")
    builder.button(text="◀️ К программам", callback_data="my_programs")
    builder.adjust(1)
    return builder.as_markup()

def get_delete_confirmation_keyboard(program_id: int) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="🗑 Да, удалить", callback_data=f"confirm_delete_{program_id}")
    builder.button(text="◀️ Нет, вернуться", callback_data=f"show_program_{program_id}")
    builder.adjust(1)
    return builder.as_markup()

# --- View / Main Card Handler ---

@router.callback_query(F.data.startswith("show_program_"))
async def show_program_handler(callback: CallbackQuery, session: AsyncSession):
    logging.info(f"Handling 'show_program' callback: {callback.data}")
    program_id = int(callback.data.split("_")[-1])

    program_query = select(Program).options(selectinload(Program.chats)).where(Program.id == program_id)
    program = (await session.execute(program_query)).scalars().first()

    if not program:
        await callback.message.edit_text("Программа не найдена.", reply_markup=get_main_menu_keyboard())
        await callback.answer("Программа не найдена.", show_alert=True)
        return

    leads_count_query = select(func.count(Lead.id)).where(Lead.program_id == program.id)
    leads_count = (await session.execute(leads_count_query)).scalar_one()
    logging.info(f"Querying lead count for program_id={program.id}. Found: {leads_count} leads.")

    chats_list_str = "\n".join([f"• @{chat.chat_username}" for chat in program.chats]) if program.chats else "Нет чатов."
    text = (
        f"📁 **{program.name}**\n\n"
        f"**Ниша**: {program.niche_description}\n\n"
        f"**Чаты**:\n{chats_list_str}\n\n"
        f"**Настройки**:\n"
        f"• Минимальный скор: {program.min_score}\n"
        f"• Лидов за запуск: макс {program.max_leads_per_run}\n"
        f"• Web-обогащение: {'вкл' if program.enrich else 'выкл'}\n"
        f"• Расписание: ежедневно в {program.schedule_time} ✅\n\n"
        f"**Статистика**:\n"
        f"• Всего найдено: {leads_count} лидов\n"
    )

    await callback.message.edit_text(text, reply_markup=get_program_card_keyboard(program.id, leads_count))
    await callback.answer()

# --- 'Run Now' Handler (Non-blocking) ---

@router.callback_query(F.data.startswith("run_program_"))
async def run_program_handler(callback: CallbackQuery, bot: Bot):
    program_id = int(callback.data.split("_")[-1])
    logging.info(f"Starting immediate job for program_id={program_id}")

    # Run the job as an asyncio task instead of scheduling it
    # This avoids pickling issues with the bot object
    asyncio.create_task(run_program_job(bot, program_id, callback.from_user.id))

    await callback.answer(
        "✅ Программа запущена в фоновом режиме.\n"
        "Результаты будут приходить в чат по мере их нахождения.",
        show_alert=True
    )

# --- Lead Card Action Handlers ---

@router.callback_query(F.data.startswith("show_message_"))
async def show_outreach_message_handler(callback: CallbackQuery, session: AsyncSession):
    lead_id = int(callback.data.split("_")[-1])
    query = select(Lead).where(Lead.id == lead_id)
    lead = (await session.execute(query)).scalars().first()

    if not lead:
        await callback.answer("Лид не найден.", show_alert=True)
        return

    # DEBUG: Log what we found
    logger.info(f"Show message for lead {lead_id}: recommended_message = {lead.recommended_message}")

    if not lead.recommended_message:
        await callback.answer("Сообщение не найдено. Проверьте raw_qualification_data.", show_alert=True)
        return

    text = f"📝 **Сообщение для @{lead.telegram_username}:**\n" \
           "━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n" \
           f"{lead.recommended_message}\n\n" \
           "━━━━━━━━━━━━━━━━━━━━━━━━━━━\n" \
           f"👆 Скопируй и отправь @{lead.telegram_username}"
    await callback.answer(text, show_alert=True)

@router.callback_query(F.data.startswith("debug_lead_"))
async def debug_lead_handler(callback: CallbackQuery, session: AsyncSession):
    lead_id = int(callback.data.split("_")[-1])
    query = select(Lead.raw_llm_input).where(Lead.id == lead_id)
    raw_input = (await session.execute(query)).scalars().first()

    if not raw_input:
        await callback.answer("Не удалось найти данные для отладки.", show_alert=True)
        return
    
    debug_text = f"--- RAW INPUT FOR LLM ---\n\n{raw_input}"
    
    try:
        await callback.message.answer(f"<pre>{debug_text}</pre>")
        await callback.answer("Отправил отладочную информацию в чат.")
    except Exception as e:
        logger.error(f"Failed to send debug info for lead {lead_id}: {e}")
        await callback.answer("Не удалось отправить отладочную информацию.", show_alert=True)

# --- Delete Flow Handlers ---

@router.callback_query(F.data.startswith("delete_program_"))
async def delete_program_confirmation(callback: CallbackQuery, session: AsyncSession):
    program_id = int(callback.data.split("_")[-1])
    query = select(Program).where(Program.id == program_id)
    program = (await session.execute(query)).scalars().first()
    if not program:
        await callback.answer("Программа уже удалена.", show_alert=True)
        return
    
    text = f"🗑 **Удаление программы**\n\nТочно удалить \"{program.name}\"?\n\nЭто действие нельзя отменить."
    await callback.message.edit_text(text, reply_markup=get_delete_confirmation_keyboard(program_id))
    await callback.answer()

@router.callback_query(F.data.startswith("confirm_delete_"))
async def delete_program_confirmed(callback: CallbackQuery, session: AsyncSession):
    program_id = int(callback.data.split("_")[-1])
    query = select(Program).where(Program.id == program_id)
    program = (await session.execute(query)).scalars().first()

    if program:
        program_name = program.name
        await session.delete(program)
        await session.commit()
        await callback.message.edit_text(f"Программа \"{program_name}\" была удалена.", reply_markup=get_main_menu_keyboard())
    else:
        await callback.message.edit_text("Программа была удалена ранее.", reply_markup=get_main_menu_keyboard())
    await callback.answer()

# --- Edit Stub ---

@router.callback_query(F.data.startswith("edit_program_"))
async def edit_program_stub(callback: CallbackQuery):
    program_id = int(callback.data.split("_")[-1])
    logging.warning(f"Handler 'edit_program_{program_id}' is a stub.")
    await callback.answer("Редактирование программы... (в разработке)", show_alert=True)
