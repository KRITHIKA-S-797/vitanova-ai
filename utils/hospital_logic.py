import requests
from math import radians, sin, cos, sqrt, atan2

HEADERS = {
    "User-Agent": "Arogya360AI/1.0 (educational project)"
}

def geocode_place(place_name):
    """
    Convert a place name into latitude and longitude using Nominatim.
    """
    url = "https://nominatim.openstreetmap.org/search"
    params = {
        "q": place_name,
        "format": "json",
        "limit": 1
    }

    response = requests.get(url, params=params, headers=HEADERS, timeout=20)
    response.raise_for_status()
    data = response.json()

    if not data:
        return None

    return {
        "lat": float(data[0]["lat"]),
        "lon": float(data[0]["lon"]),
        "display_name": data[0]["display_name"]
    }


def haversine_distance(lat1, lon1, lat2, lon2):
    """
    Calculate distance in kilometers between two lat/lon points.
    """
    r = 6371.0

    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)

    a = (
        sin(dlat / 2) ** 2
        + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon / 2) ** 2
    )
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    return round(r * c, 2)


def build_overpass_query(lat, lon, radius_meters, care_type):
    """
    Overpass query for hospitals, clinics, doctors, medical centres, etc.
    """
    amenity_values = []

    if care_type == "Emergency":
        amenity_values = ["hospital", "clinic", "doctors"]
    elif care_type == "Hospital":
        amenity_values = ["hospital"]
    elif care_type == "Clinic":
        amenity_values = ["clinic"]
    elif care_type == "Medical Centre":
        amenity_values = ["doctors", "clinic", "hospital"]
    else:
        amenity_values = ["hospital", "clinic", "doctors"]

    query_parts = []
    for amenity in amenity_values:
        query_parts.append(
            f'node["amenity"="{amenity}"](around:{radius_meters},{lat},{lon});'
        )
        query_parts.append(
            f'way["amenity"="{amenity}"](around:{radius_meters},{lat},{lon});'
        )
        query_parts.append(
            f'relation["amenity"="{amenity}"](around:{radius_meters},{lat},{lon});'
        )

    query = f"""
    [out:json][timeout:25];
    (
      {"".join(query_parts)}
    );
    out center tags;
    """
    return query


def fetch_nearby_medical_places(lat, lon, radius_km=5, care_type="All"):
    """
    Fetch nearby hospitals/clinics from Overpass API.
    """
    radius_meters = int(radius_km * 1000)
    query = build_overpass_query(lat, lon, radius_meters, care_type)

    url = "https://overpass-api.de/api/interpreter"
    response = requests.post(url, data=query, headers=HEADERS, timeout=40)
    response.raise_for_status()
    data = response.json()

    places = []

    for element in data.get("elements", []):
        tags = element.get("tags", {})

        name = tags.get("name", "Unnamed Medical Facility")
        amenity = tags.get("amenity", "medical")
        emergency = tags.get("emergency", "")
        phone = tags.get("phone", "Not available")
        address = ", ".join(
            [
                tags.get("addr:housenumber", ""),
                tags.get("addr:street", ""),
                tags.get("addr:suburb", ""),
                tags.get("addr:city", ""),
            ]
        ).strip(", ").replace(" ,", ",")

        if "lat" in element and "lon" in element:
            place_lat = float(element["lat"])
            place_lon = float(element["lon"])
        elif "center" in element:
            place_lat = float(element["center"]["lat"])
            place_lon = float(element["center"]["lon"])
        else:
            continue

        distance_km = haversine_distance(lat, lon, place_lat, place_lon)

        places.append({
            "name": name,
            "type": amenity.title(),
            "emergency": "Yes" if emergency else "No",
            "phone": phone,
            "address": address if address else "Address not available",
            "lat": place_lat,
            "lon": place_lon,
            "distance_km": distance_km
        })

    # Remove duplicates
    unique_places = []
    seen = set()

    for place in places:
        key = (
            place["name"].lower().strip(),
            round(place["lat"], 4),
            round(place["lon"], 4)
        )
        if key not in seen:
            seen.add(key)
            unique_places.append(place)

    unique_places.sort(key=lambda x: x["distance_km"])
    return unique_places


def filter_places(places, max_distance_km):
    """
    Filter by distance.
    """
    return [p for p in places if p["distance_km"] <= max_distance_km]


def recommend_best_place(places, care_type):
    """
    Simple ranking logic for best recommendation.
    """
    if not places:
        return None

    scored = []
    for place in places:
        score = 0

        # nearer is better
        score += max(0, 20 - place["distance_km"])

        # emergency gets extra for emergency searches
        if care_type == "Emergency" and place["emergency"] == "Yes":
            score += 10

        # hospitals get extra weight
        if place["type"].lower() == "hospital":
            score += 5

        # clinics still useful
        if place["type"].lower() == "clinic":
            score += 3

        scored.append((score, place))

    scored.sort(key=lambda x: x[0], reverse=True)
    return scored[0][1]