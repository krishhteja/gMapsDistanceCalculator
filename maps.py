import sys, os, json
import geopy.distance
import geocoder
import gmplot
import time

vehicle = 0
foot = 0
unknown = 0
tilting = 0
still = 0
countries = []
cities = []
locations = []
######Give the path of json file
with open('Location History.json') as json_file:  
    data = json.load(json_file)
    #Read latitude and longitude of first element
    latitude = data['locations'][0]['latitudeE7'] / 10000000
    longitude = data['locations'][0]['longitudeE7'] / 10000000
    
    for loc in data['locations']:
        nextLatitude = loc['latitudeE7'] / 10000000 
        nextLongitude = loc['longitudeE7'] / 10000000 
        coords_1 = (latitude, longitude)
        coords_2 = (nextLatitude, nextLongitude)
        if 'activity' in loc:
            activities = loc['activity'][0]['activity']
            confidenceList = []
            #Get activity with max confidence and consider activityType for that element
            for activity in activities:
                confidenceList.append(activity['confidence'])
                index = confidenceList.index(max(confidenceList))
                activityType = activities[index]['type']
                if activityType == 'TILTING':
                    tilting = tilting + geopy.distance.vincenty(coords_1, coords_2).km
                elif activityType == 'STILL':
                    still = still + geopy.distance.vincenty(coords_1, coords_2).km
                elif activityType == 'ON_FOOT':
                    foot = foot + geopy.distance.vincenty(coords_1, coords_2).km
                elif activityType == 'IN_VEHICLE':
                    vehicle = vehicle + geopy.distance.vincenty(coords_1, coords_2).km
                else: #All other types
                    unknown = unknown + geopy.distance.vincenty(coords_1, coords_2).km
            else:
                unknown = unknown + geopy.distance.vincenty(coords_1, coords_2).km
        #If distance between two points is greater than 10 km, add them to locations array for calculating number of countries and cities visited
        if geopy.distance.vincenty(coords_1, coords_2).km > 10:
            locMap = {}
            locMap['lat'] = nextLatitude
            locMap['lon'] = nextLongitude
            locations.append(locMap)
            
        #Store lat and lon to different variable for next iteration
        latitude = nextLatitude
        longitude = nextLongitude
    
    #As geocoder accepts one request per second, we iterate locations one per second
    for location in locations:
        print(location)
        g = geocoder.osm([location['lat'], location['lon']], method='reverse')
        if g.json:
            if 'city' in g.json:
                city = g.json['city']
                if not city in cities:
                    cities.append(city)
            if 'country' in g.json:
                country = g.json['country']
                if not country in countries:
                    countries.append(country)
        time.sleep(1)
    print("Distance travelled by foot is - " + str(foot))
    print("Distance travelled by tilting is - " + str(tilting))
    print("Distance travelled by still is - " + str(still))
    print("Distance travelled by vehicle is - " + str(vehicle))
    print("Distance travelled by unknown means is - " + str(unknown))
    total = foot+tilting+vehicle+unknown
    print("Total distance - " + str(total))

    #compare different circumference or distance
    earthCircumference = 40075
    earthMoon = 384400
    sun = 4379000
    mercury = 15329
    venus = 38025
    mars = 21344
    jupiter = 439264
    saturn = 378675
    uranus = 160590
    
    print(*cities, sep = ", ")  
    print("That is " + str(len(cities)) + " cities \n")
    print(*countries, sep = ", ")
    print("That is " + str(len(countries)) + " countries \n") 
    print("As per the data, it seems like, the distance you have travelled equals " + str(total/earthCircumference) + " times around the circumference of earth and " + str(total/earthMoon) + " times between earth and moon")
    print("Also, it's equal to " + str(total/sun) + " times circumference of the Sun")
    print(str(total/mercury) + " times circumference of the Mercury")
    print(str(total/venus) + " times circumference of the Venus")
    print(str(total/mars) + " times circumference of the Mars")
    print(str(total/jupiter) + " times circumference of the Jupiter")
    print(str(total/saturn) + " times circumference of the Saturn")
    print(str(total/uranus) + " times circumference of the Uranus")
    print("Great job! Keep going :)")
