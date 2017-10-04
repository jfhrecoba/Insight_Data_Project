import json
files = ['products_nord_shoes_1','products_nord_shoes_2']
# files = ['products_2']
products_all = []
for file in files:
    #open file:
    with open('/Users/saraszczepanski/workspace/insight_project/data/{}'.format(file)) as f:
        data = json.load(f)
    products_all.extend(data)
#save out 
with open('/Users/saraszczepanski/workspace/insight_project/data/products_nord_shoes_all', 'w') as out:
    json.dump(products_all, out)