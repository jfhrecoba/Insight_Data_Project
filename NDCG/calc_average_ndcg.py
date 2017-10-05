import numpy as np
from ndcg import dcg_at_k, ndcg_at_k

k=3 #k =10 

all_r = [
[3, 2, 2, 1, 2, 1, 1, 3, 1, 2], #item 1 ranking in rank order
[2, 0, 1, 1, 3, 3, 1, 1, 2, 1], #item 2 ranking in rank order,  etc...
[2, 2, 2, 1, 2, 3, 2, 1, 2, 1],
[3, 3, 2, 2, 1, 1, 1, 2, 1, 3],
[2, 2, 2, 1, 1, 1, 1, 1, 1, 1],
[3, 3, 3, 3, 3, 3, 2, 1, 1, 1],
[3, 3, 3, 3, 3, 3, 3, 3, 2, 2],
[3, 3, 2, 2, 2, 2, 1, 1, 1, 0],
[2, 3, 2, 2, 2, 3, 2, 0, 1, 1],
[3, 3, 1, 0, 0, 0, 1, 0, 0, 0],
[3, 3, 3, 3, 1, 1, 1, 1, 1, 1],
[2, 1, 2, 2, 1, 1, 1, 0, 0, 0],
[3, 3, 3, 3, 2, 1, 3, 2, 2, 2],
[3, 2, 3, 2, 2, 1, 2, 2, 2, 2],
[3, 3, 3, 1, 3, 2, 3, 2, 1, 1]
]

all_ndcg =[]
for i, r in enumerate(all_r):
	ndcg= ndcg_at_k(r, k, method=1)
	all_ndcg.append(ndcg)

avg_ndcg = np.sum(all_ndcg)/len(all_ndcg)
stdev_ndcg = np.std(all_ndcg)
#std_err_ndcg = stdev_ndcg/np.sqrt(len(all_ndcg))
std_err_ndcg = stdev_ndcg/np.sqrt(50)

print(avg_ndcg)
print(std_err_ndcg)
print(all_ndcg)

