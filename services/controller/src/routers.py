from fastapi import APIRouter
from .celery import app
from . import models

router = APIRouter()


@router.post('/ads-list')
def get_ads_list(payload: models.Input):
    assert 'https://divar.ir/s/' in payload.url
    task = app.send_task(
        name='scraper.scrape_ads_list',
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
