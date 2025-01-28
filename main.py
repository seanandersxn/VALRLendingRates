import time
import hashlib
import hmac
from dotenv import load_dotenv
import os
import requests
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
import schedule

def configure():
    load_dotenv()

def sign_request(api_key_secret, timestamp, verb, path, body=""):
    payload = "{}{}{}{}".format(timestamp, verb.upper(), path, body)
    message = bytearray(payload, 'utf-8')
    signature = hmac.new(bytearray(api_key_secret, 'utf-8'), message, digestmod=hashlib.sha512).hexdigest()
    return signature

def fetch_and_upload_data():
    configure()
    api_key = os.getenv('api_key')
    api_key_secret = os.getenv('api_key_secret')
    influx_url = os.getenv('influx_url')
    influx_token = os.getenv('influx_token')
    influx_org = os.getenv('influx_org')
    influx_bucket = os.getenv('influx_bucket')

    timestamp = int(time.time() * 1000)
    signature = sign_request(api_key_secret, timestamp, 'GET', '/v1/loans/rates')
    url = "https://api.valr.com/v1/loans/rates"

    payload = {}
    headers = {
        'X-VALR-API-KEY': api_key,
        'X-VALR-SIGNATURE': signature,
        'X-VALR-TIMESTAMP': str(timestamp)
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    data = response.json()

    zar_data = next((item for item in data if item['currency'] == 'ZAR'), None)

    if zar_data:
        formatted_zar_data = {
            k: f"{float(v) * 24 * 365 * 100:.8f}" if k != 'currency' else v for k, v in zar_data.items()
        }
        print(formatted_zar_data)

        client = InfluxDBClient(url=influx_url, token=influx_token, org=influx_org)
        write_api = client.write_api(write_options=SYNCHRONOUS)

        point = Point("loan_rates") \
            .tag("currency", formatted_zar_data["currency"]) \
            .field("previousFundingRate", float(formatted_zar_data["previousFundingRate"])) \
            .field("estimatedNextRate", float(formatted_zar_data["estimatedNextRate"])) \
            .field("estimatedNextBorrowRate", float(formatted_zar_data["estimatedNextBorrowRate"])) \
            .time(time.time_ns())

        write_api.write(bucket=influx_bucket, org=influx_org, record=point)
        print("Data written to InfluxDB!")
    else:
        print("ZAR data not found.")

schedule.every().hour.at(":52").do(fetch_and_upload_data)

while True:
    schedule.run_pending()
    time.sleep(1)