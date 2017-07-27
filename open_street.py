import osmnx as ox

#city = ox.gdf_from_place('beijing')
#ox.plot_shape(ox.project_gdf(city))

#G = ox.graph_from_place('beijing, china', network_type='drive')
#G_projected = ox.project_graph(G)
#ox.plot_graph(G_projected)

import osmnx as ox
gdf = ox.gdf_from_place('beijing, china')
point_geometry = gdf['geometry'].iloc[0]
center_point = (point_geometry.y, point_geometry.x)
G = ox.graph_from_point(center_point, distance=10000, network_type='drive')
G_projected = ox.project_graph(G)
ox.plot_graph(G_projected)
