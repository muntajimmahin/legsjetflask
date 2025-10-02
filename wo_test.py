# import requests
# from requests.auth import HTTPBasicAuth
#
# # API endpoint
# url = "https://client.docstec.com/legsjet/wp-json/wc/v3/products"
#
# # Your WooCommerce API credentials
# consumer_key = "ck_db93f7bba32824977339a2fedc954881e768a46f"
# consumer_secret = "cs_cce84d064f99d167b724eb82ec9fa1ca8e933026"
#
# # Send GET request
# response = requests.get(url, auth=HTTPBasicAuth(consumer_key, consumer_secret))
#
# # Check status
# if response.status_code == 200:
#     products = response.json()
#     print(products)
# #     for product in products:
#         print(product)
# #         print(f"{product['id']} - {product['name']} - {product['price']}")
# # else:
# #     print("Error:", response.status_code, response.text)
#
