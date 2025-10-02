# import requests
# from bs4 import BeautifulSoup
# from wp import pexels
# from wp import datapost
# from datetime import datetime, timedelta
#
# url = "https://privatelegs.com/search?page=1"
#
# headers = {
#     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36",
#     "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
#     "Accept-Encoding": "gzip, deflate, br, zstd",
#     "Accept-Language": "en-US,en;q=0.9,bn;q=0.8,fr;q=0.7",
#     "Cache-Control": "max-age=0",
#     "Connection": "keep-alive",
#     "Host": "privatelegs.com",
#     "Referer": "https://privatelegs.com/",
#     "Sec-Fetch-Dest": "document",
#     "Sec-Fetch-Mode": "navigate",
#     "Sec-Fetch-Site": "same-origin",
#     "Sec-Fetch-User": "?1",
#     "Upgrade-Insecure-Requests": "1",
#     "Sec-Ch-Ua": '"Google Chrome";v="137", "Chromium";v="137", "Not/A)Brand";v="24"',
#     "Sec-Ch-Ua-Mobile": "?0",
#     "Sec-Ch-Ua-Platform": '"Windows"',
#     "Cookie": "PHPSESSID=mbg03thi2eimentm6i8our22g3"  # Optional: only if needed
# }
#
# session = requests.Session()
# headers = {
#     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36",
#     "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
#     "Accept-Encoding": "gzip, deflate, br, zstd",
#     "Accept-Language": "en-US,en;q=0.9,bn;q=0.8,fr;q=0.7",
#     "Cache-Control": "max-age=0",
#     "Connection": "keep-alive",
#     "Host": "privatelegs.com",
#     "Referer": "https://privatelegs.com/",
#     "Sec-Fetch-Dest": "document",
#     "Sec-Fetch-Mode": "navigate",
#     "Sec-Fetch-Site": "same-origin",
#     "Sec-Fetch-User": "?1",
#     "Upgrade-Insecure-Requests": "1",
#     "Sec-Ch-Ua": '"Google Chrome";v="137", "Chromium";v="137", "Not/A)Brand";v="24"',
#     "Sec-Ch-Ua-Mobile": "?0",
#     "Sec-Ch-Ua-Platform": '"Windows"',
#
# }
#
# # Step 1: Get login page
# login_url = "https://privatelegs.com/login"
# resp = session.get(login_url, headers=headers)
# soup = BeautifulSoup(resp.text, "html.parser")
#
# # Step 2: Get CSRF token
# csrf_input = soup.find("input", {"name": "_csrf_token"})
# csrf_token = csrf_input["value"]
#
# payload = {
#     "_username": "folely@fxzig.com",
#     "_password": "zHSRPA3Tg7MdmKW",
#     "_csrf_token": csrf_token
# }
#
# login_resp = session.post(login_url, data=payload, headers=headers)
# cookie_string = '; '.join([f"{cookie.name}={cookie.value}" for cookie in session.cookies])
# headers2 = {
#     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36",
#     "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
#     "Accept-Encoding": "gzip, deflate, br, zstd",
#     "Accept-Language": "en-US,en;q=0.9,bn;q=0.8,fr;q=0.7",
#     "Cache-Control": "max-age=0",
#     "Connection": "keep-alive",
#     "Host": "privatelegs.com",
#     "Referer": "https://privatelegs.com/",
#     "Sec-Fetch-Dest": "document",
#     "Sec-Fetch-Mode": "navigate",
#     "Sec-Fetch-Site": "same-origin",
#     "Sec-Fetch-User": "?1",
#     "Upgrade-Insecure-Requests": "1",
#     "Sec-Ch-Ua": '"Google Chrome";v="137", "Chromium";v="137", "Not/A)Brand";v="24"',
#     "Sec-Ch-Ua-Mobile": "?0",
#     "Sec-Ch-Ua-Platform": '"Windows"',
#     "cookie": cookie_string
# }
# def convert_to_iso(date_str):
#     partial_date = datetime.strptime(date_str, "%a, %b %d")
#     today = datetime.today()
#     candidate_date = partial_date.replace(year=today.year)
#     if candidate_date < today:
#         candidate_date = candidate_date.replace(year=today.year)
#
#     return candidate_date.strftime("%Y-%m-%d")
#
# def run(stop_event=None):
#     for page in range(1, 51):
#             url = f"https://privatelegs.com/search?page={page}"
#             print(f"Scraping Page: {page} → {url}")
#
#             response = requests.get(url, headers=headers2)
#             print(response)
#             soup = BeautifulSoup(response.text, "html.parser")
#             print(
#                 soup
#             )
#
#             booking_items = soup.find_all("div", class_="booking-list-item", attrs={"data-controller": "flight-details"})
#             print(booking_items)
#
#             if not booking_items:
#                 print(f"No results on page {page}")
#                 continue
#             for xbooking_items in booking_items:
#                 if stop_event and stop_event.is_set():
#                     print("Scraper killed by user")
#                     return  # Exit safely
#                 flight_detail_info = xbooking_items.find('div', class_='flight-airway').find("span").text.replace(
#                     "Aircraft:", "").strip()
#                 print(flight_detail_info)
#                 imagurl = xbooking_items.find('div', class_='flight-logo').find('img')['src']
#                 flight_price = xbooking_items.find('div', class_='flight-price').find("h4").text
#                 flight_info = xbooking_items.find('ul', class_='flight-info mt-2')
#                 li_items = flight_info.find_all('li')
#                 date = li_items[0].text.strip()
#                 route_li = li_items[2]
#                 route_text = list(route_li.stripped_strings)
#                 route_title = route_li['title']
#                 departure_code, arrival_code = route_text[0], route_text[1]
#                 departure_city, arrival_city = route_title.split(' to ')
#
#                 seat_span = li_items[3].find('span')
#                 available_seats = ''.join(filter(str.isdigit, seat_span.text))
#                 formatted_date = convert_to_iso(date)
#
#                 print("Aircraft:", flight_detail_info)
#                 # print("Flight Price:", flight_price)
#                 # print("Image URL:", imagurl)
#                 # print("Date:", date)
#                 #
#                 # print("Departure Code:", departure_code)
#                 # print("Arrival Code:", arrival_code)
#                 # print("Departure City:", departure_city)
#                 # print("Arrival City:", arrival_city)
#                 # print("Available Seats:", available_seats)
#                 # print(".................")
#                 #
#                 #
#                 departure = f"{departure_city} {departure_code}"
#                 arrival = f"{arrival_city} {arrival_code}"
#                 img_id = pexels(imagurl,flight_detail_info)[1]
#
#                 # ssss = {
#                 #     "title": flight_detail_info,
#                 #     "slug": flight_detail_info,
#                 #     "status": "publish",
#                 #     "featured_media": img_id,  # optional media ID
#                 #     "meta": {
#                 #         "departure": departure,
#                 #         "arrival": arrival,
#                 #         "flight_date": str(formatted_date),
#                 #         "flight_time": "",
#                 #         "price": str(flight_price),
#                 #         "aircraft_id": flight_detail_info,
#                 #         "distance": "",
#                 #         "pax": str(available_seats)
#                 #     },
#                 # }
#
#                 data = {
#                     "name": f"{departure} to {arrival}",
#                     "slug": flight_detail_info.replace(" ", "-").lower(),
#                     "status": "publish",
#                     "type": "simple",
#                     "regular_price": str(flight_price),
#                     "price": str(flight_price),
#                     "stock_status": "instock",
#
#                     "images": [
#                         {"src": img_id},
#
#                     ],
#
#                     "meta_data": [
#                         {"key": "departure", "value": departure},
#                         {"key": "arrival", "value": arrival},
#                         {"key": "flight_date", "value": str(formatted_date)},
#                         {"key": "flight_time", "value": ""},
#                         {"key": "aircraft_type", "value": flight_detail_info},
#                         {"key": "distance", "value": ""},
#                         {"key": "pax", "value": str(available_seats)},
#                         {"key": "aoc", "value": ""},
#                         {"key": "ferry", "value": ""}
#                     ]
#                 }
#
#                 post_data = datapost(data)
#                 print(post_data)
#
# if __name__ == "__main__":
#     run()
#
#





import requests
from bs4 import BeautifulSoup
from datetime import datetime
from wp import pexels, datapost  # Assuming these are your custom functions

MAX_PAGES = 50
URL = "https://privatelegs.com/search/load-more"

HEADERS = {
    "Accept": "*/*",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "en-US,en;q=0.9,bn;q=0.8,el;q=0.7",
    "Cache-Control": "no-cache, private",
    "Connection": "keep-alive",
    "Host": "privatelegs.com",
    "Referer": "https://privatelegs.com/search?page=1",
    "Sec-Ch-Ua": '"Not;A=Brand";v="99", "Google Chrome";v="139", "Chromium";v="139"',
    "Sec-Ch-Ua-Mobile": "?0",
    "Sec-Ch-Ua-Platform": '"Windows"',
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36"
}

def convert_to_iso(date_str):
    """Convert partial date like 'Thu, Sep 05' to ISO YYYY-MM-DD format."""
    partial_date = datetime.strptime(date_str, "%a, %b %d")
    today = datetime.today()
    candidate_date = partial_date.replace(year=today.year)
    if candidate_date < today:
        candidate_date = candidate_date.replace(year=today.year + 1)
    return candidate_date.strftime("%Y-%m-%d")


def run(stop_event=None):
    for page in range(1, MAX_PAGES + 1):
        params = {
            "flight_search_form[dateRange]": "",
            "flight_search_form[departureAirport]": "",
            "flight_search_form[arrivalAirport]": "",
            "flight_search_form[aircraft]": "",
            "page": page
        }

        resp = requests.get(URL, params=params, headers=HEADERS)
        resp.raise_for_status()
        json_data = resp.json()
        html = json_data.get("html", "")
        if not html.strip():
            print(f"No more flights on page {page}. Stopping.")
            break

        soup = BeautifulSoup(html, "html.parser")
        flight_cards = soup.select(".flight-card")
        if not flight_cards:
            print(f"No flights found on page {page}.")
            continue

        for card in flight_cards:
            try:
                if stop_event and stop_event.is_set():
                    print("Scraper stopped by user.")
                    return

                # Aircraft + Image
                img_tag = card.select_one(".flight-image img")
                aircraft = img_tag.get("alt") if img_tag else "N/A"
                img_url = img_tag.get("src") if img_tag else ""

                # Flight date
                date_badge = card.select_one(".flight-date-badge")
                date = date_badge.get_text(strip=True) if date_badge else ""

                # Flight time
                time_tag = card.select_one(".flight-time i")
                flight_time = time_tag.get("title", "").strip() if time_tag else ""

                # Route
                route_tags = card.select(".flight-route h4")
                departure_city = route_tags[0].get_text(strip=True) if len(route_tags) > 0 else ""
                arrival_city = route_tags[1].get_text(strip=True) if len(route_tags) > 1 else ""

                # Passengers
                pax_tag = card.select_one(".flight-passengers span")
                passengers = pax_tag.get_text(strip=True) if pax_tag else ""

                # Price
                price_tag = card.select_one(".price-display h3")
                price = price_tag.get_text(strip=True) if price_tag else "0"

                # Flight link
                link_tag = card.select_one(".flight-price-section a")
                link = f"https://privatelegs.com{link_tag['href']}" if link_tag else ""

                # Convert date to ISO
                formatted_date = convert_to_iso(date) if date else ""

                # Download image via pexels (custom function)
                img_id = pexels(img_url, aircraft)[1] if img_url else None

                # Prepare data for WordPress
                data = {
                    "name": f"{departure_city} to {arrival_city}",
                    "slug": aircraft.replace(" ", "-").lower(),
                    "status": "publish",
                    "type": "simple",
                    "regular_price": str(price),
                    "price": str(price),
                    "stock_status": "instock",
                    "images": [{"src": img_id}] if img_id else [],
                    "meta_data": [
                        {"key": "departure", "value": departure_city},
                        {"key": "arrival", "value": arrival_city},
                        {"key": "flight_date", "value": formatted_date},
                        {"key": "flight_time", "value": flight_time},
                        {"key": "aircraft_type", "value": aircraft},
                        {"key": "pax", "value": passengers},
                        {"key": "link", "value": link}
                    ]
                }

                # Post data to WordPress
                post_response = datapost(data)
                print(post_response)
            except:
                pass


if __name__ == "__main__":
    run()




