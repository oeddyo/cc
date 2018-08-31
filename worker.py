import redis
from fake_useragent import UserAgent
from time import sleep
from random import randint
import json
import os,binascii
import requests

redisClient = redis.StrictRedis(host='localhost', port=6379, db=0)

while True:
  sleep(randint(1,5))
  productInfo = redisClient.rpop("crawl_queue")
  splitted = productInfo.split(":")

  productCategory = splitted[0]
  productId = splitted[1]

  print 'My product Id = ', productId
  ua = UserAgent()
  randomAgent = ua.random

  headers = {
    "client-basic": json.dumps({"country_code":"in","language_code":"en","gender":"U","guest_id": binascii.b2a_hex(os.urandom(15)),"from_site":"pc_site"}),
    "User-Agent": randomAgent
  }

  productUrl = "https://www.clubfactory.com/v1/product/{}".format(productId)

  try:
    totalJson = requests.get(productUrl, headers=headers, timeout=5).json()
    redisClient.set("product" + ":" + productId + ":" + productCategory, totalJson)
  except Exception as e:
    print "Error getting ", productUrl
    print e

