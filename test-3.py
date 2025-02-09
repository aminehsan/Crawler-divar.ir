import json
import re
import requests
from bs4 import BeautifulSoup


def get_preloaded_state(url: str) -> dict:
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


def get_data(payload: dict) -> dict:
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


def get_data_generator(payload: dict) -> dict:
    has_next_page = True
    while has_next_page:
        data = get_data(payload)
        has_next_page = data['pagination'].get('has_next_page')
        payload['pagination_data'] = data['pagination']['data']
        yield data


if __name__ == '__main__':
    url = 'https://divar.ir/s/iran/computer-parts-accessories?q=l&cities=1%2C17&has_secure_payment=true'
    preloaded_state = get_preloaded_state(url=url)
    search_data = preloaded_state['nb']['serverSideInitialActionLog']['server_side_info']['info']['search_data']
    payload = {
        'city_ids': search_data['cities'],
        'search_data': {
            'form_data': json.loads(search_data['form_data_json']),
            'query': search_data.get('query')
        }
    }
    for data in get_data_generator(payload=payload):
        print(data)
