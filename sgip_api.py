# -*- coding: utf-8 -*-
"""
Only tested in Python 3.
You may need to install the 'requests' Python3 module.

Be sure to fill in your username, password, org name and email before running
"""

import requests
from requests.auth import HTTPBasicAuth

# account details
username = 'YOUR USERNAME HERE'
password = 'YOUR PASSWORD HERE'
email = 'some_email@gmail.com'
org = 'some_org_name'

# request details
ba = 'SGIP_CAISO_SCE'  # identify grid region
# starttime and endtime are optional, if ommited will return the latest value
starttime = '2020-03-01T00:00:00-0000'  # UTC offset of 0 (PDT is -7, PST -8)
endtime = '2020-03-01T00:45:00-0000'
moer_version = '1.0' #'2.0'


# long term forecast horizon
horizon = 'month'  # 'month' or 'year'


def register(username, password, email, org):
    url = 'https://sgipsignal.com/register'
    params = {'username': username,
              'password': password,
              'email': email,
              'org': org}
    rsp = requests.post(url, json=params)
    print(rsp.text)


def login(username, password):
    url = 'https://sgipsignal.com/login'
    try:
        rsp = requests.get(url, auth=HTTPBasicAuth(username, password))
    except BaseException as e:
        print('There was an error making your login request: {}'.format(e))
        return None

    try:
        return rsp.json()['token']
    except BaseException:
        print('There was an error logging in. The message returned from the '
              'api is {}'.format(rsp.text))
        return None


def moer(token, ba, starttime=None, endtime=None, version=None):
    url = 'https://sgipsignal.com/sgipmoer'
    headers = {'Authorization': 'Bearer {}'.format(token)}
    params = {'ba': ba}
    if starttime:
        params.update({'starttime': starttime, 'endtime': endtime})
    if version:
        params['version'] = version
        
    rsp = requests.get(url, headers=headers, params=params)
    # print(rsp.text)  # uncomment to see raw response
    return rsp.json()


def forecast(token, ba, starttime=None, endtime=None, version=None):
    url = 'https://sgipsignal.com/sgipforecast'
    headers = {'Authorization': 'Bearer {}'.format(token)}

    params = {'ba': ba}
    if starttime:
        params.update({'starttime': starttime, 'endtime': endtime})
    if version:
        params['version'] = version
        
    rsp = requests.get(url, headers=headers, params=params)
    # print(rsp.text)  # uncomment to see raw response
    return rsp.json()


def longforecast(token, ba, horizon, starttime=None, endtime=None):
    url = 'https://sgipsignal.com/sgiplongforecast'
    headers = {'Authorization': 'Bearer {}'.format(token)}

    params = {'ba': ba,
              'horizon': horizon}
    if starttime:
        params.update({'starttime': starttime, 'endtime': endtime})

    rsp = requests.get(url, headers=headers, params=params)
    # print(rsp.text)  # uncomment to see raw response
    return(rsp.json())


# Only register once!!
# register(username, password, email, org)

token = login(username, password)
print(token)
if not token:
    print('You will need to fix your login credentials (username and password '
          'at the start of this file) before you can query other endpoints. '
          'Make sure that you have registered at least once by uncommenting '
          'the register(username, password, email, org) line near the bottom '
          'of this file.')
    exit()

realtime_moer = moer(token, ba)
print(realtime_moer)

historical_moer = moer(token, ba, starttime, endtime)
print(historical_moer)

specific_moer_version = moer(token, ba, starttime, endtime, moer_version)
print(specific_moer_version)

forecast_moer = forecast(token, ba)
print(forecast_moer)

longforecast_moer = longforecast(token, ba, horizon)
print(longforecast_moer)
