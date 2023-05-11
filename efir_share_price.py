import pandas as pd
import requests
import datetime as dt
import config

# Efir API endpoint URL
url = 'https://dh2.efir-net.ru/v2'

# Enter Efir API login and password.
login = config.login
password = config.password

# Set the URL for the account endpoint
account_url = url + '/Account/Login'

# Set the request body for the account endpoint
payload = {'login': login, 'password': password}

# Send a POST request to the account endpoint
response = requests.post(account_url, json=payload)
result = response.json()
api_token = result['token']

# Add tickers to the list
tickers = ['BSPB']

# Specify the period to get prices
number_of_years = 3

dateFrom = (dt.datetime.now() - dt.timedelta(days=365*number_of_years)).strftime("%Y-%m-%d")
dateTo = dt.datetime.now().strftime("%Y-%m-%d")

url = url + '/Moex/History'
headers = {'authorization': 'Bearer ' + api_token, 'Content-Type': 'application/json'}

body = {
    'engine' : 'stock',
    'market' : 'shares',
    'instruments': tickers,
    'dateFrom': dateFrom,
    'dateTo': dateTo
    }

response = requests.post(url, json=body, headers=headers)
result = response.json()
df = pd.DataFrame(result)
df = df[df['boardname'] == 'Т+: Акции и ДР - безадрес.']
df = df[['secid','tradedate','close']]
df.drop_duplicates(subset = ['secid','tradedate'], keep = 'first', inplace = True)
df = df.dropna()
df.reset_index(drop = True, inplace = True)

# Export dataframe with prices to an excel file
df.to_excel('Share_prices.xlsx')