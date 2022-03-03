import json
import os
import requests
from helpers.helpers import load_json
from urllib.parse import parse_qsl, urlencode

tokopedia_endpoint = 'https://gql.tokopedia.com/'

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

    result = requests.post(tokopedia_endpoint, json=req_search_prod)

    if result.status_code == 200:
        return result.json()
    else:
        return None

def tokped_get_products_from_result(res):
    """Ambil data produk dari response

    parameter:

    @res : reponse dari tokped_search_product

    returns:

    array of product
    """
    return res[0]['data']['ace_search_product_v4']['data']['products']

def tokped_get_shop_domain(prod):
    '''Get shop domain dari domain toko

    parameter:

    @prod : produk dari tokped_get_products_from_result

    return : domain dari toko (non url), None if failed
    '''
    if not prod:
        return None

    # ambil domainnya?
    domain = prod['shop']['url'] or ''
    return str.split(domain, '/')[-1]

def tokped_get_product_key(prod):
    '''Get product key from product url

    parameter:

    @prod : produk dari tokped_get_products_from_result

    return : product key (komponen terakhir dari url)
    '''
    if not prod:
        return None

    gaKey = prod['gaKey'] or ''
    return gaKey.split('/')[-1]

def tokped_request_pdpsession(shop_domain, prod_key):
    '''request pdp session untuk request detail produk

    parameter:

    @shop_domain : domain toko
    @prod_key : product key

    return : json dari graphql request
    '''

    filename = os.path.join(os.path.dirname(__file__), 'json/req_prod_detail_layout.json')
    req_prod_detail = load_json(filename)

    # modify some variable
    req_prod_detail[0]['variables']['shopDomain'] = shop_domain
    req_prod_detail[0]['variables']['productKey'] = prod_key

    # send request?
    # do not forget, add { X-TKPD-Akamai : pdpGetLayout } to header
    result = requests.post(tokopedia_endpoint, json=req_prod_detail, headers={
        'X-TKPD-Akamai' : 'pdpGetLayout'
    })

    if result.status_code == 200:
        return result.json()
    else:
        return None

def tokped_get_pdpsession_string(res):
    if not res:
        return None

    return res[0]['data']['pdpGetLayout']['pdpSession']

def tokped_request_product_detail_from_layout(pdplayout):
    '''ambil detil produk.

    parameter:

    @pdplayout : hasil dari request pdpsession

    return : json berisi detil dari produk
    '''
    if not pdplayout:
        return None

    # grab pdpSession string and item id as string
    pdpsession = tokped_get_pdpsession_string(pdplayout)
    prod_id_str = pdplayout[0]['data']['pdpGetLayout']['basicInfo']['id']

    # load the json file
    filename = os.path.join(os.path.dirname(__file__), 'json/req_get_prod_detail.json')
    req_prod_detail = load_json(filename)

    # inject our data
    req_prod_detail[0]['variables']['productID'] = prod_id_str
    req_prod_detail[0]['variables']['pdpSession'] = pdpsession

    # send request (no special header required?)
    result = requests.post(tokopedia_endpoint, json=req_prod_detail)

    if result.status_code == 200:
        return result.json()
    else:
        return None


def tokped_request_product_detail(prod):
    '''ambil data dari product, tambahkan informasi toko + lain2
    lalu pack sesuai format dari database
    '''
    prod_key = tokped_get_product_key(prod)
    shop_domain = tokped_get_shop_domain(prod)

    pdplayout = tokped_request_pdpsession(shop_domain, prod_key)
    prod_detail = tokped_request_product_detail_from_layout(pdplayout)
    
    return prod_detail