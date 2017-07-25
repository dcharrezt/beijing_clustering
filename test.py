import pandas as pd
import gmaps
import stdbscan as st
from datetime import timedelta, datetime
from PIL import Image

filename = 'sample'

def parse_dates(x):
    return datetime.strptime(x, '%Y-%m-%d %H:%M:%S.%f')

df = pd.read_csv(filename,sep=";",converters={'DATATIME': parse_dates})
print (df)

#gmaps.density_plot(df['LATITUDE'], df['LONGITUDE'],)
gmaps.polygons(df['LATITUDE'], df['LONGITUDE'], df['CLUSTER'], "ms")
gmaps.density_plot(df['LATITUDE'], df['LONGITUDE'])
gmaps.heatmap(df['LATITUDE'], df['LONGITUDE'], df['CLUSTER'])
gmaps.scatter(df['LATITUDE'], df['LONGITUDE'], colors=df['CLUSTER'])

#export LD_LIBRARY_PATH=/usr/local/cuda-8.0/lib64
