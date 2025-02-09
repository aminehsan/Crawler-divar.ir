import requests
import json

if __name__ == '__main__':
    payload = dict()

    payload['city_ids'] = [
        '1'
    ]

    # payload['pagination_data'] = {
    #     '@type': 'type.googleapis.com/post_list.PaginationData',
    #     'last_post_date': '2025-01-16T17:53:28.276024Z',
    #     'page': 1
    # }

    payload['search_data'] = {
        'form_data': {
            'data': {
                'business-type': {
                    'str': {
                        'value': 'personal'
                    }
                },
                'category': {
                    'str': {
                        'value': 'light'
                    }
                },
                'price': {
                    'number_range': {
                        'minimum': '100000000',
                        'maximum': '300000000'
                    }
                }
            }
        }
    }

    response = requests.post(
        url='https://api.divar.ir/v8/postlist/w/search',
        headers={
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'User-Agent': 'Twitterbot/1'
        },
        data=json.dumps(payload)
    )

    result = response.json()
    print(result)
