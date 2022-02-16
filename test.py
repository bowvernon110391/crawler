from tokopedia.request import tokped_search_product, tokped_get_products_from_result, tokped_get_product_key, tokped_get_shop_domain

keyword = 'Lampu Verza'

try:
    result = tokped_search_product(keyword)
    prods = tokped_get_products_from_result(result)

    print(f"First product key: {tokped_get_product_key(prods[0])}, shop_domain: {tokped_get_shop_domain(prods[0])}")
finally:
    pass