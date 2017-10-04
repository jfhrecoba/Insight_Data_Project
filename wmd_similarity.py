import numpy

from gensim import interfaces
from gensim.models import Word2Vec
from gensim.models import Doc2Vec
from gensim.models.doc2vec import TaggedDocument
 
from multiprocessing import Pool

num_processes = 8

class WmdSimilarity(interfaces.SimilarityABC):
    """
   Document similarity (like MatrixSimilarity) that uses the negative of WMD
   as a similarity measure. See gensim.models.word2vec.wmdistance for more
   information.
 
   When a `num_best` value is provided, only the most similar documents are
   retrieved.
 
   When using this code, please consider citing the following papers:
 
   .. Ofir Pele and Michael Werman, "A linear time histogram metric for improved SIFT matching".
   .. Ofir Pele and Michael Werman, "Fast and robust earth mover's distances".
   .. Matt Kusner et al. "From Word Embeddings To Document Distances".
 
   Example:
       # See Tutorial Notebook for more examples https://github.com/RaRe-Technologies/gensim/blob/develop/docs/notebooks/WMD_tutorial.ipynb
       >>> # Given a document collection "corpus", train word2vec model.
       >>> model = word2vec(corpus)
       >>> instance = WmdSimilarity(corpus, model, num_best=10)
       >>> # Make query.
       >>> query = 'Very good, you should seat outdoor.'
       >>> sims = instance[query]
   """
    def __init__(self, corpus, w2v_model, num_best=None, normalize_w2v_and_replace=True, chunksize=256):
        """
       corpus:                         List of lists of strings, as in gensim.models.word2vec.
       w2v_model:                      A trained word2vec model.
       num_best:                       Number of results to retrieve.
       normalize_w2v_and_replace:      Whether or not to normalize the word2vec vectors to length 1.
       """
        self.corpus = corpus
        self.w2v_model = w2v_model
        self.num_best = num_best
        self.chunksize = chunksize
 
        # Normalization of features is not possible, as corpus is a list (of lists) of strings.
        self.normalize = False
 
        # index is simply an array from 0 to size of corpus.
        self.index = numpy.array(range(len(corpus)))
 
        if normalize_w2v_and_replace:
            # Normalize vectors in word2vec class to length 1.
            w2v_model.init_sims(replace=True)
 
    def __len__(self):
        return len(self.corpus)
 
    def get_similarities(self, query):
        """
       **Do not use this function directly; use the self[query] syntax instead.**
       """
        if isinstance(query, numpy.ndarray):
            # Convert document indexes to actual documents.
            query = [self.corpus[i] for i in query]
 
        if not isinstance(query[0], list):
            query = [query]
 
        n_queries = len(query)
        result = []
        for qidx in range(n_queries):
            qresult = self.get_sim_for_query(query[qidx])
            result.append(qresult)
 
        if len(result) == 1:
            # Only one query.
            result = result[0]
        else:
            result = numpy.array(result)
 
        return result
 
 
    def get_sim_for_query(self, query):
        # Compute similarity for each query.
 
        calc = WMDistanceCalculator(self.w2v_model, query)
        pool = Pool(processes=num_processes, maxtasksperchild=10)
        #qresult = pool.map(calc.wmdistance, self.corpus) #calculate WMDistance
        qresult = pool.map(calc.n_similarity, self.corpus) #calculate cosine similarity
        pool.close()
        # qresult = [self.w2v_model.wv.wmdistance(document, query) for document in self.corpus]
        qresult = numpy.array(qresult)
        #return 1. / (1. + qresult)  #WMDistance- return lowest numbers. Similarity is the negative of the distance.
        return qresult #Cosine Sim- return highest numbers.
 
 
    def __str__(self):
        return "%s<%i docs, %i features>" % (self.__class__.__name__, len(self), self.w2v_model.wv.syn0.shape[1])
#endclass WmdSimilarity
 
 
class WMDistanceCalculator:

    def __init__(self, w2v_model, query):
        self.w2v_model = w2v_model
        self.query = query
 

    def wmdistance(self, document):
        return self.w2v_model.wv.wmdistance(document, self.query)


    def n_similarity(self, document):
        d_words = []
        q_words = []
        vocab = self.w2v_model.wv.vocab
        for token in document:
          if (token in vocab):
            d_words.append(token)

        for token in self.query:
          if (token in vocab):
            q_words.append(token)
 
        if len(d_words) == 0:
          return 0

        if len(q_words) == 0:
          return 0
 
        return self.w2v_model.wv.n_similarity(d_words, q_words)

