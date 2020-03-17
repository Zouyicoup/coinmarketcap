#!/usr/bin/env python3
#Load default modules

try:
  from urllib3 import PoolManager
  from json import loads as json
  from time import time
except:
  print("unable to import default modules")
  exit()

#Install non-standard modules
from sys import path
path.append('./')
from installer import install as installer

#import non-standard modules
try:
  import pymysql as mysql
except:
  installer('pymysql')

#Set constants
http = PoolManager()
URL = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'

class getbitcoin_price(object):

  def __init__(self, API_KEY, SQL_PASSWD):
      self.API_KEY = API_KEY
      self.SQL_PASSWD = SQL_PASSWD
      last_poll = self.read_db(self.SQL_PASSWD)
      check = self.time_check(last_poll)
      if type(check) == float:
       return None
      api_data = self.grab(API_KEY); f=open('json', 'w'); f.write(api_data); f.close();
      db_update = self.updatedb(api_data, SQL_PASSWD)

  def read_db(self, SQL_PASSWD):
      try:
        db = mysql.connect("127.0.0.1", "bitcoin", SQL_PASSWD, "bitcoin")
        cursor = db.cursor()
        cursor.execute("select time from price order by id desc limit 1;")
        return cursor._rows[0][0]
      except:
        print("Unable to connect to sql db")
        exit()

  def time_check(self, last_row):
      if float(time()) > float(last_row)+260:
        return True
      else:
        print("Last updated time is less than 5 min. Skipping")
        return float(last_row)+300

  def grab(self, API_KEY):
      r = http.request("GET", URL, headers={
      'Accepts': 'application/json',
      'X-CMC_PRO_API_KEY': API_KEY}
      )
      return r.data.decode()

  def updatedb(self, html, SQL_PASSWD):
    #Import rows from json
    self.body = json(html)
    self.time = time()
    self.price = self.body['data'][0]['quote']['USD']['price']
    self.percent_change_1h = self.body['data'][0]['quote']['USD']['percent_change_1h']
    self.percent_change_24h = self.body['data'][0]['quote']['USD']['percent_change_24h']
    self.percent_change_7d = self.body['data'][0]['quote']['USD']['percent_change_7d']

    #Export values to db
    db = mysql.connect("127.0.0.1", "bitcoin", SQL_PASSWD, "bitcoin")
    cursor = db.cursor()
    query = 'insert into price (time, price, percent_change_1h, percent_change_24h, percent_change_7d) values (%s, %s, %s, %s, %s)'
    values = (self.time, self.price, self.percent_change_1h, self.percent_change_24h, self.percent_change_7d)
    cursor.execute(query, values)
    db.commit()
    return True
