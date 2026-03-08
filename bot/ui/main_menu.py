from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.i18n import t


def get_main_menu_text(language_code: str | None = None) -> str:
    """Returns localized main menu text."""
    return t("main_menu_text", language_code)


def get_main_menu_keyboard(language_code: str | None = None) -> InlineKeyboardMarkup:
    """Returns inline keyboard for the main menu."""
    builder = InlineKeyboardBuilder()
    builder.button(
        text=t("btn_my_programs", language_code),
        callback_data="my_programs",
    )
    builder.button(
        text=t("btn_pains_content", language_code),
        callback_data="pains_menu",
    )
    builder.button(
        text=t("btn_subscription", language_code),
        callback_data="subscription_menu",
    )
    builder.adjust(1)  # Adjust to 1 button per row
    return builder.as_markup()
