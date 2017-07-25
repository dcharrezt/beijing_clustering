from datetime import timedelta, datetime
from geopy.distance import great_circle

import math
import argparse
import time
import pandas as pd

def st_dbscan(df, spatial_threshold, temporal_threshold, min_neighbors):
    """
    Python st-dbscan implementation.
    INPUTS:
        df={o1,o2,...,on} Set of objects
        spatial_threshold = Maximum geographical coordinate (spatial) distance
        value
        temporal_threshold = Maximum non-spatial distance value
        min_neighbors = Minimun number of points within Eps1 and Eps2 distance
    OUTPUT:
        C = {c1,c2,...,ck} Set of clusters
    """
    cluster_label = 0
    noise = -1
    unmarked = 777777
    stack = []

    # initialize each point with unmarked
    df['cluster'] = unmarked

    # for each point in database
    for index, point in df.iterrows():
        if df.loc[index]['cluster'] == unmarked:
            neighborhood = retrieve_neighbors(index, df, spatial_threshold,
                                              temporal_threshold)

            if len(neighborhood) < min_neighbors:
                df.set_value(index, 'cluster', noise)
            else:  # found a core point
                cluster_label += 1
                # assign a label to core point
                df.set_value(index, 'cluster', cluster_label)

                # assign core's label to its neighborhood
                for neig_index in neighborhood:
                    df.set_value(neig_index, 'cluster', cluster_label)
                    stack.append(neig_index)  # append neighborhood to stack

                # find new neighbors from core point neighborhood
                while len(stack) > 0:
                    current_point_index = stack.pop()
                    new_neighborhood = retrieve_neighbors(
                        current_point_index, df, spatial_threshold,
                        temporal_threshold)

                    # current_point is a new core
                    if len(new_neighborhood) >= min_neighbors:
                        for neig_index in new_neighborhood:
                            neig_cluster = df.loc[neig_index]['cluster']
                            if all([neig_cluster != noise,
                                    neig_cluster == unmarked]):
                                # TODO: verify cluster average
                                # before add new point
                                df.set_value(neig_index, 'cluster',
                                             cluster_label)
                                stack.append(neig_index)
    return df

def retrieve_neighbors(index_center, df, spatial_threshold, temporal_threshold):
    neigborhood = []

    center_point = df.loc[index_center]

    # filter by time 
    min_time = center_point['DATATIME'] - timedelta(minutes=temporal_threshold)
    max_time = center_point['DATATIME'] + timedelta(minutes=temporal_threshold)
    df = df[(df['DATATIME'] >= min_time) & (df['DATATIME'] <= max_time)]

    # filter by distance
    for index, point in df.iterrows():
        if index != index_center:
            distance = great_circle(
                (center_point['LATITUDE'], center_point['LONGITUDE']),
                (point['LATITUDE'], point['LONGITUDE'])).meters
            if distance <= spatial_threshold:
                neigborhood.append(index)

    return neigborhood

def parse_dates(x):
    return datetime.strptime(x, '%Y-%m-%d %H:%M:%S.%f')

def main(day, hour):

    filename = 'data/ms.csv'

    df = pd.read_csv(filename,sep=";",converters={'DATATIME': parse_dates})
    print ( df[(df['DATATIME'].dt.hour == 2) & (df['DATATIME'].dt.day == 1) & (df['DATATIME'].dt.minute == 3)] )
#    print df[df['DATATIME'].dt.day == 1]
    
    num_ids = len(df)
    print ( "Len:{}\n---".format(num_ids) ) 

    numFrag = 4

    # STBSCAN
    spatial_threshold   = 500
    temporal_threshold  = 60
    minPts              = 5

    result_df = st_dbscan(  df, spatial_threshold,
                            temporal_threshold, minPts)
    print ("Finished")

    import time
    timestr = time.strftime("%Y%m%d-%H%M%S")
    result_df['cluster'].to_csv("result_{}_{}_{}_{}.csv".format(spatial_threshold,
                                                                temporal_threshold,
                                                                minPts,
                                                                timestr)
                                                                )


if __name__ == "__main__":
    main()
