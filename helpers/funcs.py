
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

def tokped_parse_tags(ts):
    return list( map( lambda s: re.sub('[\-\.]', ' ', s), ts.split('/')) )

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

    # some data may be empty?
    if d['nearestWarehouse'] and len(d['nearestWarehouse']) > 0:
        kode_pos = d['nearestWarehouse'][0]['warehouse_info']['postal_code']

        # sometimes coordinate isn't provided
        coord = d['nearestWarehouse'][0]['warehouse_info']['geolocation']

        if len(coord) > 3:
            (lat, lon) = coord.split(',')


    """ if type(lat) == tuple:
        print('cause: ' + json.dumps(d['nearestWarehouse'][0]['warehouse_info'], indent=2)) """

    item = {
        # item_id is unique per marketplace
        # we're not using internal id
        'item_id': prod['id'],
        'name': prod['name'],
        'rating': int(prod['rating']),
        'rating_avg': None if not prod['ratingAverage'] else float(prod['ratingAverage']),
        'price': float(re.sub('[^0-9]','', prod['price'])),
        'url': prod['url'],
        'image_url': prod['imageUrl'],
        'view_count': int(d['productView']),
        'wishlist_count': int(d['wishlistCount']),
        'category_name': prod['categoryName'],
        'tags': tokped_parse_tags(prod['categoryBreadcrumb']),
        # shop data
        'shop': {
            'id': prod['shop']['shopId'],
            'name': prod['shop']['name'],
            'url': prod['shop']['url'],
            'domain': d['shopInfo']['shopCore']['domain'],
            'kota': prod['shop']['city'],
            'alamat': '-' if not (lat and lon) else gmap_reverse_geocode((lat, lon)),
            'last_active_timestamp': last_active_timestamp,
            'kode_pos': kode_pos,
            'lat': float(lat) if lat and lon else None,
            'lon': float(lon) if lon and lat else None,
            'registered_at': registered_at,
            # our custom marker
            'marketplace': 'tokopedia'
        }
    }

    return item