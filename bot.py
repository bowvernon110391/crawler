import os
import json
from time import sleep
from urllib.parse import parse_qsl, urlencode
import requests

def load_json(fname):
    ret = None
    try:
        f = open(fname)
        ret = json.load(f)
    except OSError:
        print(f"Failed to open {fname}")
    finally:
        f.close()
    return ret


'''
Global settings
'''
req_headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36',
    'Content-Type': 'application/json'
}


def tokped_search_product(q, page=1, rows=60):
    # start dihitung otomatis
    start = (page-1) * rows

    req_search_prod = load_json('req_search_product.json')
    parsed = dict(parse_qsl(req_search_prod[0]['variables']['params']))

    parsed['q'] = q
    parsed['page'] = str(page)
    parsed['rows'] = str(rows)
    parsed['start'] = str(start)

    req_search_prod[0]['variables']['params'] = urlencode(parsed)

    result = requests.post('https://gql.tokopedia.com/', json=req_search_prod)

    if result.status_code == 200:
        return result.json()
    else:
        return None

def tokped_get_products_from_result(res):
    return res[0]['data']['ace_search_product_v4']['data']['products']

if __name__ == '__main__':
    print(f"My ID: {os.getpid()}")

    curr_page = 1

    print("Crawling started.")
    while True:
        print(f"Crawling at page {curr_page}...")
        result = tokped_search_product('macbook 16gb', page=curr_page)

        if not result:
            break

        prods = tokped_get_products_from_result(result)
        prod_count = len(prods)
        print(f"Found {prod_count} prods")

        if not prod_count:
            break

        # sleep(1)
        curr_page = curr_page + 1
    
    print("Crawling ended.")