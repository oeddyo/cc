import requests
import json
import sys
import os
from fake_useragent import UserAgent
import os,binascii
from random import randint
from time import sleep
import redis

#category = sys.argv[1]
#totalLimit = int(sys.argv[2])
redisClient = redis.StrictRedis(host='localhost', port=6379, db=0)

limits = {
  51: 67500,
  52: 16500,
  53: 30100,
  54: 11000,
  55: 40000,
  56: 17500,
  57: 6000,
  58: 4000,
  59: 21000,
  60: 9000,
  61: 5000,
  62: 500,
  63: 1000,
}
for category in range(51, 62):
  pageLimit = (limits[category] / 100)  + 1
  for i in range(pageLimit):
    sleep(randint(1,5))
    limit = 100
    offset = i * 100
    url = "https://www.clubfactory.com/v1/product?limit={}&offset={}&category_id={}&sort_by=Default".format(
      limit, offset, category
    )
    print "URL = ", url
    ua = UserAgent()
    randomAgent = ua.random
    print randomAgent
    #https://www.clubfactory.com/v1/product/2029466
    headers = {
      "client-basic": json.dumps({"country_code":"in","language_code":"en","gender":"U","guest_id": binascii.b2a_hex(os.urandom(15)),"from_site":"pc_site"}),
      "User-Agent": randomAgent
    }
    try: 
      r = requests.get(url, headers=headers)
      cnt = 0
      for p in r.json()['product_info']:
        cnt += 1
        productId = p['id']
        redisClient.rpush("crawl_queue", str(category) + ":" + str(productId))
    except Exception as e:
      print "Error ", e
      continue
  