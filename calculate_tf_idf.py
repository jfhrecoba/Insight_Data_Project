import json
import nltk
import string
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction import DictVectorizer
from nltk.stem.porter import PorterStemmer

path = '/Users/saraszczepanski/workspace/insight_project/test/'

stemmer = PorterStemmer()#default/suggested stemmer to use


def stem_tokens(tokens, stemmer):
	'''
	Function to stem eachf word (put word at it's root. removes 'ing','ed',possessives,plurals, etc)
	'''
    stemmed = []
    for item in tokens:
        stemmed.append(stemmer.stem(item))
    return stemmed


def tokenize(text):
    tokens = nltk.word_tokenize(text)
    '''
    Function to break up sentences/text into individual units (in this case, words)
    '''
    #After the text is divided into words, you stem each word and return the stems. 
    #stems = stem_tokens(tokens, stemmer)
    #return stems
    return tokens

 def remove_punctuation(file_in, file_out): 
 	'''
 	This preprocesses the text, incuding, lower-casing all words, removes punctuation and 
 	also removes numbers. Then saves out file with new fields with the cleaned words:
 	'descript_no_punc' & 'title_no_punc'.
 	Only have to run this once on all of your scaped data. 
 	'''
    #open up each each dictionary in the list of products and remove punctuation:
    with open(path + file_in) as f:
        data = json.load(f)#list of dictionaries. Each dictionary is an item for sale
        #for each dictionary (i.e., item for sale) in the dataset
        for item in data:
            lowercase_item_description = item['description'].lower()
            lowercase_title = item['title'].lower()
            item['color'] = item['color'].lower()
            #remove punctuation:
            #no_punctuation = lowercase_item_description.translate(None, string.punctuation)
            no_punctuation  = lowercase_item_description.translate(str.maketrans('','',string.punctuation))
            no_punctuation = no_punctuation.translate(str.maketrans('','','1234567890'))
            
            no_punctuation_title  = lowercase_title.translate(str.maketrans('','',string.punctuation))
            no_punctuation_title =  no_punctuation_title.translate(str.maketrans('','','1234567890'))
            
            item['descript_no_punc'] = no_punctuation
            item['title_no_punc'] = no_punctuation_title
        with open(path + file_out,'w') as out:
            json.dump(data, out)
        return data

def calculate_tfidf_matrix(file_in):
	'''
	Calculates the tf-idf matrix given a document corpus. In this case, the document corpus is
	going to be the item_descriptions from each of our items for sale on shopbop.com, which was 
	scraped for info. Adding color info to description as well (although not sure if this is being
	used in the way that I would like)
	'''
    description_dict = {}
    with open(path + file_in) as f:
        data = json.load(f)#list of dictionaries. Each dictionary is an item for sale
        #take info out of large dict that you want to place in smaller dict for tfidf analysis:
        for item in data:
            description_dict[item['url'] + '_' + item['color']]= item['descript_no_punc']  
            #description_dict[item['title_no_punc'] + ' ' + item['color']]= item['descript_no_punc']  
        # Run the tf-idf analysis using scikit-learn. 
        # Pass our own tokenize and stemming functions.
        # Using scikit-learns's functionality to remove stop words
        # print(len(description_dict))
        tfidf = TfidfVectorizer(tokenizer=tokenize, stop_words='english')
        tfs = tfidf.fit_transform(description_dict.values())
        #features = tfidf.get_feature_names()
        #print(len(features))
        return tfs, tfidf

#NOTE: must modify to take in the item[descript_no_punc] from any given item
#def tfidf_score_document(tfidf,desc_no_punc):
def tfidf_score_document(tfidf):
    desc_no_punc = "a boxy  phillip lim crossbody bag in soft leather slim back pocket a polished loop secures the top flap lined interior with  card slots chain shoulder strap dust bag included\nleather lambskin\nweight oz  kg\nimported china\nmeasurements\nheight in  cm\nlength in  cm\ndepth in  cm\nstrap drop in  cm"
    weights = tfidf.transform([desc_no_punc])
    feature_names = tfidf.get_feature_names()#gets word names
    return weights, feature_names

# Returns sparse matrix, [n_documents, n_words]
# Matrix contains the Tf-idf-weighted values.
# tuple (document_id,word_id) , tfidf score of word given corpus 
tfs,tfidf = calculate_tfidf_matrix('products_all_newline') #this is the corpus of all products in shopbop catalog. 
weights,feature_names = tfidf_score_document(tfidf)


#Return words & weights in terms of importance:
item_weights = {}
#for each word in weights matrix:
for col in weights.nonzero()[1]:
    item_weights[feature_names[col]]= weights[0, col]
#sort words from largest weight to smallest:
item_weights_sorted = [(k, item_weights[k]) for k in sorted(item_weights, key=item_weights.get, reverse=True)]
#print(item_weights_sorted)


