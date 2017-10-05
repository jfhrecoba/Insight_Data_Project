from preprocess_words import preprocess
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