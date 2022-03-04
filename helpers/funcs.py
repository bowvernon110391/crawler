
import os
from tokopedia.request import tokped_request_product_detail
import re
from datetime import datetime
from dotenv import load_dotenv
import googlemaps

def gmap_reverse_geocode(coord):
    load_dotenv()
    GMAP_API_KEY = os.getenv('GMAP_API_KEY')
    gmap = googlemaps.Client(key=GMAP_API_KEY)

    locations = gmap.reverse_geocode(coord)
    if len(locations):
        return locations[0]['formatted_address']
    return '-'


def tokped_transform_product(prod):
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
            'alamat': gmap_reverse_geocode((lat, lon)),
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