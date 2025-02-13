import json
import re
import requests
from bs4 import BeautifulSoup

PROXIES = {'https': 'http://username:password@host:port'}


def _get_preloaded_state(url: str) -> dict:
    response = requests.get(
        url=url,
        headers={
            'Accept': 'text/html',
            'User-Agent': 'Twitterbot/1'
        },
        proxies=PROXIES
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
        data=json.dumps(payload),
        proxies=PROXIES
    )
    assert response.status_code == 200
    return response.json()


def scraper_ads(url: str) -> dict:
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


def parser_ads_list(ads_list: list) -> list:
    ads_pars_list = list()
    for ads in ads_list:
        for widget in ads.get('list_widgets', list()):
            if widget['widget_type'] == 'POST_ROW':
                ads_pars_list.append(widget)
    return ads_pars_list




if __name__ == '__main__':
    url = 'https://divar.ir/s/iran/computer-parts-accessories?q=l&cities=1%2C17&has_secure_payment=true'
    ads_list = list()
    for ads in scraper_ads(url=url):
        ads_list.append(ads)
    ads_pars_list = parser_ads_list(ads_list=ads_list)
    print(ads_pars_list)
