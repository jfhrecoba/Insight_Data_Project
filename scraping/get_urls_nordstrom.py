from bs4 import BeautifulSoup
#import urllib.request
import urllib3
import requests
from time import sleep

headers = requests.utils.default_headers()
headers.update({
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'
})

localHome = "/Users/saraszczepanski"
ec2home = "/home/ec2-user"
home = localHome

#numPages = 2900 #2869 #clothing count
#numPages = 1208 #shoes count 
#numPages = 438 #bags count
numPages = 1661 #1644 #accessories count

#pageRoot = "http://shop.nordstrom.com/c/womens-clothing?origin=leftnav&cm_sp=Left%20Navigation-_-Clothing&top={}&page={}"
#pageRoot = "http://shop.nordstrom.com/c/womens-shoes?origin=leftnav&cm_sp=Left%20Navigation-_-Shoes&top={}&page={}"
#pageRoot = "http://shop.nordstrom.com/c/womens-handbags?offset=1&top={}&page={}"
#pageRoot = "http://shop.nordstrom.com/c/womens-accessories?origin=leftnav&cm_sp=Left%20Navigation-_-Accessories&top={}page={}"
pageRoot = "http://shop.nordstrom.com/c/womens-accessories?origin=leftnav&cm_sp=Left%20Navigation-_-Accessories&page={}&top={}"

outputFilename =  'urls_nord_accessories_2'  #urls_nord_bags' #urls_nord_shoes' #'urls_nord_clothing'

#f = open('/Users/saraszczepanski/workspace/insight_project/data/urls_accessories', 'w')
f = open('{}/workspace/insight_project/data/{}'.format(home, outputFilename), 'w')
 
#Note: the numbers below must change for each site, corresponding to the page number/item number. 
for i in range(1, numPages, 1):
    #webpage = requests.get('http://www.shopbop.com/clothing/br/v=1/13266.htm?baseIndex={}'.format(i)) #clothing
    #webpage = requests.get('http://www.shopbop.com/shoes/br/v=1/13438.htm?baseIndex={}'.format(i)).text #shoes
    #webpage = requests.get('http://www.shopbop.com/bags/br/v=1/13505.htm?baseIndex={}'.format(i)).text #bags
    pageURL = pageRoot.format(i, 10)
    print('getting page {} from {}'.format(i, pageURL))
    webpage = requests.get(pageURL, headers=headers).text #clothing
    soup = BeautifulSoup(webpage, 'html5lib')
    para_tags = soup.find_all('p', attrs={'class': 'product-title'})
    print('{} p tags on page {}'.format(len(para_tags), i))
    for para in para_tags:
        anchor = para.find('a')
        url = anchor.get('href')
        f.write('shop.nordstrom.com{}\n'.format(url))
#    for para in soup.find_all('p'):
#         for anchor in soup.find('a',attrs={'class': 'product-photo-href'}):
#             #print(anchor)
#             url = anchor.get('href', '/')
#             print(url)
#             f.write('shop.nordstrom.com{}\n'.format(url))
    sleep(0.5)
f.close()