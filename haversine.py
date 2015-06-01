import math
from collections import namedtuple
import csv

City = namedtuple('City', ['name', 'latitude', 'longitude'])
Distance = namedtuple('Distance', ['start', 'end', 'length'])


def haversine(start, end):
    # radius of earth in miles
    R = 3963.1676
    start_lat = math.radians(start.latitude)
    start_cos = math.cos(start_lat)

    end_lat = math.radians(end.latitude)
    end_cos = math.cos(end_lat)

    lat_delta = math.radians(end.latitude - start.latitude)
    lat_delta_sin = math.sin(lat_delta/2)**2

    long_delta = math.radians(end.longitude - start.longitude)
    long_delta_sin = math.sin(long_delta/2)**2

    a = lat_delta_sin + (start_cos * end_cos * long_delta_sin)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    return R*c


def city_to_city(first, second):
    d = haversine(first, second)
    pretty_distance = '{0:.3f}'.format(d)
    return [Distance(first.name, second.name, pretty_distance),
            Distance(second.name, first.name, pretty_distance)]


def distances(cities):
    lengths = []
    for pos, city in enumerate(cities):
        for other_city in cities[pos+1:]:
            lengths.extend(city_to_city(city, other_city))
    return lengths


def get_cities():
    cities = []
    with open('cities.csv', 'r') as fp:
        for line in csv.reader(fp):
            name, _lat, _long = line
            cities.append(City(name, float(_lat), float(_long)))
    return cities


def calculate_distances():
    cities = get_cities()
    return distances(cities)


if __name__ == '__main__':
    with open('distances.csv', 'w', newline='') as fp:
        distance_writer = csv.writer(fp, delimiter=',')
        for row in calculate_distances():
            distance_writer.writerow(row)
