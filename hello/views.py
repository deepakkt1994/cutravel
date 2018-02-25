from django.shortcuts import render
from django.http import HttpResponse
import googlemaps

from .models import Greeting

global_waystops=[]
# Create your views here.
def index(request):
    # return HttpResponse('Hello from Python!')
    if(request.GET.get('start')):
        return render(request,'StartPage.html')
    if(request.GET.get('join')):
        return render(request,'StartPage.html')

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

def db(request):

    greeting = Greeting()
    greeting.save()

    greetings = Greeting.objects.all()

    return render(request, 'db.html', {'greetings': greetings})

def startReq(request):
    print('RECEIVED REQUEST start: ', request.method)
    if request.method == 'POST':
        return render(request, 'PlanSelection.html')
    else:
        return render(request, 'StartPage.html')

def planSelect(request):
    print('RECEIVED REQUEST plan select: ', request.method)
    if request.method == 'POST':
        username = request.POST.get('name', '')
        print("Username: ", username)
        startpoint = request.POST.get('startpoint', '')
        print("startpoint: ", startpoint)
        endpoint = request.POST.get('endpoint', '')
        print("endpoint: ", endpoint)
        startdate = request.POST.get('startdate', '')
        print("startdate: ", startdate)
        numdays = request.POST.get('numdays', '')
        print("numdays: ", numdays)
        api_key = 'AIzaSyD5QetA8YsrJ-jvQFd1hfRNLoNpVM9MHYY'

        gmaps = googlemaps.Client(key=api_key)
        geocode_result = gmaps.geocode(startpoint) #$_GET['source']
        latandlng=geocode_result[0]['geometry']['location']
        out = gmaps.places_nearby(latandlng,50)
        places = out['results']
        waystops=[]
        for place in places:
            waystops.append(place)
        geocode_result = gmaps.geocode(endpoint) #$_GET['destination']
        latandlng=geocode_result[0]['geometry']['location']
        out = gmaps.places_nearby(latandlng,50)
        places = out['results']
        for place in places:
            waystops.append(place)
        distance = gmaps.distance_matrix(startpoint,endpoint)['rows'][0]['elements'][0]['distance']['value']
        #if(distance > 100000): add code to get mid point and calc nearby places again
        #context={'waystops':waystops}
        global_waystops=waystops 
        return render(request, 'PlanSelection.html', { 'waystops':waystops})
    else:
        return render(request, 'StartPage.html')

def addPlaces(request):
    return HttpResponse(str("test"))
#    print('RECEIVED REQUEST add places: ', request.method)
#    if request.method == "POST":

