import requests
from bs4 import BeautifulSoup
import brotli
import yfinance as yf
from datetime import datetime
from wp import datapost
def convert_date(date_str):
    if date_str.lower() == "today":
        return datetime.today().strftime("%Y-%m-%d")
    else:
        # Handles formats like "5 July 2025"
        date_obj = datetime.strptime(date_str, "%d %B %Y")
        return date_obj.strftime("%Y-%m-%d")
def get_conversion_rate(from_currency, to_currency):
    symbol = f"{from_currency}{to_currency}=X"
    ticker = yf.Ticker(symbol)
    return ticker.info['regularMarketPrice']
# Test examples

url = "https://www.globeair.com/empty-leg-flights"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Accept-Language": "en-US,en;q=0.9,bn;q=0.8,el;q=0.7",
    "Cache-Control": "max-age=0",
    "Referer": "https://www.globeair.com/en/private-jet/empty-leg-flights",
    "Upgrade-Insecure-Requests": "1",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "same-origin",
    "Sec-Fetch-User": "?1",
    "Sec-Ch-Ua": '"Not)A;Brand";v="8", "Chromium";v="138", "Google Chrome";v="138"',
    "Sec-Ch-Ua-Mobile": "?0",
    "Sec-Ch-Ua-Platform": '"Windows"',
}

response = requests.get(url, headers=headers)

# print(f"Status Code: {response.status_code}")
# print(f"Content-Encoding: {response.headers.get('Content-Encoding')}")

try:
    if response.headers.get('Content-Encoding') == 'br':
        decoded_html = brotli.decompress(response.content).decode('utf-8')
    else:
        decoded_html = response.text
except Exception as e:
    # print(f"Decompression error: {e}")
    # fallback to text anyway
    decoded_html = response.text

soup = BeautifulSoup(decoded_html, "html.parser")
all_info = soup.find_all("div", class_="column is-4-desktop is-3-tablet is-12-mobile has-text-centered has-text-centered-mobile")
booking_urls = []
seen_urls = set()

for x_allinfo in all_info:
    booking_btn = x_allinfo.find("a", class_="button")

    if booking_btn and "href" in booking_btn.attrs:
        booking_url = booking_btn["href"]

        if booking_url not in seen_urls:
            seen_urls.add(booking_url)
            booking_urls.append(booking_url)

# Output the list
# print(booking_urls)

import requests
from bs4 import BeautifulSoup

# Start a session to maintain cookies
session = requests.Session()
headers1 = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "en-US,en;q=0.9",
    "Referer": "https://fly.globeair.com/en/users/login",
    "Origin": "https://fly.globeair.com",
    "Content-Type": "application/x-www-form-urlencoded",
    "Connection": "keep-alive",
}

# Define the login URL
login_url = "https://fly.globeair.com/en/users/login"

# Step 1: GET the login page to grab any required cookies (e.g. PHPSESSID)
get_response = session.get(login_url)
soup = BeautifulSoup(get_response.text, "html.parser")

# Step 2: Prepare the form data
payload = {
    "auth_userid": "cyqabi@fxzig.com",  # Replace with your email
    "auth_password": "sdfsdfsdf1313#@4qw5",         # Replace with your password
    "auth_rememberme": "1"
}
session.post(login_url, data=payload, headers=headers1)
cookie_string = '; '.join([f"{cookie.name}={cookie.value}" for cookie in session.cookies])
# print(cookie_string)

def run(stop_event=None):
    for xurl in booking_urls:
        # print(xurl)
        if stop_event and stop_event.is_set():
            print("Scraper killed by user")
            return  # Exit safely
        try:
            url = xurl
            # print(url)
            headers2 = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
                "Accept-Encoding": "gzip, deflate, br, zstd",
                "Accept-Language": "en-US,en;q=0.9,bn;q=0.8,fr;q=0.7",
                "Cache-Control": "max-age=0",
                "If-Modified-Since": "Mon, 10 Oct 2022 22:01:57 GMT",
                "Upgrade-Insecure-Requests": "1",
                "Sec-Fetch-Dest": "document",
                "Sec-Fetch-Mode": "navigate",
                "Sec-Fetch-Site": "none",
                "Sec-Fetch-User": "?1",
                "Sec-CH-UA": '"Not)A;Brand";v="8", "Chromium";v="138", "Google Chrome";v="138"',
                "Sec-CH-UA-Mobile": "?0",
                "Sec-CH-UA-Platform": '"Windows"',
                "cookie": f"{cookie_string};",

            }

            redirect_response = requests.get(url, headers=headers2, allow_redirects=False)
            redirect_url = redirect_response.headers.get("Location")
            final_url = redirect_url+"?pax=1"
            redirect_response1 = requests.get(final_url, headers=headers2, allow_redirects=False)
            redirect_url_main = redirect_response1.headers.get("Location")
            # print("Redirected to:", redirect_url_main)

            redirect_response_mian = requests.get(redirect_url_main, headers=headers2)
            # print(redirect_response_mian.text)

            soup = BeautifulSoup(redirect_response_mian.text, "html.parser")
            Jet_name = soup.find("h5").find("strong").text
            # print(Jet_name)
            price_tag = soup.select_one("div.text-primary > span.f3x.font-weight-bold").text.replace("€","").replace(",", "")

            try:
                rate = get_conversion_rate("GBP", "USD")
                usd_amount = float(rate) * float(price_tag)
                usd_amount = f"{usd_amount:.2f}"
            except:
                usd_amount = "0.00"
            # print(Jet_name)
            flight_info = soup.find('div', class_='row light-grey p-4 mb-4')
            departure = flight_info.find('div', class_='col-sm-5 text-center')
            # print(flight_info)

            departure_block = flight_info.select_one(".col-sm-5.text-center")
            departure_airport = departure_block.select_one(".f2x strong").text.strip()
            departure_code = departure_block.select_one(".f2x").find_all("strong")[1].text.strip()
            departure_date_time = departure_block.select_one(".m10")
            departure_date = departure_date_time.find_all("strong")[0].text.strip()
            departure_time = departure_date_time.find_all("strong")[1].text.strip()

            # Arrival details
            arrival_block = soup.select(".col-sm-5.text-center")[1]
            arrival_airport = arrival_block.select_one(".f2x strong").text.strip()
            arrival_code = arrival_block.select_one(".f2x").find_all("strong")[1].text.strip()
            arrival_time = arrival_block.select_one(".m10 strong").text.strip()

            # Final result
            departure = f"{departure_airport} {departure_code})"
            arrival = f"{arrival_airport} {arrival_code}"
            departure_date = convert_date(departure_date)

            # date_obj = datetime.strptime(departure_date, "%d %B %Y")
            # formatted_date = date_obj.strftime("%Y-%m-%d")
            #
            # print(formatted_date)

            # print(f"  Time: {departure_time}")
            # print(f"  Time: {arrival_time}")
            # # image_url = get_wikipedia_image('Cessna Citation')
            # # print("Image URL:", image_url)
            # print(Jet_name)

            data = {
                "title": Jet_name,
                "slug": Jet_name,
                "status": "publish",
                "featured_media": None,  # optional media ID
                "meta": {
                    "departure": departure,
                    "arrival": arrival,
                    "flight_date": str(departure_date),
                    "flight_time": "",
                    "price": str(usd_amount),
                    "aircraft_id": Jet_name,
                    "distance": "",
                    "pax": str(1)
                },
            }
            # print(data)
            post_data = datapost(data)
            print(post_data)
        except:
            pass

if __name__ == "__main__":
    run()



