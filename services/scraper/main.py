from src import envs
from src.celery import app

# from src.scraper import ...


# @app.task()
# def ...(...: str) -> dict:
#     ...


if __name__ == '__main__':
    app.worker_main(argv=[
        'worker',
        '--events',
        '--loglevel=INFO',
        '--pool=prefork',
        f'--hostname={envs.service.name}@%h'
    ])
