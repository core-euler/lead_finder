import logging
from aiogram import Router, F, Bot
from aiogram.types import CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from bot.models.lead import Lead
from bot.ui.lead_card import format_lead_card, get_lead_card_keyboard

router = Router()
logger = logging.getLogger(__name__)

@router.callback_query(F.data.startswith("view_program_leads_"))
async def view_program_leads_handler(callback: CallbackQuery, session: AsyncSession, bot: Bot):
    program_id = int(callback.data.split("_")[-1])
    logger.info(f"Fetching leads for program_id={program_id}")

    query = (
        select(Lead)
        .where(Lead.program_id == program_id)
        .options(selectinload(Lead.program)) # Eager load the program to get its name for the card
        .order_by(Lead.created_at.desc())
    )
    result = await session.execute(query)
    leads = result.scalars().all()

    if not leads:
        await callback.answer("Для этой программы лиды еще не найдены.", show_alert=True)
        return

    await callback.message.answer(f"Отправляю {len(leads)} найденных лидов...")
    await callback.answer()

    for i, lead in enumerate(leads):
        card_text = format_lead_card(lead, i + 1, len(leads))
        await bot.send_message(
            callback.from_user.id,
            card_text,
            reply_markup=get_lead_card_keyboard(lead.id),
            disable_web_page_preview=True
        )
