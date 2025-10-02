# "aircraft_id": row['Aircraft type'],
#
# data = {
#     "title": flight_detail_info,
#     "slug": flight_detail_info.replace(" ", "-").lower(),
#     "status": "publish",
#     "featured_media": img_id,  # optional
#     "price": str(flight_price),
#
#     "meta_data": {
#
#         "key": "departure",
#         "value": "Dhaka"
#
#                  "departure": departure,
# "arrival": arrival,
# "flight_date": str(formatted_date),
# "flight_time": row['Block time [Plan]'],
# "distance": str(row['Distance [Plan][km]']),
# "pax": str(available_seats),
# "aoc": AOC,
# "ferry": ferry,
#
# },
#
# }
#
#
import requests
from requests.auth import HTTPBasicAuth

# API endpoint
url = "https://client.docstec.com/legsjet/wp-json/wc/v3/products"

# WooCommerce API credentials
consumer_key = "ck_db93f7bba32824977339a2fedc954881e768a46f"
consumer_secret = "cs_cce84d064f99d167b724eb82ec9fa1ca8e933026"


def is_match(meta, data):
    return all(meta.get(k) == v for k, v in data.items())  # Make GET request


def datapost(data):
    # API endpoint
    alldata = "https://client.docstec.com/legsjet/wp-json/wc/v3/products"
    # Target meta fields to match
    # Function to check if a flight meta matches target exactly
    response = requests.get(alldata)

    if response.status_code == 200:
        flights = response.json()
        matched = []


        # Loop through each flight and check for exact match
        for flight in flights:
            if 'meta' in flight and is_match(flight['meta'], data["meta"]):
                matched.append(flight)

        # Output
        # print(matched)
        if matched:
            result = "Already posted"
            # for m in matched:
            #     print(m)
        else:
            response = requests.post(
                site_urlapi,
                headers=get_headers(username, password),
                json=data
            )
            print(response)
            postdone_url = response.json()
            result = postdone_url["link"]
    else:
        result = f"Failed to fetch data. Status code: {response.status_code}"

    return result













# Product data


data = {
    "name": "EPWA to DPWA",
    "slug": "epwa-to-dpwa",
    "status": "publish",
    "type": "simple",
    "regular_price": "100.00",
    "price": "100.00",
    "stock_status": "instock",
    "images": [
        {"src": "https://client.docstec.com/legsjet/wp-content/uploads/2025/07/foto_1.jpg"},
        {"src": "https://client.docstec.com/legsjet/wp-content/uploads/2025/07/20240626-090828.jpg"},
        {"src": "https://client.docstec.com/legsjet/wp-content/uploads/2025/07/Dassault_Falcon_6X_EXTERIOR_1-scaled.png"}
    ],
    "meta_data": [
        {"key": "departure", "value": "EPWA"},
        {"key": "arrival", "value": "DPWA"},
        {"key": "flight_date", "value": "2025-08-14"},
        {"key": "flight_time", "value": "04:09"},
        {"key": "aircraft_type", "value": "F900-Mystere"},
        {"key": "distance", "value": "6898"},
        {"key": "pax", "value": "100"},
        {"key": "aoc", "value": "1MAN"},
        {"key": "ferry", "value": "Yes"}
    ]
}

# Send POST request
response = requests.post(url, auth=HTTPBasicAuth(consumer_key, consumer_secret), json=data)

# Check response
if response.status_code in [200, 201]:
    product = response.json()
    print("✅ Product created successfully!")
    print(f"ID: {product['id']} | Name: {product['name']} | Price: {product['price']}")
else:
    print("❌ Error:", response.status_code, response.text)


