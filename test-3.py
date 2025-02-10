import json
import re
import requests
from bs4 import BeautifulSoup


def _get_preloaded_state(url: str) -> dict:
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


def get_ads(url: str) -> dict:
    assert 'https://divar.ir/s/' in url
    preloaded_state = _get_preloaded_state(url=url)
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
        ads = _get_data(payload)
        has_next_page = ads['pagination'].get('has_next_page')
        payload['pagination_data'] = ads['pagination']['data']
        yield ads


if __name__ == '__main__':
    url = 'https://divar.ir/s/tehran/buy-apartment?business-type=personal&price=-3000000000'
    for ads in get_ads(url=url):
        print(ads)
