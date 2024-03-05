import json

def convert_to_geojson(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    features = []

    for entry in data:
        properties = {
            "kod": entry.get("kod", ""),
            "postadress": entry.get("postadress", ""),
            "postnummer": entry.get("postnummer", ""),
            "telefon": entry.get("telefon", ""),
            "epost": entry.get("epost", ""),
            "namn": entry.get("namn", "")
        }

        geometry = entry.get("geometry", {"coordinates": []})
        coordinates = geometry.get("coordinates", [])

        feature = {
            "type": "Feature",
            "properties": properties,
            "geometry": {
                "type": "MultiPolygon",
                "coordinates": [coordinates]
            }
        }
        features.append(feature)  

    geojson_data = {
        "type": "FeatureCollection",
        "features": features
    }

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(geojson_data, f, indent=2,ensure_ascii=False)

# Example usage:
input_file = 'counties/lan.json'
output_file = 'counties/lan.geojson'
convert_to_geojson(input_file, output_file)
