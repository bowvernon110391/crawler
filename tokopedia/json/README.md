# TOKOPEDIA API

## How?
it uses GraphQL. for querying product, see `req_search_product.json` for sample output, see `res_search_product.json`

## Quirks
to request, just modify and send POST request to `https://gql.tokopedia.com` without any specific header.
But for requesting product detail layout (to get info such as `whid` (warehouse id) or `pdpSession` string, necessary to query shop detail),
you must add header `{ X-TKPD-Akamai : pdpGetLayout }` to your request. see `req_prod_detail_layout.json` for
sample query data