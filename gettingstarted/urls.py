from django.conf.urls import include, url
from django.urls import path

from django.contrib import admin
admin.autodiscover()

import hello.views

# Examples:
# url(r'^$', 'gettingstarted.views.home', name='home'),
# url(r'^blog/', include('blog.urls')),

urlpatterns = [
    url(r'^start$', hello.views.startReq, name='startReq'),
    url(r'^PlanSelection$', hello.views.planSelect, name='PlanSelection'),
    url(r'^$', hello.views.index, name='index'),
    url(r'^places_gmap$', hello.views.addPlaces, name='addPlaces'),
	
        url(r'^db', hello.views.db, name='db'),
    path('admin/', admin.site.urls),
]
