import time
import random
import urllib.parse
import requests
from redis import Redis
from . import envs

REDIS = Redis(
    host=envs.storage.host,
    port=envs.storage.port,
    db=0,
    password=envs.storage.password,
    decode_responses=True,
    retry_on_timeout=True
)


class Scraper:
    def scrape_data(self, url: str) -> dict:
        print('Successfully scraped the data.')
        return {
            'url': url,
            'scrape': 'ok'
        }
