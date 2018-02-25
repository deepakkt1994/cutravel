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
	url(r'^genpdf$', hello.views.html_to_pdf_view, name='genpdf'),
	url(r'^JoinPlan$', hello.views.joinPlan, name='JoinPlan'),
    url(r'^$', hello.views.index, name='index'),
	url(r'^db', hello.views.db, name='db'),
    path('admin/', admin.site.urls),
]
