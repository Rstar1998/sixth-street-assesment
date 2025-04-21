from fastapi import FastAPI,HTTPException,Request
import os 
import requests
from cachetools import TTLCache
import re
from datetime import datetime
from dotenv import load_dotenv
import hashlib
import hmac
import base64

def decode_base64(encoded_string):
    """Decodes a Base64 encoded string.

    Args:
        encoded_string: The Base64 encoded string.

    Returns:
        The decoded string, or None if an error occurs.
    """
    try:
        encoded_bytes = encoded_string.encode('ascii')
        decoded_bytes = base64.b64decode(encoded_bytes)
        decoded_string = decoded_bytes.decode('utf-8')
        return decoded_string
    except Exception as e:
        print(f"Error decoding Base64 string: {e}")
        return None

app = FastAPI()

# load env variables
load_dotenv()
ALPHA_VANTAGE_API_KEY = os.getenv("ALPHA_VANTAGE_API_KEY", "demo")


BASE_URL = "https://www.alphavantage.co/query"

CACHE_TTL = 86400  # Cache for 24 hours time to live
# Initialize cache (maxsize=100, TTL=24 hours)  alphavantage API refersh every 24 hours 
cache = TTLCache(maxsize=100, ttl=CACHE_TTL) # in memory cache db 


import requests
import json

def get_keys():
    url = "https://simpleauth-2qrr5eu6wa-uc.a.run.app/keys"

    payload = {}
    headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer '
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    return response.json()


def validate_token(username,received_digest):

    valid_token = False
    keys = get_keys()["keys"]
    print(keys)

    for key in keys:
        computed_digest = hmac.new(key.encode(), username.encode(), hashlib.sha256).hexdigest()
        print(computed_digest)
        if hmac.compare_digest(received_digest, computed_digest):
            valid_token = True
            break
    
    return valid_token



def is_valid_date(date: str):
    # match pattern of 4 digit - 2 digit - 2 digit
    if not re.match(r"^\d{4}-\d{2}-\d{2}$", date):
        return False
    
    try:
        # check for valid date 
        datetime.strptime(date, "%Y-%m-%d")
        return True
    except ValueError:
        return False
    

def fetch_full_stock_data(symbol: str):
    # check if already present in cache and use it 
    if symbol in cache:
        print("Using cache no API hit required ")
        return cache[symbol]
    
    # API params
    params = {
        "function": "TIME_SERIES_DAILY",
        "symbol": symbol,
        "outputsize" : "full",
        "apikey": ALPHA_VANTAGE_API_KEY
    }

    # API call
    response = requests.get(BASE_URL, params=params)
    data = response.json()
    
    # check if "Time Series (Daily)" in response body , there can be a posibilty of API limit reached or Invalid symbol
    if "Time Series (Daily)" not in data:
        print(data)
        raise HTTPException(status_code=400, detail="Invalid symbol or API limit reached")
    
    cache[symbol] = data["Time Series (Daily)"]
    return cache[symbol]



@app.get("/lookup")
def lookup(symbol: str, date: str):

    # check if date is valid or not. raise error in that case 
    if not is_valid_date(date):
        raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD")
    
    # get full stock data for respective symbol (if already present in cache then use that)
    stock_data = fetch_full_stock_data(symbol)

    # if date not present in the data then return 404 data not found ( Public Holidays , Weekends etc)
    if date not in stock_data:
        raise HTTPException(status_code=404, detail="Data not found for given date")
    
    # get data for that date
    daily_data = stock_data[date]

    # return data with proper format and type
    return {
        "open": float(daily_data["1. open"]),
        "high": float(daily_data["2. high"]),
        "low": float(daily_data["3. low"]),
        "close": float(daily_data["4. close"]),
        "volume": int(daily_data["5. volume"])
    }


@app.get("/min")
def get_min(request: Request):
    authorization_header = request.headers.get("Authorization")
    if not authorization_header :
        raise HTTPException(status_code=401, detail="Authorization header is missing")
    
    try:
        token_type, token = authorization_header.split(" ")
        if token_type.lower() != "bearer":
             raise HTTPException(status_code=401, detail="Invalid token type")
    except ValueError:
        raise HTTPException(status_code=401, detail="Invalid authorization header format")
    
    decode_string = decode_base64(token)
    arr = decode_string.split(":")
    print(arr)

    if not validate_token(arr[0],arr[1]):
        raise HTTPException(status_code=401, detail="Unauthorization header format")


    # symbol =request.query_params['symbol']
    # range =request.query_params['range']

    # #symbol: str, range: int , 

    # # range should be atleast 1
    # if range <= 0:
    #     raise HTTPException(status_code=400, detail="Invalid range")
    
    # # get full stock data
    # stock_data = fetch_full_stock_data(symbol)

    # # get list of last n dates
    # last_n_days = list(stock_data.keys())[:range]

    # # for each last n days calculate min of low
    # min_price = min(float(stock_data[day]["3. low"]) for day in last_n_days)

    return {"min": "0"}
   

@app.get("/max")
def get_max(symbol: str, range: int):
    
     # range should be atleast 1
    if range <= 0:
        raise HTTPException(status_code=400, detail="Invalid range")
    
    # get full stock data
    stock_data = fetch_full_stock_data(symbol)

    # get list of last n dates 
    last_n_days = list(stock_data.keys())[:range]

    # for each last n days calculate max of high
    max_price = max(float(stock_data[day]["2. high"]) for day in last_n_days)

    return {"max": max_price}


@app.get("/status")
def status():
    return {"app": "boilerplate"}
