import requests
from datetime import datetime, timezone
from wp import pexels
from wp import datapost
# Setup


def run(stop_event=None):
    offset = 0
    limit = 8
    total_items = 10
    all_data = []
    base_url = "https://operators-dashboard.bubbleapps.io/api/1.1/obj/f-emptylegs"
    current_time = datetime.utcnow().isoformat()
    params = {
        "constraints": f'[{{"key":"date_date","constraint_type":"greater than","value":"{current_time}"}}]',
        "sort_by": "date_date",
        "sort_order": "desc",
        "limit": limit,
        "cursor": offset
    }

    def fetch_data(offset):
        params["cursor"] = offset
        try:
            response = requests.get(base_url, params=params)
            response.raise_for_status()
            return response.json()["response"]["results"]
        except Exception as e:
            print("Error fetching data:", e)
            return []
    # Pagination loop
    while offset < total_items:
        # print(f"Fetching offset: {offset}")
        results = fetch_data(offset)
        if not results:
            break
        for item in results:
            try:
                date_date = item["date_date"]
                dt = datetime.strptime(date_date, "%Y-%m-%dT%H:%M:%S.000Z").replace(tzinfo=timezone.utc)
                timestamp_ms = int(dt.timestamp() * 1000)

                all_data.append({
                    "from airport id": item["from_airport_custom_airport"],
                    "to airport id": item["to_airport_custom_airport"],
                    "App_Out_Date_As_Text": dt.strftime("%Y-%m-%d"),
                    "date": timestamp_ms,
                    "date_as_text": dt.strftime("%Y-%m-%d"),
                    "time_as_text": dt.strftime("%H:%M:%S"),
                    "aircraft_description_text": item["aircraft_description_text"],
                    "pax": "1",

                    "from_text": item["from_text"],
                    "to_airport_fixed_address_geographic_address": item["to_airport_fixed_address_geographic_address"],
                    "aircraftimage_image": item["aircraftimage_image"],

                })
            except Exception as parse_err:
                pass

        offset += limit

    # print(all_data)
    datas = all_data
    for all_data_xxx in datas:
        if stop_event and stop_event.is_set():
            print("Scraper killed by user")
            return  # Exit safely
        # print(all_data_xxx)

        url_webflow_one_way_flight = "https://operators-dashboard.bubbleapps.io/api/1.1/wf/webflow_one_way_flight"
        headers = {
            "Content-Type": "application/json",
            "Origin": "https://jettly.com",
            "Referer": "https://jettly.com/",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36",
            "Accept": "*/*"
        }

        payload = all_data_xxx
        airname = payload["aircraft_description_text"]
        response = requests.post(url_webflow_one_way_flight, headers=headers, json=payload)
        webflow_one_way_flight = response.json()["response"]
        flightrequestid = webflow_one_way_flight["flightrequest"]
        longest_flight_leg = webflow_one_way_flight["longest_flight_leg"]
        total_distance = webflow_one_way_flight["total_distance"]
        flight_legs = webflow_one_way_flight["flight_legs"]
        # print(longest_flight_leg)
        filtered_aircrafts = []
        for i in range(1, 11):
            key = f"aircraft_set_{i}"
            aircraft_list = webflow_one_way_flight.get(key, [])
            for aircraft in aircraft_list:
                if isinstance(aircraft, dict) and aircraft.get("description_text") == airname:
                    filtered_aircrafts.append(aircraft)
        if filtered_aircrafts:
            filtered_aircrafts[0]["flightrequest"] = flightrequestid
            filtered_aircrafts[0]["longest_flight_leg"] = longest_flight_leg
            filtered_aircrafts[0]["total_distance"] = total_distance
            filtered_aircrafts[0]["flight_legs"] = flight_legs
            all_flight_data = filtered_aircrafts[0]
            # print(all_flight_data)
            url_book = "https://operators-dashboard.bubbleapps.io/api/1.1/wf/book_now_button"
            headers = {
                "Authorization": "Bearer bus|1751724939718x903691032710047400|1751724939765x876068256823087400",
                # "Content-Type": "application/json",
                "Accept": "*/*",
                "Origin": "https://jettly.com",
                # You can add other headers if needed
            }
            payload = {
                "flightrequestid": all_flight_data["flightrequest"],
                "type": "market",
                "aircraftid": all_flight_data["_id"],  # _id
                "fare_class": "Value",
                "catering": "No",
                "groundtransfers": "No",
                "de_icinginsurance": "No",
                "crowdsource": "Yes",
                "way": "one way",
            }
            response = requests.post(url_book, headers=headers, json=payload)
            alldatast = response.json()
            alldatast["all_flight_data"] = all_flight_data
            data = alldatast
            try:
                flight = data['response']['flightlegs'][0]
                aircraft = data['all_flight_data']
                departure = f"{flight['mobile_app_from_airport_name_short_text']} ({flight['mobile_app_from_airport_faa_code_text']} / {flight['mobile_app_from_airport_icao_code_text']})"
                arrival = f"{flight['mobile_app_to_airport_name_short_text']} ({flight['mobile_app_to_airport_faa_code_text']})"
                date = flight['date_as_text1_text']
                aircraft_name = aircraft['description_text']
                distance = round(flight['total_distance__statute_m__number'], 2)
                pax = data['all_flight_data']['pax_number']
                image_url = f"https:{aircraft['interior_image1_image']}" if aircraft['interior_image1_image'].startswith(
                    "//") else \
                    aircraft['interior_image1_image']
                total_price = round(data['response']['total_price'], 2)
                # print("...................................")
                # print("✈️ Flight Summary")
                # print(f"Departure: {departure}")
                # print(f"Arrival: {arrival}")
                # print(f"Date: {date}")
                # print(f"Aircraft Name: {aircraft_name}")
                # print(f"Distance: {distance} miles")
                # print(f"Pax: {pax}")
                # print(f"Image URL: {image_url}")
                # print(f"Total Price: ${total_price}")
                try:
                    img_id = pexels(image_url,aircraft_name)[1]
                except:
                    img_id = None

                # datas = {
                #     "title": aircraft_name,
                #     "slug": aircraft_name,
                #     "status": "publish",
                #     "featured_media": img_id,  # optional media ID
                #     "meta": {
                #         "departure": departure,
                #         "arrival": arrival,
                #         "flight_date": str(date),
                #         "flight_time": "",
                #         "price": str(total_price),
                #         "aircraft_id": aircraft_name,
                #         "distance": str(distance),
                #         "pax": str(pax)
                #     },
                # }

                data = {
                    "name": f"{departure} to {arrival}",
                    "slug": aircraft_name,
                    "status": "publish",
                    "type": "simple",
                    "regular_price": str(total_price),
                    "price": str(total_price),
                    "stock_status": "instock",

                    "images": [
                        {"src": img_id},
                        #     {"src": "https://client.docstec.com/legsjet/wp-content/uploads/2025/07/20240626-090828.jpg"},
                        #     {
                        #         "src": "https://client.docstec.com/legsjet/wp-content/uploads/2025/07/Dassault_Falcon_6X_EXTERIOR_1-scaled.png"}
                    ],

                    "meta_data": [
                        {"key": "departure", "value": departure},
                        {"key": "arrival", "value": arrival},
                        {"key": "flight_date", "value": str(date)},
                        {"key": "flight_time", "value": ""},
                        {"key": "aircraft_type", "value": aircraft_name},
                        {"key": "distance", "value": str(distance)},
                        {"key": "pax", "value": str(pax)},
                        {"key": "aoc", "value": ""},
                        {"key": "ferry", "value": ""}
                    ]
                }



                post_data = datapost(data)
                print(post_data)
            except:
                pass
        else:
            pass

if __name__ == "__main__":
    run()





