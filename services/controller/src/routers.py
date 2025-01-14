from fastapi import APIRouter
from .celery import app
from . import models

router = APIRouter()


@router.post('/test')
def get_test_data(payload: models.Input):
    task = app.send_task(
        name='scraper.scrape_test_data',
        kwargs={'url': payload.url},
        queue='scraper'
    )
    return {'id': task.id}


@router.get('/result/{_id}')
def get_result(_id: str):
    task = app.AsyncResult(_id)
    return {
        'status': task.state,
        'result': task.result
    }
