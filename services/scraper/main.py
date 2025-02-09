from src import envs
from src.celery import app
from src.scraper import Scraper


@app.task()
def scrape_data(url: str) -> dict:
    scraper = Scraper()
    data_list = list()
    for data in scraper.get_data_generator(url=url):
        data_list.append(data)
    task = app.send_task('parser.pars_data', kwargs={'data_list': data_list}, queue='parser')
    return task.id


if __name__ == '__main__':
    app.worker_main(argv=[
        'worker',
        '--events',
        '--loglevel=INFO',
        '--pool=prefork',
        f'--hostname={envs.service.name}@%h'
    ])
