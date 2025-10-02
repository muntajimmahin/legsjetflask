import imaplib
import email
from email import policy
import os
import base64
import pandas as pd
import requests
from datetime import datetime, timedelta
import json
# from main import aircraft
from wp import datapost

def run(stop_event=None):
    M = imaplib.IMAP4_SSL('mail.infomaniak.com', 993)
    M.login('flights@jetyourway.com', '80UA/9#W0D.apt')
    M.select('INBOX')
    # Search all emails
    typ, data = M.search(None, 'ALL')
    # Folder to save attachments
    save_folder = "attachments"
    os.makedirs(save_folder, exist_ok=True)
    for num in data[0].split():
        typ, msg_data = M.fetch(num, '(RFC822)')
        raw_email = msg_data[0][1]

        # Parse email
        msg = email.message_from_bytes(raw_email, policy=policy.default)
        # print(msg)
        # print("..............................................")

        # Loop through email parts
        for part in msg.iter_attachments():
            filename = part.get_filename()
            if filename:
                # Only save CSV or XLSX
                if filename.endswith(('.csv', '.xlsx')):
                    filepath = os.path.join(save_folder, filename)
                    with open(filepath, 'wb') as f:
                        f.write(part.get_payload(decode=True))
                    # print(f"Saved: {filepath}")
                    print("Wait Start Inbox mail screping                                   ")

    M.logout()

    file_path = "attachments/Empty legs report - Legs Jet_flights.csv"
    if os.path.exists(file_path):
        # print("yes")
        file_path = "attachments/Empty legs report - Legs Jet_flights.csv"
        df = pd.read_csv(file_path)
        for index, row in df.iterrows():
            if stop_event and stop_event.is_set():
                print("Scraper killed by user")
                return  # Exit safely
            # Extract fields
            departure = row['ADEP ICAO [Plan]']
            arrival = row['ADES ICAO [Plan]']
            formatted_date = row['Date ADEP [Plan][LT]']
            available_seats = row['PAX Capacity']
            flight_price = ""  # <-- no price in CSV, can set manually or leave blank

            # Example (if no image ID available)
            img_id = None
            flight_detail_info = f"{departure} to {arrival}"


            # datas= {
            #     "title": flight_detail_info,
            #     "slug": flight_detail_info.replace(" ", "-").lower(),
            #     "status": "publish",
            #     "featured_media": img_id,  # optional
            #     "meta": {
            #         "departure": departure,
            #         "arrival": arrival,
            #         "flight_date": str(formatted_date),
            #         "flight_time": row['Block time [Plan]'],
            #         "price": str(flight_price),
            #         "aircraft_id": row['Aircraft type'],
            #         "distance": str(row['Distance [Plan][km]']),
            #         "pax": str(available_seats)
            #     },
            # }

            data = {
                "name": flight_detail_info,
                "slug": flight_detail_info.replace(" ", "-").lower(),
                "status": "publish",
                "type": "simple",
                "regular_price": str(flight_price),
                "price": str(flight_price),
                "stock_status": "instock",

                # "images": [
                #     {"src": "https://client.docstec.com/legsjet/wp-content/uploads/2025/07/foto_1.jpg"},
                #     {"src": "https://client.docstec.com/legsjet/wp-content/uploads/2025/07/20240626-090828.jpg"},
                #     {
                #         "src": "https://client.docstec.com/legsjet/wp-content/uploads/2025/07/Dassault_Falcon_6X_EXTERIOR_1-scaled.png"}
                # ],


                "meta_data": [
                    {"key": "departure", "value": departure},
                    {"key": "arrival", "value": arrival},
                    {"key": "flight_date", "value": str(formatted_date)},
                    {"key": "flight_time", "value": str(row['Block time [Plan]'])},
                    {"key": "aircraft_type", "value": row['Aircraft type']},
                    {"key": "distance", "value": str(row['Distance [Plan][km]'])},
                    {"key": "pax", "value": str(available_seats)},
                    {"key": "aoc", "value": row['AOC']},
                    {"key": "ferry", "value": row['Ferry']}
                ]
            }

            post_data = datapost(data)
            print(post_data)
    else:
        print("no")





