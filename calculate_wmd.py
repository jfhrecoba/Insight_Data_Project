# First, we need to pre-process the documents.
# Import and download stopwords from NLTK.
from nltk.corpus import stopwords
from nltk import download
from nltk import word_tokenize
import json
from gensim.models import Word2Vec
from gensim.similarities import WmdSimilarity

path = '/Users/saraszczepanski/workspace/insight_project/data/'
file_in = 'products_all_newline' #final file with all products from shopbop
num_best = 5 #this is the number of products that the model will spit out/recommend. 

# Remove stopwords.
stop_words = stopwords.words('english')
#NOTE: need to check if uppercase matters
#add more useless words to the stop_words list, so they are removed from further processing
useless_words =['weight','oz','kg','mm','imported','china','measurements','height','length','depth','cm','drop',
'dust','included','vietnam','cannot','giftboxed','gift-boxed','made','greece','india','indonesia','imported','portugal',
'romania', "manufacturer's" ,'warranty','item','request', 'will', 'receive', 'response', 'hours','requested','customer',
'service','size','spain','france','brazil','circumference','pul','xs','philippines','l','korea','bangladesh', 'measurement',
'shopbop','xs/s']

stop_words.extend(useless_words)
#print(stop_words)
#download('stopwords')  # Download stopwords list.
#download('punkt')  # Download data for tokenizer.

def preprocess(doc):
	doc = doc.lower() # Lower the text.
	doc = word_tokenize(doc)  # Split into words.
	doc = [w for w in doc if not w in stop_words]  # Remove stopwords.
	doc = [w for w in doc if w.isalpha()]  # Remove numbers and punctuation.
	return doc

def build_initialize_wmd_model(path,file_in):
	'''
	Next, we need to put the corpus documents in a format that can be read 
	by the WMD model. Trains word2vec model on corpus. Lastly, this initializes
	the WMD (word mover's distance) model. '''
	w2v_corpus = [] # all of the item descriptions to train w2v model
	wmd_corpus = [] # Documents to run queries against (only one). ie, info from the item I want to find.
	documents = []  # wmd_corpus, with no pre-processing (so we can see the original documents).
	urls = []
	images = []
	with open(path + file_in) as f:
		data = json.load(f)#list of dictionaries. Each dictionary is an item for sale for each dictionary (i.e., item for sale) in the dataset
		for item in data:
			text = item['descript_no_punc'] + ' ' + item['color'] + ' '+ item['Item_type']
			documents.append(text)
			urls.append(item['url'])
			images.append(item['image'])
			# Pre-process document.
			text = preprocess(text)
			# Add to corpus for training Word2Vec.
			w2v_corpus.append(text)#word2vec corpus
			wmd_corpus.append(text)#query corpus
	#####BUILD THE MODEL########
	#from time import time
	#start = time()

	# Train Word2Vec on the corpus.
	model = Word2Vec(w2v_corpus, workers=3, size=100)

	# Initialize WmdSimilarity (search engine)
	instance = WmdSimilarity(wmd_corpus, model, num_best)
	#print('Cell took %.2f seconds to run.' % (time() - start))
	#takes about 3 sec to run this part of the code. possibly save out the instance?
	return model, instance

def query_wmd_model(description,instance):
	'''
	Input description of item (taken from scraped website) and return items that are most similar from shopbop corpus. 
	'''
	#start = time()
	#description = 'A Manna water bottle in marble-patterned stainless steel.' #Double wall insulation keeps drinks cold for 24 hours or hot for 12. Leak-proof lid. BPA free. white accessories'
	#description = 'A pajama-inspired RED Valentino top with contrast piping. Notched lapels frame the V neckline. Covered-button placket. Patch breast pocket. Short sleeves.\nFabric: Plain weave.\nShell: 100% silk.\nTrim: 100% polyester.\nDry clean.\nImported, Romania.\nMeasurements\nLength: 22in / 56cm, from shoulder\nMeasurements from size 40'
	query = preprocess(description)
	#this part takes a LONG time! need to improve this. 90 sec for two word description. 180 sec
	# for 10 word description. 
	sims = instance[query]  # A query is simply a "look-up" in the similarity class.
	#print('Cell took %.2f seconds to run.' % (time() - start))
	#print(sims)
	return sims

#Build and initial model:
model, instance = build_initialize_wmd_model(path,file_in)
#Calculate similarity between item of interest and items in corpus:
sims = query_wmd_model('A Manna water bottle in marble-patterned stainless steel.',instance)

# Print the query and the retrieved documents, together with their similarities.
print('Query:')
print(description)
for i in range(num_best):
    print()
    print('sim = %.4f' % sims[i][1])
    print(documents[sims[i][0]])
    print(urls[sims[i][0]])
    print(images[sims[i][0]])
