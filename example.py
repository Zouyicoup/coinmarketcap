#!/usr/bin/env python3
#Add local folder as sys path
from sys import path
path.append('./')
from time import sleep
#from price import getbitcoin_price
from price import getbitcoin_price

API_KEY='017c4707-d8d9-4b78-bb0d-3a309a6e96d9'

while True:
  query = getbitcoin_price(API_KEY)
  print("bitcoin price: %s" % query.price)
  sleep(86400/333) #You only get 333 queries a day, which is about 5 min
