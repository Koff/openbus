"""openbus URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from reservations.views import ReserveView, LogInView, HomeView, MyTripsView, Profile, Logout
from reservations import urls as reservations_url


urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^reservation/', view=ReserveView.as_view()),
    url(r'^account/', include(reservations_url)),
    url(r'^login/', view=LogInView.as_view(), name='login'),
    url(r'^home/', view=HomeView.as_view(), name='home'),
    url(r'^my_trips/', view=MyTripsView.as_view(), name='my_trips'),
    url(r'^logout/', view=Logout.as_view(), name='logout'),
    url(r'^profile/', view=Profile.as_view(), name='profile'),
]
