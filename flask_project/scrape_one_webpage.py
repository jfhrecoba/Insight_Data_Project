from bs4 import BeautifulSoup
#from time import sleep
import urllib3
import requests
import re
import json
from scrape_shopbop import find_selected_color as sb_find_selected_color
from scrape_shopbop import find_image as sb_find_image
from scrape_shopbop import find_price as sb_find_price
from scrape_shopbop import find_description as sb_find_description
from scrape_shopbop import find_title as sb_find_title
from scrape_shopbop import parse_html as sb_parse_html

from scrape_nordstrom import find_selected_color as nd_find_selected_color
from scrape_nordstrom import find_image as nd_find_image
from scrape_nordstrom import find_price as nd_find_price
from scrape_nordstrom import find_description as nd_find_description
from scrape_nordstrom import find_title as nd_find_title
from scrape_nordstrom import parse_html as nd_parse_html
from scrape_nordstrom import find_image_for_url as nd_find_image_for_url

def scrape_one_shopbop(url):
    #price_re = re.compile('\$[0-9]+\.[0-9]{2}')
    price_re = re.compile('\$[0-9]{1,3}(?:,?[0-9]{3})*\.[0-9]{2}')
    soup = sb_parse_html(url)
    color = sb_find_selected_color(soup)
    image = sb_find_image(soup)
    price = sb_find_price(soup)
    description = sb_find_description(soup)
    title = sb_find_title(soup)

    item_dict = {}
    item_dict['url'] = url
    item_dict['color'] = color
    item_dict['image'] = image
    item_dict['price'] = price
    item_dict['description'] = description
    item_dict['title'] = title

    return item_dict

def scrape_one_nordstrom(url):
    headers = requests.utils.default_headers()
    #for this website, you have to specify a user agent or you will be given blank pages back. 
    headers.update({
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'
        })

    price_re = re.compile('\$[0-9]{1,3}(?:,?[0-9]{3})*\.[0-9]{2}')

    soup = nd_parse_html(url)
    color = nd_find_selected_color(soup)
    price = nd_find_price(soup)
    description = nd_find_description(soup)
    title = nd_find_title(soup)
    
    item_dict = {}
    item_dict['url'] = url
    item_dict['color'] = color
    item_dict['image'] = nd_find_image_for_url(url)
    item_dict['price'] = price
    item_dict['description'] = description
    item_dict['title'] = title

    return item_dict

def scrape_one_webpage(url):
    
    if 'shopbop' in url:
        item_dict = scrape_one_shopbop(url)

    elif 'nordstrom' in url:
        item_dict = scrape_one_nordstrom(url)

    return item_dict


if __name__ == "__main__":
    url = 'http://shop.nordstrom.com/s/rosie-hw-x-paige-bessy-metallic-silk-blouse/4739990?origin=category-personalizedsort&fashioncolor=BLACK%20METALLIC'
    item_dict = scrape_one_webpage(url)
    print(item_dict)
