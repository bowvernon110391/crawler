import json
import sys
from helpers.helpers import get_lock, release_lock

from tokopedia.request import tokped_get_products_from_result,tokped_search_product

if __name__ == '__main__':

    # read terminal arguments?
    if len(sys.argv) < 2:
        print("usage: python main.py [search_keyword]")
        sys.exit()
    
    if not get_lock():
        print("Crawler already running! exiting...")
        sys.exit()

    json_result = []
    try:
        curr_page = 1
        keyword = sys.argv[1]

        # print(f"Crawling started. Scraping for [{keyword}]")
        while True:
            # print(f"Crawling at page {curr_page}...")
            result = tokped_search_product(keyword, page=curr_page, rows=100)

            if not result:
                break

            prods = tokped_get_products_from_result(result)
            prod_count = len(prods)
            # print(f"Found {prod_count} prods")

            if not prod_count:
                break
            else:
                # print(json.dumps(prods[0], indent=2))
                json_result.extend(prods)

            # sleep(1)
            curr_page = curr_page + 1
        
        # print("Crawling ended.")
    except:
        print("{ \"error\": \"exception happens\" }")
    finally:
        release_lock()
    
    # if len(json_result):
    print(json.dumps(json_result, indent=2))