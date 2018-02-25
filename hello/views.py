from django.shortcuts import render
from django.http import HttpResponse
import googlemaps

from .models import Greeting


import urllib.request
import json

class gmap_wrapper:
    def __init__(self):
        self.key_google_direction="AIzaSyD5QetA8YsrJ-jvQFd1hfRNLoNpVM9MHYY"
        self.key_google_embeded="AIzaSyB2uz-9zoyW7GgkytCGnt636POGkTJyZuU"
        self.key_google_geocoding="AIzaSyDzaIPhbF4dYeu_wvBlWPL40dqAia4Hfioself"
    
    #input: origin_str: str; dest_str: str, ways_point list of str, str should not contain " ", instead use "+"
    #output: the order of ways_point (list of int, start from 0), not including origin_str/dest_str,
    #         i.e. same size with ways_point
    def get_direction_order(self, origin_str, dest_str, ways_point):
        if(ways_point==None):
            waypt=""
        else:
            waypt="|".join(ways_point)
            waypt="optimize:true|"+waypt
        url="https://maps.googleapis.com/maps/api/directions/json?"+ \
           "origin="+ origin_str+ \
           "&destination="+dest_str+ \
           "&waypoints="+waypt+ \
           "&key="+self.key_google_direction
#        print(url)
        res=urllib.request.urlopen(url)
        data=json.load(res)
#        print(data['routes'][0]['waypoint_order'])
        return(data['routes'][0]['waypoint_order'])


global_waystops=[]
global_src=""
global_dest=""
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
    global global_waystops, global_src, global_dest
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
        #request.session['waystops']=waystops
        global_waystops=waystops
        global_src=startpoint.replace(' ','+')
        global_dest=endpoint.replace(' ','+')
        dct=dict()
        dct['waystops']=waystops
        dct['source']=global_src
        dct['dest']=global_dest
        return render(request, 'PlanSelection.html', dct)
    elif request.method == 'GET':
        #waystops=request.session.get('waystops')
        selected_waypoints=[]
        n_waypts=len(global_waystops)
        print(n_waypts)
        for i in range(n_waypts):
            varname="checkbox"+str(i)
            if(request.GET.get(varname)):
                selected_waypoints.append(global_waystops[i])
        print(selected_waypoints)
        waystops_name=[]
        for wpt in selected_waypoints:
            waystops_name.append(wpt["name"].replace(' ','+'))
        print(waystops_name)
        gm=gmap_wrapper()
        order=gm.get_direction_order(global_src, global_dest, waystops_name)
        print(order)
        reordered=[waystops_name[i] for i in order]
        dct=dict()
        dct['waystops']='|'.joint(reordered)
        dct['source']=global_src
        dct['dest']=global_dest
        return render(request, 'PlanSelection.html', dct)
    else:
        return render(request, 'StartPage.html')
