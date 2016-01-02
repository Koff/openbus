from django.conf.urls import include, url
from django.contrib import admin
from reservations.views import ReserveView, LogInView, HomeView, MyTripsView, Profile, Logout, NewReservation
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
    url(r'^new_reservation/([0-9]{0,6})', view=NewReservation.as_view(), name='new_reservation'),
]
