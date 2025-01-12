from celery import Celery
from . import envs

app = Celery(
    main=envs.service.name,
    backend=f'redis://:{envs.storage.password}@{envs.storage.host}:{envs.storage.port}/1',
    broker=f'pyamqp://{envs.broker.username}:{envs.broker.password}@{envs.broker.host}:{envs.broker.port}//'
)
