
import imp
from tokopedia.request import tokped_request_product_detail
import re
from datetime import datetime

def transform_product_tokped(prod):
    # first get detail
    details = tokped_request_product_detail(prod)

    # only take the first detail
    d = details[0]['data']['pdpGetData']

    # optional data
    kode_pos = ''
    lat = None,
    lon = None
    last_active_timestamp = datetime.fromtimestamp(int(d['shopInfo']['shopLastActive'])).strftime('%Y-%m-%d %H:%M:%S')
    registered_at = datetime.fromtimestamp(int(d['shopInfo']['createInfo']['epochShopCreated'])).strftime('%Y-%m-%d %H:%M:%S')

    if d['nearestWarehouse'] and len(d['nearestWarehouse']) > 0:
        kode_pos = d['nearestWarehouse'][0]['warehouse_info']['postal_code']
        lat, lon = d['nearestWarehouse'][0]['warehouse_info']['geolocation'].split(',')
    

    item = {
        # item_id is unique per marketplace
        # we're not using internal id
        'item_id': prod['id'],
        'name': prod['name'],
        'rating': int(prod['rating']),
        'rating_avg': float(prod['ratingAverage']),
        'price': float(re.sub('[^0-9]','', prod['price'])),
        'url': prod['url'],
        'image_url': prod['imageUrl'],
        'view_count': int(d['productView']),
        'wishlist_count': int(d['wishlistCount']),
        # shop data
        'shop': {
            'id': prod['shop']['shopId'],
            'name': prod['shop']['name'],
            'url': prod['shop']['url'],
            'domain': d['shopInfo']['shopCore']['domain'],
            'kota': prod['shop']['city'],
            'alamat': 'resolve via gmap pls',
            'last_active_timestamp': last_active_timestamp,
            'kode_pos': kode_pos,
            'lat': float(lat),
            'lon': float(lon),
            'registered_at': registered_at,
            # our custom marker
            'marketplace': 'tokopedia'
        }
    }

    return item