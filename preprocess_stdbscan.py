from datetime import timedelta, datetime
from geopy.distance import great_circle

import math
import argparse
import time
import pandas as pd

import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import DBSCAN
from sklearn import metrics
from sklearn.datasets.samples_generator import make_blobs
from sklearn.preprocessing import StandardScaler

file_path = 'data/ms.csv'

def parse_dates(x):
    return datetime.strptime(x, '%Y-%m-%d %H:%M:%S')
    
def heatMap(long, lat, area, bins=200, smoothing=1, vmax=4, title=None):
    x = area.to_pixels(lat, long)[0]
    y = area.to_pixels(lat, long)[1]
    
    ax = area.show_mpl(figsize=(12, 10))
    
    heatmap, xedges, yedges = np.histogram2d(y, x, bins=bins)
    extent = [yedges[0], yedges[-1], xedges[-1], xedges[0]]
    
    logheatmap = np.log(heatmap)
    logheatmap[np.isneginf(logheatmap)] = 0
    logheatmap = ndimage.filters.gaussian_filter(logheatmap, smoothing, mode='nearest')
    
    output = ax.imshow(logheatmap, cmap=cmap, extent=extent, vmin=0, vmax=vmax)
    
    if title:
        ax.set_title(title, size=25)
        plt.savefig(title+'.png', bbox_inches='tight')
    
    print(np.amax(logheatmap))
    return output

#df2 = pd.read_csv(file_path)
#print df2
latMin = 39.8
latMax = 40
longMin = 116.2
longMax = 116.4


df = pd.read_csv(file_path,converters={'time': parse_dates})
query = df[(df['time'].dt.hour == 13) & (df['time'].dt.day == 2) & (df['time'].dt.minute == 50) \
			& (df.lat.between(latMin, latMax)) & (df.long.between(longMin, longMax))]

X = np.array(query[['lat','long']])



#dfBeijing = query[(query.lat.between(latMin, latMax)) & (query.long.between(longMin, longMax))]

#print(dfBeijing)

print(len(X))

X = StandardScaler().fit_transform(X)


# Compute DBSCAN
db = DBSCAN(eps=0.2, min_samples=20).fit(X)
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









