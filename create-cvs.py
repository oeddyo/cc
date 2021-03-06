
import requests
import json
import sys
import os
#import csv
import unicodecsv as csv
category = sys.argv[1]

def filterValidTags(tags):
  res = set()
  for tag in tags:
    if(tag.isalpha()):
      res.add(tag.lower())
  return list(res)

def generateHTML(content):
  print "content = ", content
  if not content:
    return ""
  res = "<table>"
  for row in content:
    if 'key' in row:
      key = row['key']
    else:
      key = ""
    if 'value' in row:
      value = row['value']
    else:
      value = ""

    res += "<tr>"
    res += '<td class="description-key">' + key + "</td>"
    res += '<td class="description-value">' + value + "</td>"
    res += "</tr>"
  res += "</table>"
  return res

fieldnames = ["Handle", "Title", "Body (HTML)", "Vendor", "Type", "Tags", "Published", "Variant Grams", "Variant Inventory Quantity", "Variant Inventory Policy", "Variant Fulfillment Service", "Variant Price", "Variant Compare at Price", "Option1 Name", "Option1 Value", "Option2 Name", "Option2 Value", "Image Src"]
with open('employee_file2.csv', mode='w') as csv_file:
  writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
  writer.writeheader()

  for filename in os.listdir("./" + category):
    path = "./" + category + "/" + filename
    with open(path) as jsonFile: 
      data = json.load(jsonFile)
      productInfo = data['product_info']
      skuInfo = data['sku_info']

      print "----------------"

      # handle
      print "id = ", productInfo["id"]
      print productInfo


      imageIndex = 0
      for imageIndex, sku in enumerate(skuInfo):
        print sku
        # a row
        row = {}
        row['Handle'] = productInfo["id"]
        row['Title'] = productInfo["name"]
        row['Body (HTML)'] = generateHTML(productInfo["b_specifics"])
        row['Vendor'] = "Corner Gem"
        row['Type'] = category

        #row['Tags'] = ",".join(list(set(productInfo["search_keywords"].split())))

        row['Tags'] = ",".join(filterValidTags(productInfo["search_keywords"].split()))

        row['Published'] = True
        row['Variant Grams'] = 0.1
        print sku['attribute_info']
        for comb in sku['attribute_info']:
          row['Variant Inventory Quantity'] = 10000
          row['Variant Inventory Policy'] = "deny"
          row['Variant Fulfillment Service'] = "manual"
          row['Variant Price'] = productInfo['list_price']
          row['Variant Compare at Price'] = productInfo['c_platform_price']

          attrName = comb['attr_name']
          attrValue = comb['attr_value_name']

          if(attrName == "Color"):
            row['Option1 Name'] = "Color"
            row['Option1 Value'] = attrValue
          elif(attrName == "Size"):
            row['Option2 Name'] = "Size"
            row['Option2 Value'] = attrValue
          else:
            pass
        #print row
        #writer.writerow({'emp_name': 'John Smith', 'dept': 'Accounting', 'birth_month': 'November'})
        imgs = productInfo["product_images"]
        if(imageIndex < len(imgs)):
          img = imgs[imageIndex]
          imgUrl = img['url'][2:]
          row['Image Src'] = "http://" + imgUrl
          print "now row = ", row
        writer.writerow(row)

      for img in productInfo['product_images'][imageIndex+1:]:
        row = {}
        row['Handle'] = productInfo['id']
        imgUrl = "http://" + img['url'][2:]
        row['Image Src'] = imgUrl
        writer.writerow(row)

