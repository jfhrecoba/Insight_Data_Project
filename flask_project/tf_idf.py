import nltk
import string
import pandas as pd
import numpy as np
import json
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction import DictVectorizer

home = "../data/"

def tokenize(text):
    tokens = nltk.word_tokenize(text)
    '''
    Function to break up sentences/text into individual units (in this case, words)
    '''
    #After the text is divided into words, you stem each word and return the stems. 
    #stems = stem_tokens(tokens, stemmer)
    #return stems
    return tokens


def initialize_tfidf(corpus):
    '''
    Calculates the tf-idf matrix given a document corpus. In this case, the document corpus is
    going to be the item_descriptions from each of our items for sale on shopbop.com, which was 
    scraped for info. Adding color info to description as well (although not sure if this is being
    used in the way that I would like)
    '''
    tfidf = TfidfVectorizer(tokenizer=tokenize, stop_words='english')
    tfs = tfidf.fit_transform(corpus)
    #features = tfidf.get_feature_names()
    #print(len(features))
    return tfs, tfidf


def get_top_n(query,tfidf):
    weights = tfidf.transform([query])
    feature_names = tfidf.get_feature_names()#gets word names
     #Return words & weights in terms of importance:
    item_weights = {}
    #for each word in weights matrix:
    for col in weights.nonzero()[1]:
        item_weights[feature_names[col]]= weights[0, col]
    #sort words from largest weight to smallest:
    item_weights_sorted = [(k, item_weights[k]) for k in sorted(item_weights, key=item_weights.get, reverse=True)]
    
    words = [list(t) for t in zip(*item_weights_sorted)][0]
    if len(words) >= 15:
        return words[0:15]
    else:
        return words

if __name__ == '__main__':
    with open(home+'wmd_corpus') as f:
        wmd_corpus = json.load(f)

    joined_corpus = [" ".join(doc) for doc in wmd_corpus]
    #print(joined_corpus)
    tfs, tfidf = initialize_tfidf(joined_corpus)

    query = "a boxy  phillip lim crossbody bag in soft leather slim back pocket a polished loop secures the top flap lined interior with  card slots chain shoulder strap dust bag included\nleather lambskin\nweight oz  kg\nimported china\nmeasurements\nheight in  cm\nlength in  cm\ndepth in  cm\nstrap drop in  cm"
    top_n = get_top_n(query,tfidf)
    print(top_n)
    

