from geopy.geocoders import Nominatim
geolocator = Nominatim(user_agent="specify_your_app_name_here")
location = geolocator.geocode("SAN DORLIGO DELLA VALLE")
print('location: ',location)
#print(location.address)
print((location.latitude, location.longitude))
#print(location.raw)
