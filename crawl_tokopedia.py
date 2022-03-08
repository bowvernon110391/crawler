import argparse
import sys
from helpers.helpers import get_lock, release_lock
from tokopedia.request import tokped_search_product, tokped_get_products_from_result
from helpers.funcs import tokped_transform_product
import json

def main():
    parser = argparse.ArgumentParser(description="Crawl a specific amount of item on a specific page given a keyword")

    '''
    Parameter definition
    '''
    # must be provided
    parser.add_argument('keyword', type=str, help='Keyword to search')

    # optional
    parser.add_argument('-p', '--page', type=int, default=1,help="The page to visit. defaults to 1")
    parser.add_argument('-n', '--number', type=int, default=60, help="The number of items to grab. defaults to 60")
    parser.add_argument('-l', '--lock', type=str, default='0', help="The lock id for concurrency. defaults to 0")
    parser.add_argument('--pretty', action='store_true', help='Whether to indent the result or not')

    # parse args
    args = parser.parse_args()

    # attempt to lock
    if not get_lock(args.lock):
        print(f"Crawler #{args.lock} already running...")
        sys.exit(2)

    # could say we succeeds?
    try:
        # do the job
        # search product
        result = tokped_search_product(q=args.keyword, page=args.page, rows=args.number)

        # parse product
        prods = tokped_get_products_from_result(result)

        # store + transform result
        items = []
        
        for prod in prods:
            item = tokped_transform_product(prod)
            items.append(item)
        
        # return as json dump
        print(json.dumps(items,indent=2 if args.pretty else None))
    except Exception as ex:
        """ template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(ex).__name__, ex.args)
        print(message) """
        print(ex.with_traceback())

        sys.exit(1)
    finally:
        release_lock(args.lock)


if __name__ == '__main__':
    main()