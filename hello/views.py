from django.shortcuts import render
from django.http import HttpResponse
import googlemaps	

from .models import Greeting

# Create your views here.
def index(request):
    # return HttpResponse('Hello from Python!')
    return render(request, 'index.html')

def getNearbyplaces(request):
	api_key = 'AIzaSyD5QetA8YsrJ-jvQFd1hfRNLoNpVM9MHYY'

	gmaps = googlemaps.Client(key=api_key)
	geocode_result = gmaps.geocode('Boulder, CO') #$_GET['source']
	latandlng=geocode_result[0]['geometry']['location']	
	out = gmaps.places_nearby(latandlng,50)
	places = out['results']
	waystops=[]
	for place in places:
		waystops.append(place)
	geocode_result = gmaps.geocode('Denver, CO') #$_GET['destination']
	latandlng=geocode_result[0]['geometry']['location']	
	out = gmaps.places_nearby(latandlng,50)
	places = out['results']
	for place in places:
		waystops.append(place)
	distance = gmaps.distance_matrix('Boulder, CO','Denver, CO')['rows'][0]['elements'][0]['distance']['value']
	#if(distance > 100000): add code to get mid point and calc nearby places again
	
	print(waystops)
	return waystops
def db(request):

    greeting = Greeting()
    greeting.save()

    greetings = Greeting.objects.all()

    return render(request, 'db.html', {'greetings': greetings})

