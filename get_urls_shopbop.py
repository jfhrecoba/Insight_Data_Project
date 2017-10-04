from bs4 import BeautifulSoup
#import urllib.request
import urllib3
import requests
from time import sleep

localHome = "/Users/saraszczepanski"
ec2home = "/home/ec2-user"
home = localHome

numPages = 5100

#pageRoot = "https://www.shopbop.com/clothing/br/v=1/13266.htm"
#pageRoot = "https://www.shopbop.com/shoes/br/v=1/13438.htm"
#pageRoot = "https://www.shopbop.com/bags/br/v=1/13505.htm"
pageRoot = "https://www.shopbop.com/accessories/br/v=1/13539.htm"

outputFilename = 'urls_shopbop_accessories_2'

#f = open('/Users/saraszczepanski/workspace/insight_project/data/urls_accessories', 'w')
f = open('{}/workspace/insight_project/data/{}'.format(home, outputFilename), 'w')
 
#Note: the numbers below must change for each site, corresponding to the page number/item number. 
for i in range(0, numPages, 100):
    #webpage = requests.get('http://www.shopbop.com/clothing/br/v=1/13266.htm?baseIndex={}'.format(i)) #clothing
    #webpage = requests.get('http://www.shopbop.com/shoes/br/v=1/13438.htm?baseIndex={}'.format(i)).text #shoes
    #webpage = requests.get('http://www.shopbop.com/bags/br/v=1/13505.htm?baseIndex={}'.format(i)).text #bags
    webpage = requests.get('{}?baseIndex={}'.format(pageRoot, i)).text #accessories
    soup = BeautifulSoup(webpage, 'html5lib')
    for anchor in soup.find_all('a'):
        url = anchor.get('href', '/')
        if "folderID" not in url:
            continue
        f.write('http://www.shopbop.com{}\n'.format(url))
    sleep(0.5)
 
f.close()