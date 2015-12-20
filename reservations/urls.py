"""openbus URL Configuration
"""
from django.conf.urls import include, url
from django.contrib import admin
from reservations.views import ReserveView, UserCreate, RegistrationComplete


urlpatterns = [
    url(r'^register/', view=UserCreate.as_view()),
    url(r'^register/submit_registration_form/', view=UserCreate.as_view()),
    url(r'^registration_complete/', view=RegistrationComplete.as_view(), name='registration_complete'),
]
