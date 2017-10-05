# First, we need to pre-process the documents.
# Import and download stopwords from NLTK.
from nltk.corpus import stopwords
from nltk import download
from nltk import word_tokenize

def preprocess(doc):
	# Remove stopwords.
    stop_words = stopwords.words('english')
	#NOTE: need to check if uppercase matters
	#add more useless words to the stop_words list, so they are removed from further processing
    useless_words =['weight','oz','kg','mm','imported','china','measurements','height','length','depth','cm','drop',
    'dust','included','vietnam','cannot','giftboxed','gift-boxed','made','greece','india','indonesia','portugal',
    'romania', "manufacturer's" ,'warranty','item','request', 'will', 'receive', 'response', 'hours','requested','customer',
    'service','size','spain','france','brazil','circumference','pul','xs','philippines','l','korea','bangladesh', 
    'usa','measurement','width','item','xss','shopbop','nordstrom']

    stop_words.extend(useless_words)
    doc = doc.lower() # Lower the text.
    doc = word_tokenize(doc)  # Split into words.
    doc = [w for w in doc if not w in stop_words]  # Remove stopwords.
    doc = [w for w in doc if w.isalpha()]  # Remove numbers and punctuation.
    return doc
