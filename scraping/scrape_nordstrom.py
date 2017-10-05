from bs4 import BeautifulSoup
from time import sleep
import random
import urllib3
import requests
import re
import json

localHome = "/Users/saraszczepanski"
ec2home = "/home/ec2-user"
home = ec2home

inputFilename = "urls_nord_accessories"
outputFilename = "products_nord_accessories"

headers = requests.utils.default_headers()
#for this website, you have to specify a user agent or you will be given blank pages back. 
headers.update({
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'
})

#price_re = re.compile('\$[0-9]+\.[0-9]{2}')
price_re = re.compile('\$[0-9]{1,3}(?:,?[0-9]{3})*\.[0-9]{2}')

def find_colors(soup):
	#Find the color info
	colorImgs = soup.find_all('img', attrs={'class': 'np-image', 'alt': re.compile('.*swatch image')})
	colors = {}
	for color in colorImgs:
	    key = color.get('alt').split(' swatch')[0]
	    imgUrl = color.get('src')
	    if imgUrl == None:
	    	return None
	    value = imgUrl.split('?')[0]
	    colors[key] = value
	return colors


def find_selected_color(soup):
	'''
	Return the color name for a single item. 
	'''
	colorImg = soup.find('img', attrs={'class': 'np-image', 'alt': re.compile('.*swatch image selected')})
	if colorImg == None:
		colorImg = soup.find('img', attrs={'class': 'np-image', 'alt': re.compile('.*swatch image')})
	if colorImg == None:
		return ""
	key = colorImg.get('alt').split(' swatch')[0]
	imgUrl = colorImg.get('src')
	if imgUrl == None:
		return None
		value = imgUrl.split('?')[0]
	return key


def find_image_for_url(url):
	soup = parse_html(url)
	return find_image(soup)


def find_image(soup):
    #Find the image
    image = soup.find('img')
    return image.get('src').split('?')[0]


def find_price(soup):
	#Find the price info
	priceDiv = soup.find('div', attrs={'class': 'price-display-inner'})
	if (priceDiv == None):
		return None
	price = priceDiv.find('div', attrs={'class': 'current-price'}).getText()
	return price

def find_description(soup):
	#Find item description info
	itemDetails = soup.find("div", attrs={'class': 'product-details-and-care'})
	itemDesc = itemDetails.find("div", attrs={'class': 'item-description-body'}).find('p').getText()
	details = []
	details.append(itemDesc)
	for line in itemDetails.find_all('li'):
	    details.append(line.getText())
	return details

def find_title(soup):
	title_all = soup.find_all("title")
	title = title_all[0].text[:-12]
	#print(title)
	return title

def parse_html(url):
    
    #get the text from the url
    #http = urllib3.PoolManager()
    #page_text = http.request('GET', url)
    #replace the breaks with spaces
    #new_text=re.sub('</br>',' ',page_text)
    
    html = requests.get(url, headers=headers).text
    #parse the html
    soup = BeautifulSoup(html,'html5lib')
    return soup


if __name__ == "__main__":
	with open('{}/workspace/insight_project/data/{}'.format(home, inputFilename)) as f:
		with open('{}/workspace/insight_project/data/{}'.format(home, outputFilename), 'w') as out:
			out.write('[')

			for url in f:
				url = 'http://' + url.strip(' \t\n\r')
				try:
					# print(url)

					soup = parse_html(url)

					colors = find_colors(soup)
					if colors == None:
						continue
					# image = find_image(soup)
					price = find_price(soup)
					description = find_description(soup)
					title = find_title(soup)

					for color_name, color_image in colors.items():
						color_name_url_suffix = '%20'.join(color_name.upper().split(' '))
						if ('&fashioncolor=' in url):
							url = url.split('&fashioncolor=')[0] + '&fashioncolor=' + color_name_url_suffix
						else:
							url = url + '&fashioncolor=' + color_name_url_suffix
						# print(url)
						item_dict = {}
						item_dict['url'] = url
						item_dict['color'] = color_name
						item_dict['image'] = find_image_for_url(url)
						item_dict['price'] = price
						item_dict['description'] = description
						item_dict['title'] = title

						json.dump(item_dict, out)
						out.write(',\n')
					out.flush()
					sleep_len = random.uniform(0.1, 0.5)
					sleep(sleep_len)
				except:
					sleep_len = random.uniform(5, 10)
					print("warning, an error occured, url={}".format(url))
					print("sleeping {}s".format(sleep_len))
					sleep(sleep_len)
					continue

			out.write(']')

