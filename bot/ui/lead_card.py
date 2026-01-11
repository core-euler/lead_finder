from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.models.lead import Lead # Import Lead for type hinting

def get_lead_card_keyboard(lead_id: int) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="📝 Показать сообщение", callback_data=f"show_message_{lead_id}")
    builder.button(text="🐞 Debug", callback_data=f"debug_lead_{lead_id}")
    builder.adjust(2)
    return builder.as_markup()

def format_lead_card(lead: Lead, index: int, total: int) -> str:
    """Formats a Lead object into a message string for the bot."""
    # Use lead.program.name if the program relationship is eagerly loaded
    program_name = lead.program.name if lead.program else "N/A"
    
    return (
        f"🎯 **Лид #{index} из {total}**\n"
        f"Программа: {program_name}\n"
        f"━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
        f"👤 @{lead.telegram_username}\n"
        f"⭐ Оценка: {lead.qualification_score}/10\n\n"
        f"**💼 Бизнес:**\n{lead.business_summary or 'Нет данных'}\n\n"
        f"**😤 Боли:**\n{lead.pains_summary or 'Нет данных'}\n\n"
        f"**💡 Что предложить:**\n{lead.solution_idea or 'Нет данных'}\n"
    )