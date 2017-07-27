from sklearn.cluster import DBSCAN
from sklearn import metrics
from sklearn.datasets.samples_generator import make_blobs
from sklearn.preprocessing import StandardScaler
import numpy as np

path_file = "data/vectors_hour_2"

vectors = []
ids = []
with open(path_file, 'r') as v:
	for line in v:
		a = line.rstrip().split(',')
		ids.append(a[0])
		a.pop(0)
		vectors.append(a)

print(vectors)

vectors = StandardScaler().fit_transform(vectors)
print (vectors)
print (len(vectors))


db = DBSCAN(eps=0.3, min_samples=3).fit(vectors)
core_samples_mask = np.zeros_like(db.labels_, dtype=bool)
core_samples_mask[db.core_sample_indices_] = True
labels = db.labels_

print(db)
print(core_samples_mask)
print(labels)
print(ids)

for n, m in zip(ids, labels):
	print("ID: "+str(n)+"\t"+"ClusterID: "+str(m))





