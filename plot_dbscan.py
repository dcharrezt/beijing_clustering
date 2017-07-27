import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import DBSCAN
from sklearn import metrics
from sklearn.datasets.samples_generator import make_blobs
from sklearn.preprocessing import StandardScaler

def Interpret(line):
	params=line.split(',')
	tid=params[0]
	cal=params[1]

	date=cal.split(' ')[0]
	ymd=date.split('-')
	yy=int(ymd[0])
	mo=int(ymd[1])
	dd=int(ymd[2])

	time=cal.split(' ')[1]
	hms=time.split(':')
	hh=int(hms[0])
	mm=int(hms[1])
	ss=int(hms[2])

	x=float(params[2])
	y=float(params[3])

	record={'id':tid,'date':date,'time':time,\
			'dt':{'yy':yy,'mo':mo,'dd':dd,'hh':hh,'mm':mm,'ss':ss},\
			'x':x,'y':y}
	return record

with open('data/data_dbscan_1', 'r') as f:
	X = []
	for line in f:
		tmp = Interpret(line)
		X.append([tmp['x'], tmp['y']])

Y = StandardScaler().fit_transform(X)
X = []
for i in Y:
	if (i[0] <= 1 and i[0] >= -1) and (i[1] <= 1 and i[1] >= -1):
		X.append([i[0], i[1]])

X = StandardScaler().fit_transform(X)
print(X)

# Compute DBSCAN
db = DBSCAN(eps=0.3, min_samples=20).fit(X)
core_samples_mask = np.zeros_like(db.labels_, dtype=bool)
core_samples_mask[db.core_sample_indices_] = True
labels = db.labels_

#print(db)
#print(core_samples_mask)
#print(labels)

# Number of clusters in labels, ignoring noise if present.
n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)

# Black removed and is used for noise instead.
unique_labels = set(labels)
colors = [plt.cm.Spectral(each)
          for each in np.linspace(0, 1, len(unique_labels))]
for k, col in zip(unique_labels, colors):
    if k == -1:
        # Black used for noise.
        col = [0, 0, 0, 1]

    class_member_mask = (labels == k)

    xy = X[class_member_mask & core_samples_mask]
    plt.plot(xy[:, 0], xy[:, 1], 'o', markerfacecolor=tuple(col),
             markeredgecolor='k', markersize=14)

    xy = X[class_member_mask & ~core_samples_mask]
    plt.plot(xy[:, 0], xy[:, 1], 'o', markerfacecolor=tuple(col),
             markeredgecolor='k', markersize=6)

plt.title('Estimated number of clusters: %d' % n_clusters_)
plt.show()
