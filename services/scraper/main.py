from src import envs
from src.celery import app
from src.scraper import Scraper


@app.task()
def scrape_ads_list(url: str) -> dict:
    ads_list = list()
    for ads in Scraper.get_ads(url=url):
        ads_list.append(ads)
    task = app.send_task('parser.pars_ads_list', kwargs={'ads_list': ads_list}, queue='parser')
    return task.id


if __name__ == '__main__':
    app.worker_main(argv=[
        'worker',
        '--events',
        '--loglevel=INFO',
        '--pool=prefork',
        f'--hostname={envs.service.name}@%h'
    ])
