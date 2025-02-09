import json
import re
import requests
from bs4 import BeautifulSoup

URL = 'https://divar.ir/s/iran/computer-parts-accessories?q=l&cities=1%2C17&has_secure_payment=true'

if __name__ == '__main__':
    response = requests.get(
        url=URL,
        headers={
            'Accept': 'text/html',
            'User-Agent': 'Twitterbot/1'
        }
    )
    result_1 = response.text

    soup = BeautifulSoup(result_1, 'html.parser')
    scripts = soup.find_all('script')

    script_str = str()
    for script in scripts:
        if 'window.__PRELOADED_STATE__' in script.text:
            script_str = script.text
            break

    script_dict = json.loads(re.search(r'__PRELOADED_STATE__\s*=\s*(\{.*?});', script_str).group(1))

    search_data = script_dict['nb']['serverSideInitialActionLog']['server_side_info']['info']['search_data']

    payload = {
        'city_ids': search_data['cities'],
        'search_data': {
            'form_data': json.loads(search_data['form_data_json']),
            'query': search_data.get('query')
        }
    }

    response = requests.post(
        url='https://api.divar.ir/v8/postlist/w/search',
        headers={
            'Accept': 'application/json',
            'User-Agent': 'Twitterbot/1',
            'Content-Type': 'application/json'
        },
        data=json.dumps(payload)
    )
    result_2 = response.json()

    print(result_2)

    # info = result_2['action_log']['server_side_info']['info']
    # search_data = info['search_data']
    #
    # pagination = result_2['pagination']
    # has_next_page = pagination['has_next_page']
    # is_first_page = pagination['is_first_page']
    # data = pagination['data']
    #
    # seo_details = result_2['seo_details']

