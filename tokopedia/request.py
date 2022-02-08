import os
import requests
from helpers.helpers import load_json
from urllib.parse import parse_qsl, urlencode

def tokped_search_product(q, page=1, rows=60):
    """Cari produk di tokopedia

    parameters:

    @q: keyword pencarian, misal 'macbook'
    @page: halaman ke berapa
    @rows: berapa items per request, kalau 0 berarti udh habis
    """
    # start dihitung otomatis
    start = (page-1) * rows

    filename = os.path.join(os.path.dirname(__file__), 'json/req_search_product.json')
    req_search_prod = load_json(filename)
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