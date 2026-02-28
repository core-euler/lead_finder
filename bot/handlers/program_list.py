import logging
from aiogram import Router, F
from aiogram.types import CallbackQuery, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from bot.models.program import Program
from bot.i18n import get_locale, pick, t
from bot.ui.main_menu import get_main_menu_keyboard

router = Router()

def get_my_programs_keyboard(
    programs: list[Program], language_code: str | None
) -> InlineKeyboardMarkup:
    locale = get_locale(language_code)
    builder = InlineKeyboardBuilder()
    if programs:
        for program in programs:
            builder.button(text=f"📁 {program.name}", callback_data=f"show_program_{program.id}")
        builder.adjust(1) # Adjust later for 2-column layout if many programs
        builder.button(
            text=pick(locale, "➕ Создать ещё", "➕ Create Another"),
            callback_data="create_program",
        ) # Add as a regular button
    else:
        builder.button(
            text=pick(locale, "➕ Создать программу", "➕ Create Program"),
            callback_data="create_program",
        )
    
    # These buttons will appear on their own rows due to adjust or explicitly being added after others
    builder.button(text=t("btn_back", language_code), callback_data="main_menu")
    builder.adjust(1) # Ensure these last two buttons are on separate rows, or a different adjust if more buttons are added

    return builder.as_markup()

@router.callback_query(F.data == "my_programs")
async def my_programs_handler(callback: CallbackQuery, session: AsyncSession):
    logging.info("Handling 'my_programs' callback.")
    locale = get_locale(callback.from_user.language_code)
    
    # Use selectinload to eagerly load the 'chats' relationship
    query = (
        select(Program)
        .options(selectinload(Program.chats))
        .where(Program.user_id == callback.from_user.id)
        .order_by(Program.id)
    )
    result = await session.execute(query)
    programs = result.scalars().all()

    if not programs:
        text = pick(
            locale,
            (
                "📋 Мои программы\n\n"
                "🔍 У тебя пока нет программ поиска.\n"
                "Создай первую — это займёт пару минут 👇"
            ),
            (
                "📋 My Programs\n\n"
                "🔍 You don't have any programs yet.\n"
                "Create your first one in a couple of minutes 👇"
            ),
        )
    else:
        text = pick(locale, "📋 Мои программы\n\n", "📋 My Programs\n\n")
        for i, program in enumerate(programs):
            schedule_status = (
                f"⏰ {program.schedule_time}"
                if program.auto_collect_enabled else
                pick(locale, "⏸ выключено", "⏸ disabled")
            )
            text += (
                f"{i+1}️⃣ {program.name}\n"
                f"   {len(program.chats)} "
                f"{pick(locale, 'чат(а/ов)', 'chat(s)')} • "
                f"{pick(locale, 'скор ≥', 'score ≥')}{program.min_score} • "
                f"{schedule_status}\n"
                "\n"
            )

    await callback.message.edit_text(
        text,
        reply_markup=get_my_programs_keyboard(
            programs, callback.from_user.language_code
        ),
    )
    await callback.answer()
