import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from bot.db_config import engine, async_session
from bot.handlers import start, program_create, program_list, program_view, auth, lead_viewer
from bot.middleware.db_session import DbSessionMiddleware
from bot.models.base import Base
from bot.models.program import Program, ProgramChat
from bot.models.lead import Lead
from bot.scheduler import scheduler


async def create_tables():
    """Creates all tables in the database."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def main(bot_token: str):
    """Bot entry point."""

    # Create tables
    await create_tables()

    bot = Bot(token=bot_token, parse_mode="HTML")
    dp = Dispatcher(
        storage=MemoryStorage(),
        bot=bot,
        scheduler=scheduler
    )

    # Register middleware
    dp.update.middleware(DbSessionMiddleware(session_pool=async_session))

    # Register routers
    dp.include_router(start.router)
    dp.include_router(program_create.router)
    dp.include_router(program_list.router)
    dp.include_router(program_view.router)
    dp.include_router(auth.router)
    dp.include_router(lead_viewer.router)

    # Register shutdown hook for scheduler
    dp.shutdown.register(scheduler.shutdown)

    # Start scheduler and polling
    scheduler.start()
    logging.info("Starting bot...")
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)
