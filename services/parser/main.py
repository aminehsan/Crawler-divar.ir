from src import envs
from src.celery import app
from src.parser import Parser


@app.task()
def pars_ads_list(ads_list: list) -> list:
    return Parser.pars_ads_list(ads_list=ads_list)


if __name__ == '__main__':
    app.worker_main(argv=[
        'worker',
        '--events',
        '--loglevel=INFO',
        '--pool=prefork',
        f'--hostname={envs.service.name}@%h'
    ])
