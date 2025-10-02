


from requests.exceptions import ConnectTimeout
from PIL import Image, UnidentifiedImageError
import os
import shutil
from PIL import Image as resi
import requests
import base64
import requests
from requests.auth import HTTPBasicAuth





# Your WordPress site credentials
site_url = "https://client.docstec.com/legsjet/"
site_urlapi = "https://client.docstec.com/legsjet/wp-json/wp/v2/flights"
username = "admin"
password = "RVOV OpAI EcSo FRfH Q4oK pZsC"  # watch for spacing





# API credentials
wourl = "https://client.docstec.com/legsjet/wp-json/wc/v3/products"
consumer_key = "ck_db93f7bba32824977339a2fedc954881e768a46f"
consumer_secret = "cs_cce84d064f99d167b724eb82ec9fa1ca8e933026"





def datapost(new_product):
    target_meta = {m["key"]: m["value"] for m in new_product["meta_data"]}
    response = requests.get(wourl, auth=HTTPBasicAuth(consumer_key, consumer_secret))
    if response.status_code == 200:
        products = response.json()

        duplicate_found = False
        for p in products:
            meta = {m["key"]: m["value"] for m in p.get("meta_data", [])}
            check_keys = [
                "departure", "arrival", "flight_date", "flight_time",
                "aircraft_type", "distance", "pax", "aoc", "ferry"
            ]
            if all(meta.get(k) == target_meta.get(k) for k in check_keys):
                duplicate_found = True
                return f"Duplicate found! Product already exists (ID: {p['id']})"

        if not duplicate_found:
            create = requests.post(
                wourl,
                auth=HTTPBasicAuth(consumer_key, consumer_secret),
                json=new_product
            )
            if create.status_code in [200, 201]:
                prod = create.json()
                return f"New Flight created: {prod['id']} - {prod['name']} - {prod['permalink']}"
            else:
                return f"Error creating product: {create.status_code} - {create.text}"

    else:
        return f"Error fetching products: {response.status_code} - {response.text}"




# Function to generate headers
def get_headers(user, pwd):
    credentials = f"{user}:{pwd}"
    token = base64.b64encode(credentials.encode()).decode("utf-8")
    return {
        "Authorization": f"Basic {token}",
        "Content-Type": "application/json"
    }



def headerss(wp_user, wp_pass):
    wp_credential = f'{wp_user}:{wp_pass}'
    wp_token = base64.b64encode(wp_credential.encode())
    wp_header = {'Authorization': f'Basic {wp_token.decode("utf-8")}'}
    return wp_header

xxx = {
        "title": "aircraft",
        "slug": "aircraft",
        "status": "publish",
        "featured_media": 77,  # optional media ID
        "meta": {
            "departure":"origin",
            "arrival": "destination",
            "date": "2025-07-09",
            "time": "",
            "price": "10",
            "aircraft_id": "aircraft",
            "distance": "",
            "pax": "1"
        },
    }

#
# def is_match(meta, data):
#     return all(meta.get(k) == v for k, v in data.items())  # Make GET request
#
#
# def datapost(data):
#     # API endpoint
#     alldata = "https://client.docstec.com/legsjet/wp-json/custom/v1/all-flights"
#     # Target meta fields to match
#     # Function to check if a flight meta matches target exactly
#     response = requests.get(alldata)
#
#     if response.status_code == 200:
#         flights = response.json()
#         matched = []
#
#
#         # Loop through each flight and check for exact match
#         for flight in flights:
#             if 'meta' in flight and is_match(flight['meta'], data["meta"]):
#                 matched.append(flight)
#
#         # Output
#         # print(matched)
#         if matched:
#             result = "Already posted"
#             # for m in matched:
#             #     print(m)
#         else:
#             response = requests.post(
#                 site_urlapi,
#                 headers=get_headers(username, password),
#                 json=data
#             )
#             print(response)
#             postdone_url = response.json()
#             result = postdone_url["link"]
#     else:
#         result = f"Failed to fetch data. Status code: {response.status_code}"
#
#     return result
#
#





def datapost1(data):
    response = requests.post(
        site_urlapi,
        headers=get_headers(username, password),
        json=data
    )

    postdone_url = response.json()
    return postdone_url


def headerss(wp_user, wp_pass):
    wp_credential = f'{wp_user}:{wp_pass}'
    wp_token = base64.b64encode(wp_credential.encode())
    wp_header = {'Authorization': f'Basic {wp_token.decode("utf-8")}'}
    return wp_header

def pexels(valid_urls, query):
    try:
        select_img = valid_urls
        response = requests.get(select_img, timeout=10) # increase timeout value as required
        # print(response)
        if response.status_code == 302:
            redirect_url = response.headers['Location']
            response = requests.get(redirect_url, timeout=10) # send new request to the redirect location
            print(response)
    except (IndexError, ConnectTimeout, requests.exceptions.RequestException) as e:
        a=(f"Error: {str(e)}")
        return None, None

    try:
        if not os.path.exists('img'):
            os.makedirs('img')
        if isinstance(response, str):
            raise ValueError("Response is not a requests.Response object.")
        else:
            with open('img/' + query + ".jpg", "wb") as local_file:
                local_file.write(response.content)
        image = resi.open('img/' + query + ".jpg")
        # print(image)
        image = image.convert("RGB")
        image.save('img/' + query + ".webp", "webp")
        header = headerss(username,password)
        url = f'{site_url}wp-json/wp/v2/media'
        image_file = open('img/' + query + ".webp", 'rb')
        payload = {'file': ('img/' + query + ".webp", image_file)}
        response = requests.post(url, headers=header, files=payload).json()
        wp_image_id = response.get('id')
        wp_image_ulr = response.get('guid').get('rendered')
        image_file.close()
    except UnidentifiedImageError:
        # print("Error: Unable to identify image file format.")
        wp_image_id = None
        wp_image_ulr = None
    except ValueError as e:
        t=(str(e))
        wp_image_id = None
        wp_image_ulr = None
    img_dir = 'img'
    shutil.rmtree(img_dir)
    return wp_image_id, wp_image_ulr

headers_aircharter = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36",
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "X-Requested-With": "XMLHttpRequest",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
}

def pexels_aircharter(valid_urls, query):
    try:
        select_img = valid_urls
        response = requests.get(select_img, headers=headers_aircharter, timeout=10,verify=False) # increase timeout value as required
        # print(response)
        if response.status_code == 302:
            redirect_url = response.headers['Location']
            response = requests.get(redirect_url, headers=headers_aircharter, timeout=10, verify=False) # send new request to the redirect location
            print(response)
    except (IndexError, ConnectTimeout, requests.exceptions.RequestException) as e:
        a=(f"Error: {str(e)}")
        return None, None

    try:
        if not os.path.exists('img'):
            os.makedirs('img')
        if isinstance(response, str):
            raise ValueError("Response is not a requests.Response object.")
        else:
            with open('img/' + query + ".jpg", "wb") as local_file:
                local_file.write(response.content)
        image = resi.open('img/' + query + ".jpg")
        # print(image)
        image = image.convert("RGB")
        image.save('img/' + query + ".webp", "webp")
        header = headerss(username,password)
        url = f'{site_url}wp-json/wp/v2/media'
        image_file = open('img/' + query + ".webp", 'rb')
        payload = {'file': ('img/' + query + ".webp", image_file)}
        response = requests.post(url, headers=header, files=payload).json()
        wp_image_id = response.get('id')
        wp_image_ulr = response.get('guid').get('rendered')
        image_file.close()
    except UnidentifiedImageError:
        # print("Error: Unable to identify image file format.")
        wp_image_id = None
        wp_image_ulr = None
    except ValueError as e:
        t=(str(e))
        wp_image_id = None
        wp_image_ulr = None
    img_dir = 'img'
    shutil.rmtree(img_dir)
    return wp_image_id, wp_image_ulr




# print(pexels_aircharter("https://privatejet.aircharter.com/aircharter/resizer?src=/aircharter-images/tails/ac6e880a-d92f-4aa9-b087-090b6830f83c.jpg", "df fsd sdf fds"))

