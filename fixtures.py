import json

import haversine

cities = haversine.get_cities()
distances = haversine.distances(cities)

city_ids = {city.name: pk+1 for pk, city in enumerate(cities)}


def locations_fixture(cities):
    model_name = 'distances.location'
    locations = []
    for pos, city in enumerate(cities):
        pk = pos + 1
        locations.append({
            'model': model_name,
            'pk': pk,
            'fields': {
                'name': city.name,
                'latitude': city.latitude,
                'longitude': city.longitude
            }
        })
    return locations


def trips_fixture(dists):
    model_name = 'distances.trip'
    trips = []
    for pos, trip in enumerate(dists):
        pk = pos + 1
        trips.append({
            'model': model_name,
            'pk': pk,
            'fields': {
                'start': city_ids[trip.start],
                'end': city_ids[trip.end],
                'length': float(trip.length)
            }
        })
    return trips


def save_locations(locs, filename):
    with open(filename, 'w') as fp:
        json.dump(locs, fp, indent=2)


def save_trips(trips, filename):
    with open(filename, 'w') as fp:
        json.dump(trips, fp, indent=2)

if __name__ == '__main__':
    locations = locations_fixture(cities)
    save_locations(locations, 'locations.json')
    trips = trips_fixture(distances)
    save_trips(trips, 'trips.json')
