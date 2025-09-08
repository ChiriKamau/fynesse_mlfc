# ADDRESS: Create visualization to address spatial understanding needs
fig, ax = plt.subplots(figsize=(6,6))
area.plot(ax=ax, color="tan", alpha=0.5)
buildings.plot(ax=ax, facecolor="gray", edgecolor="gray")
edges.plot(ax=ax, linewidth=1, edgecolor="black", alpha=0.3)
nodes.plot(ax=ax, color="black", markersize=1, alpha=0.3)
pois.plot(ax=ax, color="green", markersize=5, alpha=1)
ax.set_xlim(west, east)
ax.set_ylim(south, north)
ax.set_title(place_name, fontsize=14)
plt.show()

# ADDRESS: Create reusable feature extraction function
features = [
    ("building", None),
    ("amenity", None),
    ("amenity", "school"),
    ("amenity", "hospital"),
    ("amenity", "restaurant"),
    ("amenity", "cafe"),
    ("shop", None),
    ("tourism", None),
    ("tourism", "hotel"),
    ("tourism", "museum"),
    ("leisure", None),
    ("leisure", "park"),
    ("historic", None),
    ("amenity", "place_of_worship"),
]

def get_feature_vector(latitude, longitude, box_size_km=2, features=features):
    """
    ADDRESS: Solution for extracting feature vectors from any location.
    
    Given a central point (latitude, longitude) and a bounding box size,
    query OpenStreetMap via OSMnx and return a feature vector.
    
    Parameters
    ----------
    latitude : float
        Latitude of the center point.
    longitude : float
        Longitude of the center point.
    box_size_km : float
        Size of the bounding box in kilometers
    features : list of tuples
        List of (key, value) pairs to count.
        
    Returns
    -------
    feature_vector : dict
        Dictionary of feature counts, keyed by (key, value).
    """
    # Convert box size to degrees (~111km per degree latitude)
    box_deg = box_size_km / 111
    north = latitude + box_deg / 2
    south = latitude - box_deg / 2
    east = longitude + box_deg / 2
    west = longitude - box_deg / 2
    bbox = (west, south, east, north)
    
    # Collect all unique keys needed
    keys = {k for k, _ in features}
    tags = {k: True for k in keys}
    
    # ACCESS data for this location
    pois = ox.features_from_bbox(bbox, tags=tags)
    
    # ASSESS and count features
    counts = {}
    for key, value in features:
        if key in pois.columns:
            if value:
                counts[f"{key}:{value}"] = (pois[key] == value).sum()
            else:
                counts[key] = pois[key].notnull().sum()
        else:
            counts[f"{key}:{value}" if value else key] = 0
    
    return counts

# ADDRESS: Define datasets for comparative analysis
cities_kenya = {
    "Nyeri, Kenya": {"latitude": -0.4371, "longitude": 36.9580},
    "Nairobi, Kenya": {"latitude": -1.2921, "longitude": 36.8219},
    "Mombasa, Kenya": {"latitude": -4.0435, "longitude": 39.6682},
    "Kisumu, Kenya": {"latitude": -0.0917, "longitude": 34.7680}
}

cities_england = {
    "Cambridge, England": {"latitude": 52.2053, "longitude": 0.1218},
    "London, England": {"latitude": 51.5072, "longitude": -0.1276},
    "Sheffield, England": {"latitude": 53.3811, "longitude": -1.4701},
    "Oxford, England": {"latitude": 51.7520, "longitude": -1.2577},
}

# ADDRESS: Example usage of the solution
print("\nExample feature vector extraction:")
nyeri_features = get_feature_vector(latitude, longitude, box_size_km=2)
for feature, count in nyeri_features.items():
    print(f"{feature}: {count}")
