

import osmnx as ox
import matplotlib.pyplot as plt
import pandas as pd
import warnings
import math
warnings.filterwarnings("ignore", category=FutureWarning, module='osmnx')

# Define location and bounding box parameters
place_name = "Nyeri, Kenya"
latitude = -0.4371
longitude = 36.9580
placestub = place_name.lower().replace(' ', '-').replace(',','')

box_width = 0.1  # About 11 km
box_height = 0.1
north = latitude + box_height/2
south = latitude - box_height/2
west = longitude - box_width/2
east = longitude + box_width/2
bbox = (west, south, east, north)

# Define what data to retrieve
tags = {
    "amenity": True,
    "buildings": True,
    "historic": True,
    "leisure": True,
    "shop": True,
    "tourism": True,
    "religion": True,
    "memorial": True
}

# ACCESS: Retrieve all necessary data from OpenStreetMap
pois = ox.features_from_bbox(bbox, tags)
graph = ox.graph_from_bbox(bbox)
area = ox.geocode_to_gdf(place_name)
nodes, edges = ox.graph_to_gdfs(graph)
buildings = ox.features_from_bbox(bbox, tags={"building": True})

print(f"Retrieved {len(pois)} POIs")
