# Initial data exploration
print("POI data structure:")
print(pois.head())

# Convert to DataFrame for easier analysis
pois_df = pd.DataFrame(pois)
pois_df['latitude'] = pois_df.apply(lambda row: row.geometry.centroid.y, axis=1)
pois_df['longitude'] = pois_df.apply(lambda row: row.geometry.centroid.x, axis=1)

# Assess tourist places specifically
tourist_places_df = pois_df[pois_df.tourism.notnull()]
print(f"Found {len(tourist_places_df)} tourist places")
print("Tourist places:")
print(tourist_places_df)

# Define POI types for systematic assessment
poi_types = [
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

# ASSESS: Count different types of POIs
poi_counts = {}
for key, value in poi_types:
    if key in pois_df.columns:
        if value:  # count only that value
            poi_counts[f"{key}:{value}"] = (pois_df[key] == value).sum()
        else:  # count any non-null entry
            poi_counts[key] = pois_df[key].notnull().sum()
    else:
        poi_counts[f"{key}:{value}" if value else key] = 0

poi_counts_df = pd.DataFrame(list(poi_counts.items()), columns=["POI Type", "Count"])
print("POI Assessment Summary:")
print(poi_counts_df)
