from src import envs
from src.celery import app

# from src.parser import ...


# @app.task()
# def ...(...: list) -> list:
#     ...


if __name__ == '__main__':
    app.worker_main(argv=[
        'worker',
        '--events',
        '--loglevel=INFO',
        '--pool=prefork',
        f'--hostname={envs.service.name}@%h'
    ])
