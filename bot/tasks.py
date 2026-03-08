import asyncio
import logging

from bot.celery_app import celery_app
from bot.db_config import ensure_engine_process_bound
from bot.services.program_runner import run_program_job

logger = logging.getLogger(__name__)


@celery_app.task(
    bind=True,
    name="bot.tasks.run_program_job_task",
    autoretry_for=(Exception,),
    retry_backoff=True,
    retry_jitter=True,
    retry_kwargs={"max_retries": 3},
)
def run_program_job_task(self, program_id: int, chat_id: int) -> dict:
    """Execute one program run in worker process."""
    ensure_engine_process_bound()
    logger.info(
        f"[CELERY] Running program job task: program_id={program_id}, chat_id={chat_id}"
    )
    asyncio.run(run_program_job(program_id, chat_id))
    return {"program_id": program_id, "chat_id": chat_id}


def enqueue_program_job(program_id: int, chat_id: int) -> str:
    """Enqueue a program job and return task id."""
    task = run_program_job_task.delay(program_id=program_id, chat_id=chat_id)
    return task.id
