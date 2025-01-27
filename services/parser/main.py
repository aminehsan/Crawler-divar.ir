from src import envs
from src.celery import app
from src.parser import Parser


@app.task()
def pars_test_data(data: dict) -> dict:
    parser = Parser()
    data = parser.pars_data(data=data)
    return data


if __name__ == '__main__':
    app.worker_main(argv=[
        'worker',
        '--events',
        '--loglevel=INFO',
        '--pool=prefork',
        f'--hostname={envs.service.name}@%h'
    ])
