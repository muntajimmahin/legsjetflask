import requests
from datetime import datetime, timedelta
import json
# from main import aircraft
from wp import datapost
from wp import pexels_aircharter



url = "https://www.aircharter.com/wp-content/plugins/empty-legs/php/get_empty_legs.php"
params = {
    # "key": "da5a2f4d-5411-440e-b359-ab78424aec85",
    "controller": "trip/emptyleg",
    "action": "info",
    # "token": "13b02e080bf12bca53d60921e02a5440a439443c9718f13959484f13eb031546"
}


headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36",
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "X-Requested-With": "XMLHttpRequest",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
}
def run(stop_event=None):
    try:
        dt = datetime.now() + timedelta(days=1)
        start_date = f"{dt.month}/{dt.day}/{str(dt.year)[2:]}"
        data = {
            "startDate": start_date
        }
        response = requests.post(url, data=data, headers=headers, verify=False)
        # print("Status code:", response.status_code)
        content = response.json()["content"]
        for xcontent in content:
            if stop_event and stop_event.is_set():
                print("Scraper killed by user")
                return  # Exit safely


            # print(xcontent)
            # id = xcontent["Id"]
            # print(xcontent)
            # print(xcontent)

            from_iata = xcontent['atAirport'].split('-')[0]
            to_iata = xcontent['toAirport'].split('-')[0]

            # Convert date from 'MM/DD/YY' to 'M/D/YYYY'
            start_date_obj = datetime.strptime(xcontent['startDate'], '%m/%d/%y')
            formatted_date = f"{start_date_obj.month}/{start_date_obj.day}/{start_date_obj.year}"

            # Construct payload
            payload = {
                "emptyLegID": str(xcontent['Id']),
                "from0": from_iata,
                "to0": to_iata,
                "date0": formatted_date,
                "time0": "00:00",
                "pax": str(xcontent.get('pax', 1)),
                "numberLeg": "1",
                "currency": "usd",
                "catVals": "null",
                "AircraftTypes": "null",
                "fuelStop": "false"
            }

            # print(payload)
            url2 = "https://www.aircharter.com/wp-content/plugins/Booking_Engine/php/manage.php"

            response = requests.post(url2, params=params, data=payload, headers=headers, verify=False)

            all_info = response.json()


            displayName = all_info["displayName"].strip()
            aircraftName = all_info["aircraftName"].strip()
            baseAirport = all_info["baseAirport"].strip()
            fromAirport = all_info["fromAirport"].strip()
            endDate = all_info["endDate"]
            estimatedPrice = all_info["estimatedPrice"]
            pax = all_info["maxPax"]
            distance = all_info['costs']['legs'][0]['distance']
            total_distance_miles = f"{round(distance, 2)} miles"

            all_img_url = all_info["images"]
            exterior_image = next((img['src'] for img in all_img_url if img['type'] == 'Exterior'), None)
            img_url = f'https://privatejet.aircharter.com/aircharter/resizer?src={exterior_image}'
            img_id = pexels_aircharter(img_url, displayName)[1]
            # print(img_id)

            # datas = {
            #     "title": displayName,
            #     "slug": aircraftName,
            #     "status": "publish",
            #     "featured_media": img_id,
            #     "meta": {
            #         "departure": baseAirport,
            #         "arrival": fromAirport,
            #         "flight_date": str(endDate),
            #         "flight_time": "",
            #         "price": str(estimatedPrice),
            #         "aircraft_id": aircraftName,
            #         "distance": total_distance_miles,
            #         "pax": str(pax)
            #     },
            # }

            # print(datas)
            data = {
                "name": f"{baseAirport} to {fromAirport}",
                "slug": aircraftName,
                "status": "publish",
                "type": "simple",
                "regular_price": str(estimatedPrice),
                "price": str(estimatedPrice),
                "stock_status": "instock",

                "images": [
                    {"src": img_id},
                #     {"src": "https://client.docstec.com/legsjet/wp-content/uploads/2025/07/20240626-090828.jpg"},
                #     {
                #         "src": "https://client.docstec.com/legsjet/wp-content/uploads/2025/07/Dassault_Falcon_6X_EXTERIOR_1-scaled.png"}
                ],

                "meta_data": [
                    {"key": "departure", "value": baseAirport},
                    {"key": "arrival", "value": fromAirport},
                    {"key": "flight_date", "value": str(formatted_date)},
                    {"key": "flight_time", "value": ""},
                    {"key": "aircraft_type", "value": aircraftName},
                    {"key": "distance", "value": total_distance_miles},
                    {"key": "pax", "value": str(pax)},
                    {"key": "aoc", "value": ""},
                    {"key": "ferry", "value": ""}
                ]
            }
            post_data = datapost(data)
            print(post_data)
    except:
        pass
if __name__ == "__main__":
    run()

