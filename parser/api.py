#!/usr/bin/python3
import requests

URL = 'https://президентскиегранты.рф/public/application/table'

# I don't know why, but these empty params are required
DEFAULT_PARAMS = {
    'SearchString':'',
    'DirectionId':'',
}

# I'm Browser. Without it i can't get content :(
HEADERS = {
    'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) \
                  AppleWebKit/537.36 (KHTML, like Gecko) \
                  Chrome/69.0.3497.100 Safari/537.36'
}

def request(URL, params):
    params = {**DEFAULT_PARAMS, **params}

    response = requests.get(URL, params=params, headers=HEADERS)
    
    if response.status_code != 200:
        response.raise_for_status()
    return response
