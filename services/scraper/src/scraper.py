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
    def _get_preloaded_state(self, url: str) -> dict:
        assert 'https://divar.ir/s/' in url
        response = requests.get(
            url=url,
            headers={
                'Accept': 'text/html',
                'User-Agent': 'Twitterbot/1'
            }
        )
        soup = BeautifulSoup(response.text, 'html.parser')
        scripts = soup.find_all('script')
        script_str = str()
        for script in scripts:
            if 'window.__PRELOADED_STATE__' in script.text:
                script_str = script.text
                break
        return json.loads(re.search(r'__PRELOADED_STATE__\s*=\s*(\{.*?});', script_str).group(1))

    def _get_data(self, payload: dict) -> dict:
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
        result = response.json()
        return result

    def scrape_data(self, url: str) -> dict:
        preloaded_state = self._get_preloaded_state(url=url)
        search_data = preloaded_state['nb']['serverSideInitialActionLog']['server_side_info']['info']['search_data']
        payload = {
            'city_ids': search_data['cities'],
            'search_data': {
                'form_data': json.loads(search_data['form_data_json']),
                'query': search_data.get('query', str())
            }
        }
        data = self._get_data(payload=payload)
        print('Successfully scraped the data.')
        return data
