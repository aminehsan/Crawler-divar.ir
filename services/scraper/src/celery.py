from celery import Celery
from . import envs

app = Celery(
    main=envs.service.name,
    backend=f'redis://:{envs.storage.password}@{envs.storage.host}:{envs.storage.port}/1',
    broker=f'pyamqp://{envs.broker.username}:{envs.broker.password}@{envs.broker.host}:{envs.broker.port}//'
)

app.conf.update(
    broker_connection_retry_on_startup=True,
    timezone='Asia/Tehran',
    result_expires=60 * 60 * 24 * 2,
    task_soft_time_limit=int(60 * 60 * 1.5),
    task_time_limit=60 * 60 * 2,
    worker_concurrency=1,
    worker_prefetch_multiplier=1,
    task_default_queue=envs.service.name
)
