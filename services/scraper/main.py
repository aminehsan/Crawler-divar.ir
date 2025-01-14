from src import envs
from src.celery import app
from src.scraper import Scraper


@app.task()
def scrape_test_data(url: str) -> dict:
    scraper = Scraper()
    data = scraper.scrape_data(url=url)
    task = app.send_task('parser.pars_test_data', kwargs={'data': data}, queue='parser')
    return task.id


if __name__ == '__main__':
    app.worker_main(argv=[
        'worker',
        '--events',
        '--loglevel=INFO',
        '--pool=prefork',
        f'--hostname={envs.service.name}@%h'
    ])
