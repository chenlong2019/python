import pandas as pd
import numpy as np
import os
import folium
from folium import plugins  
import webbrowser
import geopandas as gp
full = pd.read_excel("F:/日报/22复查/其他复查反馈情况.xls")
full = full.dropna()
schools_map = folium.Map(location=[full['X'].mean(), full['Y'].mean()], zoom_start=10)
marker_cluster = plugins.MarkerCluster().add_to(schools_map)
for name,row in full.iterrows():
     folium.Marker([row["X"], row["Y"]], popup="{0}:{1}".format(row["责任单位"], row["复查整改情况"])).add_to(marker_cluster)     
#folium.RegularPolygonMarker([row["lat"], row["lon"]], popup="{0}:{1}".format(row["cities"], row["GDP"]),number_of_sides=10,radius=5).add_to(marker_cluster)
schools_map
schools_map.save('f1.html')
webbrowser.open('f1.html')