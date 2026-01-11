from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore

from bot.db_config import DATABASE_URL

# Configure the job store to use our PostgreSQL database
jobstores = {
    'default': SQLAlchemyJobStore(url=DATABASE_URL.replace("+asyncpg", "")) # Job store needs sync URL
}

# Initialize the scheduler
scheduler = AsyncIOScheduler(jobstores=jobstores)
