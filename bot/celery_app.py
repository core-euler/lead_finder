from celery import Celery
from celery.signals import worker_process_init, worker_process_shutdown

import config
from bot.db_config import ensure_engine_process_bound, dispose_engine_sync


celery_app = Celery(
    "leadcore",
    broker=config.CELERY_BROKER_URL,
    backend=config.CELERY_RESULT_BACKEND,
    include=["bot.tasks"],
)

celery_app.conf.update(
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    timezone="UTC",
    enable_utc=True,
    task_track_started=True,
)


@worker_process_init.connect
def _on_worker_process_init(**_kwargs):
    ensure_engine_process_bound()


@worker_process_shutdown.connect
def _on_worker_process_shutdown(**_kwargs):
    dispose_engine_sync()
