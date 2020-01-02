from geopy.geocoders import Nominatim
geolocator = Nominatim(user_agent="specify_your_app_name_here")
location = geolocator.geocode("Dolegna del collio")
print(location.address)
print((location.latitude, location.longitude))
print(location.raw)
