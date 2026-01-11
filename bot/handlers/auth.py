import logging
from aiogram import Router, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.filters import StateFilter

import config
from bot.states import Auth
from modules.telegram_client import TelegramAuthManager

router = Router()
logger = logging.getLogger(__name__)

async def start_auth_flow(message: Message, state: FSMContext):
    """
    Starts the authentication flow by sending a code request.
    This function is intended to be called from other handlers when auth is required.
    """
    logger.info("Starting Telegram client authentication flow.")
    phone = config.TELEGRAM_PHONE
    if not phone:
        await message.answer("Ошибка: `TELEGRAM_PHONE` не указан в файле .env.")
        return

    try:
        await TelegramAuthManager.start_sign_in(phone)
        await state.set_state(Auth.enter_code)
        await message.answer(f"Отправил код подтверждения в Telegram на номер `{phone}`. Пожалуйста, введите его:")
    except Exception as e:
        logger.error(f"Failed to start auth flow: {e}")
        await message.answer(f"Не удалось отправить код. Ошибка: {e}")
        await state.clear()

@router.message(StateFilter(Auth.enter_code))
async def enter_code(message: Message, state: FSMContext, bot: Bot):
    code = message.text.strip()
    logger.info("Received Telegram auth code from user.")
    
    try:
        result = await TelegramAuthManager.submit_code(code)
        
        if result == "signed_in":
            await state.clear()
            await message.answer("✅ Отлично! Авторизация пройдена успешно.\n\nПопробуйте запустить программу снова.")
            # Ideally, we would re-trigger the original action here.
        elif result == "password_needed":
            await state.set_state(Auth.enter_password)
            await message.answer("Требуется пароль двухфакторной аутентификации (2FA). Пожалуйста, введите его:")
        else:
            await state.clear()
            await message.answer("Произошла неизвестная ошибка при вводе кода.")

    except Exception as e:
        logger.error(f"Error submitting code: {e}")
        await message.answer(f"Ошибка при вводе кода: {e}\n\nПопробуйте снова или отмените /cancel.")
        await state.clear() # Reset on error

@router.message(StateFilter(Auth.enter_password))
async def enter_password(message: Message, state: FSMContext, bot: Bot):
    password = message.text.strip()
    logger.info("Received 2FA password from user.")

    try:
        await TelegramAuthManager.submit_password(password)
        await state.clear()
        await message.answer("✅ Пароль принят! Авторизация пройдена успешно.\n\nПопробуйте запустить программу снова.")
        # Ideally, we would re-trigger the original action here.
    except Exception as e:
        logger.error(f"Error submitting password: {e}")
        await message.answer(f"Ошибка при вводе пароля: {e}\n\nПопробуйте снова или отмените /cancel.")
        await state.clear() # Reset on error
