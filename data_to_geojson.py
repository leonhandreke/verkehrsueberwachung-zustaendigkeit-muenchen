#! /usr/bin/env python3

import yaml
import json
import requests

data = yaml.load(open("data.yaml", "r"))

geojson_features = []

for incident in data["incidents"]:

    r = requests.get(
    "http://nominatim.openstreetmap.org/search",
    params={
        "format": "jsonv2",
        "q": incident["address"] + ", Munich, Germany"
        })
    loc = (float(r.json()[0]["lon"]), float(r.json()[0]["lat"]))

    agency = data["agencies"][incident["agency"]]
    geojson_properties = { "agency": agency["name"], "marker-color": agency["color"] }
    if "address" in incident:
        geojson_properties["address"] = incident["address"]
    geojson_features.append({
        "type": "Feature",
        "geometry": {
            "type": "Point",
            "coordinates": [loc[0], loc[1]]
            },
        "properties": geojson_properties
        })

print(geojson_features)

with open("processed.geojson", "w") as outfile:
    json.dump({
        "type": "FeatureCollection",
        "features": geojson_features
        }, outfile)


