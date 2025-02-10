import json
import re
import requests
from redis import Redis
from bs4 import BeautifulSoup
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
    @staticmethod
    def _get_preloaded_state(url: str) -> dict:
        response = requests.get(
            url=url,
            headers={
                'Accept': 'text/html',
                'User-Agent': 'Twitterbot/1'
            }
        )
        soup = BeautifulSoup(response.text, 'html.parser')
        script_str = str()
        for script_tag in soup.find_all('script'):
            if 'window.__PRELOADED_STATE__' in script_tag.text:
                script_str = script_tag.text
                break
        return json.loads(re.search(r'__PRELOADED_STATE__\s*=\s*(\{.*?});', script_str).group(1))

    @staticmethod
    def _get_data(payload: dict) -> dict:
        response = requests.post(
            url='https://api.divar.ir/v8/postlist/w/search',
            headers={
                'Accept': 'application/json',
                'User-Agent': 'Twitterbot/1',
                'Content-Type': 'application/json'
            },
            data=json.dumps(payload)
        )
        assert response.status_code == 200
        return response.json()

    @staticmethod
    def get_data_generator(url: str) -> dict:
        preloaded_state = Scraper._get_preloaded_state(url=url)
        search_data = preloaded_state['nb']['serverSideInitialActionLog']['server_side_info']['info']['search_data']
        payload = {
            'city_ids': search_data['cities'],
            'search_data': {
                'form_data': json.loads(search_data['form_data_json']),
                'query': search_data.get('query')
            }
        }
        has_next_page = True
        while has_next_page:
            data = Scraper._get_data(payload)
            has_next_page = data['pagination'].get('has_next_page')
            payload['pagination_data'] = data['pagination']['data']
            yield data
