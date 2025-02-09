from src import envs
from src.celery import app
from src.parser import Parser


@app.task()
def pars_test_data(data_list: list) -> list:
    parser = Parser()
    data = parser.pars_data(data_list=data_list)
    return data


if __name__ == '__main__':
    app.worker_main(argv=[
        'worker',
        '--events',
        '--loglevel=INFO',
        '--pool=prefork',
        f'--hostname={envs.service.name}@%h'
    ])
