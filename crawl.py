
import requests
import json
import sys
import os
from fake_useragent import UserAgent
import os,binascii
from random import randint
from time import sleep

category = sys.argv[1]

if not os.path.isdir("./" + category):
  os.mkdir("./" + category)

for i in range(10, 1000):
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
      sleep(randint(1,5))
      cnt += 1
      print "Working on ", cnt
      productId = p['id']
      productUrl = "https://www.clubfactory.com/v1/product/{}".format(productId)
      totalJson = requests.get(productUrl, headers=headers, timeout=5).json()

      # write to file
      with open("./" + category + "/" + str(productId) + '.json', 'w') as outfile:
        json.dump(totalJson, outfile)

      """
      rProductJson = totalJson['product_info']
      existDetail = False
      if len(rProductJson['c_details']) > 0:
        existDetail = True
      if(existDetail):
        cDetail = rProductJson['c_details'][0]
        print 'Wish link: ' + cDetail['c_url'] + ' CF link: ' "https://www.clubfactory.com/views/product/detail.html?productId={}".format(productId)
      else:
        print "No detail exist"
      """
  except Exception as e:
    print "Error: ", e, "when trying ", url, cnt
    continue



