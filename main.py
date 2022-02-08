import os

from tokopedia.request import tokped_get_products_from_result,tokped_search_product

if __name__ == '__main__':
    print(f"My ID: {os.getpid()}")

    curr_page = 1

    print("Crawling started.")
    while True:
        print(f"Crawling at page {curr_page}...")
        result = tokped_search_product('xiaomi mi max 2', page=curr_page)

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