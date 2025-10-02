import cloudscraper
from bs4 import BeautifulSoup
from wp import datapost, pexels
from urllib.parse import urlparse, parse_qs, unquote
import yfinance as yf
from datetime import datetime
import time

# Spoof browser
scraper = cloudscraper.create_scraper(browser={'custom': 'ScraperBot/1.0'})

# Currency converter
def get_conversion_rate(from_currency, to_currency):
    symbol = f"{from_currency}{to_currency}=X"
    ticker = yf.Ticker(symbol)
    return ticker.info['regularMarketPrice']

# 🛠 Main scraper function
def run(stop_event=None):
    for i in range(1, 50):
        if stop_event and stop_event.is_set():
            print("Scraper killed by user")
            return  # Exit safely
        try:
            url = f"https://www.flyvictor.com/en-gb/flights/{i}/"
            # print(f"Scraping: {url}")
            res = scraper.get(url)
            # print("Status Code:", res.status_code)

            soup = BeautifulSoup(res.text, "html.parser")
            main_div = soup.find('div', class_="EmptyLegsList_listContainer__dkO26")
            if not main_div:
                continue

            cards = main_div.find_all('div', class_="Card_wrapper__fFgb1")

            for card in cards:
                if stop_event and stop_event.is_set():
                    print("Scraper killed during inner loop")
                    return  # Exit safely

                departure_date = card.find('p', string=lambda text: text and "Jul" in text)
                if not departure_date:
                    departure_date = card.find('p', class_="Body1_body1__iRf1n")

                img_tag = card.find("img")
                image_url = img_tag.get("src") if img_tag else ""
                parsed = urlparse(image_url)
                query = parse_qs(parsed.query)
                encoded_image_url = query.get("url", [""])[0]
                decoded_image_url = unquote(encoded_image_url)

                departure_date_text = departure_date.text.strip() if departure_date else "N/A"
                departure_airport = card.find_all('h6', class_="H6_h6__FsQB1")[0].text.strip()
                arrival_airport = card.find_all('h6', class_="H6_h6__FsQB1")[1].text.strip()

                aircraft_info = card.find_all('p', class_="Body1_body1__iRf1n")
                aircraft_type = aircraft_info[0].text.strip() if len(aircraft_info) > 0 else "N/A"
                aircraft_category = aircraft_info[1].text.strip() if len(aircraft_info) > 1 else "N/A"

                capacity_label = card.find('p', string="Capacity:")
                capacity = capacity_label.find_next_sibling('p').text.strip() if capacity_label else "N/A"

                price_text = card.find('h4', class_="H4_h4__SVkgx")
                price = price_text.text.strip().replace("£", "").replace(",", "") if price_text else "0"

                try:
                    rate = get_conversion_rate("GBP", "USD")
                    usd_amount = float(rate) * float(price)
                    usd_amount = f"{usd_amount:.2f}"
                except:
                    usd_amount = "0.00"

                img_id = pexels(decoded_image_url, aircraft_type)[1]
                try:
                    parsed_date = datetime.strptime(departure_date_text, "%a %d %b %Y")
                    formatted_date = parsed_date.strftime("%Y-%m-%d")
                except:
                    formatted_date = ""

                # datas = {
                #     "title": aircraft_category.replace(",", ""),
                #     "slug": aircraft_category.replace(",", ""),
                #     "status": "publish",
                #     "featured_media": img_id,
                #     "meta": {
                #         "departure": departure_airport,
                #         "arrival": arrival_airport,
                #         "flight_date": formatted_date,
                #         "flight_time": "",
                #         "price": str(usd_amount),
                #         "aircraft_id": aircraft_category.replace(",", ""),
                #         "distance": "",
                #         "pax": capacity
                #     },
                # }

                data = {
                    "name": f"{departure_airport} to {arrival_airport}",
                    "slug": aircraft_category.replace(",", ""),
                    "status": "publish",
                    "type": "simple",
                    "regular_price": str(usd_amount),
                    "price": str(usd_amount),
                    "stock_status": "instock",

                    "images": [
                        {"src": img_id},
                        #     {"src": "https://client.docstec.com/legsjet/wp-content/uploads/2025/07/20240626-090828.jpg"},
                        #     {
                        #         "src": "https://client.docstec.com/legsjet/wp-content/uploads/2025/07/Dassault_Falcon_6X_EXTERIOR_1-scaled.png"}
                    ],

                    "meta_data": [
                        {"key": "departure", "value": departure_airport},
                        {"key": "arrival", "value": arrival_airport},
                        {"key": "flight_date", "value": str(formatted_date)},
                        {"key": "flight_time", "value": ""},
                        {"key": "aircraft_type", "value": aircraft_category.replace(",", ""),},
                        {"key": "distance", "value": ""},
                        {"key": "pax", "value": capacity},
                        {"key": "aoc", "value": ""},
                        {"key": "ferry", "value": ""}
                    ]
                }




                post_data = datapost(data)
                print(post_data)
        except Exception as e:
            print("Error:", e)

if __name__ == "__main__":
    run()







