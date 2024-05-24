# Purpose
Port of my original traderJS module from 2 years ago to Python. Python is a more utilitarian language when it comes to automation of trading, so this module will allow for users to utilize this language with their Tradovate accounts.
# Setup
1) Create a Tradovate account and register an app
2) Create accessToken.json (leave blank or if there's an error, setup as {"accessToken":""})
3) Create a .env (fill it in with all your account details)
4) Run the file calling the refresh access token function in order to obtain an access token. This is how you will authenticate sending orders and performing core account actions.
5) Place orders and call the refres access token function in a loop in order to ensure that it never expires
6) Get rich? I don't know - up to you.
# Code
```python
import datetime
import requests
import json
import dotenv
import os

# Toggle between sending requests to the live or demo environment
# I would recommend using the demo environment to test your code before going live
# WARNING: DO NOT SWITCH TO MD - THIS WILL BREAK EVERYTHING
# MD IS MARKET DATA AND DOES NOT ALLOW FOR ORDER PLACEMENT OR ACCOUNT AUTHENTICATION

# version = "live"
version = "demo"

dotenv.load_dotenv()

# These are the environment variables that you need to set in your .env file

name = os.getenv('TRADOVATE_NAME')
password = os.getenv('TRADOVATE_PASSWORD')
app_id = os.getenv('TRADOVATE_APP_ID')
app_version = os.getenv('TRADOVATE_APP_VERSION')
cid = os.getenv('TRADOVATE_CID')
sec = os.getenv('TRADOVATE_SEC')
device_id = os.getenv('TRADOVATE_DEVICE_ID')

# This function will place an order for you

def place_order(symbol, order_action, quantity, account_spec, account_id):
    with open('./accessToken.json') as f:
        access_token = json.load(f)['accessToken']

    initial = {
        "accountSpec": account_spec,
        "accountId": account_id,
        "symbol": symbol,
        "action": order_action,
        "orderQty": quantity,
        "orderType": "Market",
        "isAutomated": True
    }

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}"
    }

    response = requests.post(f"https://{version}.tradovateapi.com/v1/order/placeorder", headers=headers, data=json.dumps(initial))

    print(f'Tradovate Status: {response.status_code}')
    print(response.text)

# This function will cancel an order for you

def cancel_order(account_id, contract_id):
    with open('./accessToken.json') as f:
        access_token = json.load(f)['accessToken']

    body = {
        "accountId": account_id,
        "contractId": contract_id,
        "admin": False
    }

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}"
    }

    response = requests.post(f'https://{version}.tradovateapi.com/v1/order/liquidateposition', headers=headers, data=json.dumps(body))

    print(f'Tradovate Status: {response.status_code}')
    print(response.text)

# This function will refresh your access token
# It is advisable to call this function in a loop to keep your access token fresh
# As of my present knowledge, the access token expires every hour

def refresh_access_token():
    print(f"Refreshing your access token... [{datetime.datetime.now()}]")

    # You must register an app on tradovate's website prior to these variables working properly

    body = {
        "name": f"{name}",
        "password": f"{password}",
        "appId": f"{app_id}",
        "appVersion": f"{app_version}",
        "cid": cid,
        "sec": f"{sec}",
        "deviceId": f"{device_id}"
    }

    response = requests.post(f'https://{version}.tradovateapi.com/v1/auth/accesstokenrequest', json=body)

    if response.status_code == 200:
        print(f"Access token successfully refreshed [{datetime.datetime.now().isoformat()}]")
        try:
            data = {"accessToken": response.json()['accessToken']}
        except Exception as e:

            # Most common exception is thrown because you forgot to register your app properly

            print(f"Error: {e}")
            print(f"Response: {response.text}")
            return
        with open("./accessToken.json", 'w') as f:
            json.dump(data, f)
```
