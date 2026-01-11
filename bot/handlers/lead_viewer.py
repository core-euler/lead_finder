import logging
from aiogram import Router, F, Bot
from aiogram.types import CallbackQuery, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from bot.models.lead import Lead
from bot.ui.lead_card import format_lead_card, get_lead_card_keyboard

router = Router()
logger = logging.getLogger(__name__)


def get_lead_navigation_keyboard(program_id: int, current_page: int, total_pages: int, lead_id: int) -> InlineKeyboardMarkup:
    """Creates pagination keyboard for lead viewing."""
    builder = InlineKeyboardBuilder()

    # Navigation buttons
    if current_page > 0:
        builder.button(text="◀️ Назад", callback_data=f"lead_page_{program_id}_{current_page - 1}")

    builder.button(text=f"{current_page + 1}/{total_pages}", callback_data="noop")

    if current_page < total_pages - 1:
        builder.button(text="Вперёд ▶️", callback_data=f"lead_page_{program_id}_{current_page + 1}")

    # Back to program button
    builder.button(text="◀️ К программе", callback_data=f"show_program_{program_id}")

    # Adjust layout: navigation buttons in one row, back button on separate row
    nav_button_count = 1  # Always has page counter
    if current_page > 0:
        nav_button_count += 1
    if current_page < total_pages - 1:
        nav_button_count += 1

    builder.adjust(nav_button_count, 1)

    return builder.as_markup()


@router.callback_query(F.data.startswith("view_program_leads_"))
async def view_program_leads_handler(callback: CallbackQuery, session: AsyncSession, bot: Bot):
    """Shows the first lead in paginated view."""
    program_id = int(callback.data.split("_")[-1])
    await show_lead_page(callback, session, program_id, page=0, edit=False)


@router.callback_query(F.data.startswith("lead_page_"))
async def lead_page_navigation_handler(callback: CallbackQuery, session: AsyncSession):
    """Handles pagination navigation between leads."""
    parts = callback.data.split("_")
    program_id = int(parts[2])
    page = int(parts[3])
    await show_lead_page(callback, session, program_id, page, edit=True)


async def show_lead_page(callback: CallbackQuery, session: AsyncSession, program_id: int, page: int, edit: bool):
    """Shows a specific lead page."""
    logger.info(f"Showing lead page {page} for program_id={program_id}")

    query = (
        select(Lead)
        .where(Lead.program_id == program_id)
        .options(selectinload(Lead.program))
        .order_by(Lead.created_at.desc())
    )
    result = await session.execute(query)
    leads = result.scalars().all()

    if not leads:
        await callback.answer("Для этой программы лиды еще не найдены.", show_alert=True)
        return

    total_leads = len(leads)

    # Validate page number
    if page < 0 or page >= total_leads:
        await callback.answer("Неверная страница.", show_alert=True)
        return

    lead = leads[page]
    card_text = format_lead_card(lead, page + 1, total_leads)
    keyboard = get_lead_navigation_keyboard(program_id, page, total_leads, lead.id)

    if edit:
        await callback.message.edit_text(card_text, reply_markup=keyboard, disable_web_page_preview=True)
        await callback.answer()
    else:
        await callback.message.answer(card_text, reply_markup=keyboard, disable_web_page_preview=True)
        await callback.answer()


@router.callback_query(F.data == "noop")
async def noop_handler(callback: CallbackQuery):
    """Handles the page counter button (does nothing)."""
    await callback.answer()
