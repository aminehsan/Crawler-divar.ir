from fastapi import APIRouter
from .celery import app
from . import models

router = APIRouter()


# @router.post('/.../...')
# def ...(...: models.Input):
#     task = app.send_task(
#         name='scraper....',
#         kwargs={'...': payload....},
#         queue='scraper'
#     )
#     return {...}


@router.get('/result/{_id}')
def get_result(_id: str):
    task = app.AsyncResult(_id)
    return {
        'status': task.state,
        'result': task.result
    }
