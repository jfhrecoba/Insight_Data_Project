from bs4 import BeautifulSoup
from time import sleep
import urllib3
import requests
import re
import json

localHome = "/Users/saraszczepanski"
ec2home = "/home/ec2-user"
home = localHome

inputFilename = ""
outputFilename = ""

#price_re = re.compile('\$[0-9]+\.[0-9]{2}')
price_re = re.compile('\$[0-9]{1,3}(?:,?[0-9]{3})*\.[0-9]{2}')

def find_colors(soup):
	#Find the color info
	swatches = soup.find('div', attrs={'class': 'swatchImages'})
	color_tags = swatches.find_all('img',{"id":re.compile('swatchImage.*')})
	colors = []
	for color_tag in color_tags:
	    color = color_tag.get('alt')
	    colors.append(color)
	return colors


def find_selected_color(soup):
	#find only one selected color:
	#shopbop webpages are broken. there is no way to fetch the particular color that a person chooses from the
	#website in real time, since the url does not change when a different color is chosen. So one can only 
	#search for the default color that is listed (useing the default url). therefore, you can only search for 
	#an item that is the default color. 
	#the code in the three lines below doesn't work because there is no way to fetch swatchSelected.
	#swatches = soup.find('div', attrs={'class': 'swatchImages'})
	#color_tag = swatches.find('img',{"class":re.compile('.*swatchSelected')})
	#return color_tag.get('alt')

	#The code below grabs the first color by default:
	swatches = soup.find('div', attrs={'class': 'swatchImages'})
	color_tags = swatches.find_all('img',{"id":re.compile('swatchImage.*')})
	color = color_tags[0].get('alt')
	return color


def find_image(soup):
    #Find the image
    image = soup.find('img', attrs={'id': 'productImage'})
    return image.get('src')


def find_price(soup):
	#Find the price info
	price = soup.find("div", attrs={'class': 'priceBlock'})
	price = price.text.strip()
	m = price_re.match(price)
	return m.group()


def find_description(soup):
	#Find item description info
	description = soup.find("div", itemprop="description")
	return description.getText(separator='\n').strip()


def find_title(soup):
	title_all = soup.find_all("title")
	title = title_all[0].text[:-10]
	return title


def parse_html(url):
    
    #get the text from the url
    #http = urllib3.PoolManager()
    #page_text = http.request('GET', url)
    #replace the breaks with spaces
    #new_text=re.sub('</br>',' ',page_text)
    
    html = requests.get(url).text
    #parse the html
    soup = BeautifulSoup(html,'html5lib')
    return soup


if __name__ == "__main__":
	with open('{}/workspace/insight_project/data/{}'.format(home, inputFilename)) as f:
		with open('{}/workspace/insight_project/data/{}'.format(home, outputFilename), 'w') as out:
			out.write('[')

			for url in f:
				soup = parse_html(url)

				colors = find_colors(soup)
				image = find_image(soup)
				price = find_price(soup)
				description = find_description(soup)
				title = find_title(soup)

				for color in colors:
					item_dict = {}
					item_dict['url'] = url
					item_dict['color'] = color
					item_dict['image'] = image
					item_dict['price'] = price
					item_dict['description'] = description
					item_dict['title'] = title

					json.dump(item_dict, out)
					out.write(',')
				out.flush()
				sleep(1)

			out.write(']')

