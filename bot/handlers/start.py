import logging
from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery

from bot.ui.main_menu import get_main_menu_keyboard, MAIN_MENU_TEXT

router = Router()

@router.message(Command("start"))
async def start_handler(message: Message):
    """Handler for the /start command."""
    logging.info("Handling /start command")
    await message.answer(
        MAIN_MENU_TEXT,
        reply_markup=get_main_menu_keyboard()
    )

@router.callback_query(F.data == "main_menu")
async def main_menu_callback_handler(callback: CallbackQuery):
    """Handler for the 'Back to Main Menu' button."""
    logging.info("Handling 'main_menu' callback")
    await callback.message.edit_text(
        MAIN_MENU_TEXT,
        reply_markup=get_main_menu_keyboard()
    )
    await callback.answer()

# --- Stub handlers for main menu buttons ---

@router.callback_query(F.data == "statistics")
async def statistics_stub(callback: CallbackQuery):
    logging.warning("Handler 'statistics' is a stub.")
    await callback.answer("Вы выбрали 'Статистика'. Этот раздел в разработке.")

@router.callback_query(F.data == "settings")
async def settings_stub(callback: CallbackQuery):
    logging.warning("Handler 'settings' is a stub.")
    await callback.answer("Вы выбрали 'Настройки'. Этот раздел в разработке.")
