import urllib.request
import json
from pandas.io.json import json_normalize
import pandas as pd

""" Python template for retrieving data from gurufocus.com
    Limited to 2,000 requests per month under Kathleen's current subscription. I already used about 10 to write
    and test this code."""

token = '334f65fdde40369654a97bb6b6d77588:af9ac180eb35becaf817dc3b2e114bab'  # This is Kathleen's specific token
ticker = 'WMT'  # Walmart

# 'keyratios' returns a dictionary or ratios (name: value) as of 5-1-2020
response = urllib.request.urlopen('https://api.gurufocus.com/public/user/{}/stock/{}/keyratios'.format(token, ticker))
content = response.read()
data = json.loads(content.decode('utf8'))
keyratios = json_normalize(data)

# 'price' returns a list of split-adjusted closing prices. Walmart has prices back to 1972
response = urllib.request.urlopen('https://api.gurufocus.com/public/user/{}/stock/{}/price'.format(token, ticker))
content = response.read()
data = json.loads(content.decode('utf8'))
price = pd.DataFrame(data)

print('pause')