#!/usr/bin/env python

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


if __name__ == "__main__":
    z=gmap_wrapper()
    order=z.get_direction_order("Boulder+CO", "Denver+CO", ["Broomfield+CO", "Thorton+CO", "Westminster+CO"])
    print(order)
        
