from flask import render_template
from flask import request
from sara_flask_project import app

from nltk.corpus import stopwords
from nltk import download
from nltk import word_tokenize
import json
from gensim.models import Word2Vec
from gensim.models import KeyedVectors
# from gensim.similarities import WmdSimilarity

from bs4 import BeautifulSoup
#from time import sleep
import urllib3
import requests
import re
import json
from scrape_shopbop import find_colors, find_image, find_price, find_description, find_title, parse_html
from scrape_one_webpage import scrape_one_webpage
from query_wmd_model import query_wmd_model
from preprocess_words import preprocess
from wmd_similarity import WmdSimilarity
from tf_idf import initialize_tfidf, get_top_n
from time import time

path = '../data/'
#file_in = 'products_all_newline' #final file with all products from shopbop
num_best = 10 #this is the number of products that the model will spit out/recommend. 

model = KeyedVectors.load(path + 'word2vec_shopbop_nordstrom_model')
#model = KeyedVectors.load_word2vec_format(fname="/data/GoogleNews-vectors-negative300.bin", binary=True)
#model = KeyedVectors.load_word2vec_format(fname="/data/glove.twitter.27B.25d.txt", binary=False)
  #load json files
with open(path+'wmd_corpus') as f:
  wmd_corpus_curr = json.load(f)
with open(path+'documents') as f:
  documents_curr = json.load(f)
with open(path+'titles') as f:
  titles_curr = json.load(f)
with open(path+'urls') as f:
  urls_curr = json.load(f)
with open(path+'images') as f:
  images_curr = json.load(f)

# uncomment to re-enable tfidf
# joined_corpus = [" ".join(doc) for doc in wmd_corpus_curr]
# tfs, tfidf = initialize_tfidf(joined_corpus)

def get_resource_and_color_from_nordstrom_url(url):
  '''
  This function breaks up Nordstrom url in order to compare the root url and
  the color of the item. Color is always somewhere in the url after the '?'
  '''
  url_color = None
  tok_url = url.split('?')
  if len(tok_url) > 1:
    tok_qry = tok_url[1].split('&fashioncolor=')
    if len(tok_qry) > 1:
      url_color = tok_qry[1].split('&')[0]
  return tok_url[0], url_color

#run @ system start:
@app.route('/')

@app.route('/input')
#put top function that calls the rest of your anlaysis here.
def index():
  return render_template("input.html")

@app.route('/output')
def output():

  url = request.args.get('url', '')
  
  #find the information from the webpage you want to search
  item_to_find = scrape_one_webpage(url)
  #query = "a boxy  phillip lim crossbody bag in soft leather slim back pocket a polished loop secures the top flap lined interior with  card slots chain shoulder strap dust bag included\nleather lambskin\nweight oz  kg\nimported china\nmeasurements\nheight in  cm\nlength in  cm\ndepth in  cm\nstrap drop in  cm"
  if 'shopbop' in url:
    query = item_to_find['description'] + " " + item_to_find['color'] 
  elif 'nordstrom' in url:
    description_all = ' '.join(item_to_find['description'])
    query = description_all + " " + item_to_find['color']
    #print("query={}".format(query))

  #top_n = get_top_n(query,tfidf) #returns top 15 words that best describe the item according to tfidf

  #print("top_n={}".format(top_n))

  # Initialize WmdSimilarity (search engine)
  instance = WmdSimilarity(wmd_corpus_curr, model, num_best)
  #print("query={}".format(query))
  #start_time = time()
  #sims = query_wmd_model('black leather backpack',instance)
  #sims = query_wmd_model('faux fur wolf jacket helmut lang',instance)
  sims = query_wmd_model(query, instance) #this preprocesses query words as well. 
  #sims = query_wmd_model(" ".join(top_n), instance) #use if running tf-idf first. 
  #total_time = time() - start_time
  #print("elapsed time = {}s".format(total_time))
  
  #Return the retrieved documents, together with their similarities.
  urls_out = []
  images_out = []
  titles_out = []
  documents_out = []
  
  for i in range(num_best): #get rid of exact match (in case you are searching for item that is in corpus)
    #print('sim = %.4f' % sims[i][1])
    #print(documents[sims[i]])
    curr_url = urls_curr[sims[i][0]]
    if 'shopbop' in url:
      if url.split('?')[0] == curr_url.split('?')[0]:
        continue
    elif 'nordstrom' in url:
      url, url_color = get_resource_and_color_from_nordstrom_url(url)
      curr_url, curr_url_color = get_resource_and_color_from_nordstrom_url(curr_url)
      if curr_url == url and curr_url_color == url_color:
        continue
    #print(urls_curr[sims[i][0]])
    urls_out.append(urls_curr[sims[i][0]])
    images_out.append(images_curr[sims[i][0]])
    titles_out.append(titles_curr[sims[i][0]])

  #print(urls_out[:])

  return render_template("output.html", 
    image1=images_out[0], image2=images_out[1], image3=images_out[2], 
    url1=urls_out[0], url2=urls_out[1], url3=urls_out[2],
    title1=titles_out[0], title2=titles_out[1], title3=titles_out[2])





