from django.http import HttpResponseRedirect
from django.views.generic import TemplateView, FormView, CreateView, ListView
from .models import Reservation, User, Trip
from .forms import RegistrationForm, LogInForm, ProfileForm
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib import messages
from django.utils import timezone
from django.contrib.auth.mixins import LoginRequiredMixin


class ReserveView(TemplateView):
    model = Reservation
    template_name = 'reservations/base.html'


class RegistrationComplete(TemplateView):
    template_name = 'registration/registration_complete.html'


class UserCreate(CreateView):
    model = User
    fields = ['first_name', 'last_name', 'email', 'phone_number', 'password']
    template_name = 'registration/registration_form.html'

    def get(self, request, *args, **kwargs):
        registration_form = RegistrationForm()
        registration_form.prefix = 'registration/registration_form'
        return self.render_to_response(context={})

    def post(self, request, *args, **kwargs):
        post_data = self.request.POST.dict()
        registration_form = RegistrationForm(post_data)

        if registration_form.is_valid():
            User.objects.create_user(first_name=post_data.get('first_name'),
                                     last_name=post_data.get('last_name'),
                                     email=post_data.get('email'),
                                     phone_number=post_data.get('phone_number'),
                                     password=post_data.get('password'))
            return HttpResponseRedirect(reverse('registration_complete'))
        else:
            return self.form_invalid(registration_form, **kwargs)


class LogInView(FormView):
    template_name = 'reservations/login.html'
    form_class = LogInForm
    success_url = '/'

    def form_valid(self, form):
        user = authenticate(email=form.data['email'], password=form.data['password'])
        if user is not None:
            # the password verified for the user
            if user.is_active:
                login(self.request, user)
                print("User is valid, active and authenticated")
                return redirect(to='home')
            else:
                messages.add_message(self.request, messages.ERROR, 'Your account has been suspended...')
        else:
            messages.add_message(self.request, messages.ERROR, 'Invalid username or password')
            return render(request=self.request, template_name='reservations/login.html')

        return super(LogInView, self).form_valid(form)


class HomeView(LoginRequiredMixin, ListView):
    login_url = '/login/'
    model = Trip
    past_trips = Trip.objects.all().filter(departure_date__lt=timezone.now()).order_by('departure_date')[:5]
    upcoming_trips = Trip.objects.all().filter(departure_date__gt=timezone.now()).order_by('departure_date')[:5]
    template_name = 'reservations/home.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {'upcoming_trips': self.upcoming_trips,
                                                    'past_trips': self.past_trips})


class MyTripsView(LoginRequiredMixin, ListView):
    login_url = '/login/'
    model = Trip
    template_name = 'reservations/my_trips.html'

    def get(self, request, *args, **kwargs):
        upcoming_trips = []
        past_trips = []
        reservations = Reservation.objects.all().filter(user_id_id=request.user.id)
        for reservation in reservations:
            trip = Trip.objects.all().filter(id=reservation.trip_id_id)[0]
            if trip.arrival_date >= timezone.now():
                seat = reservation.seat
                upcoming_trips.append({'departure_city': trip.departure_city,
                                       'arrival_city': trip.arrival_city,
                                       'departure_date': trip.departure_date,
                                       'arrival_date': trip.arrival_date,
                                       'seat': seat})
            elif trip.arrival_date < timezone.now():
                seat = reservation.seat
                past_trips.append({'departure_city': trip.departure_city,
                                   'arrival_city': trip.arrival_city,
                                   'departure_date': trip.departure_date,
                                   'arrival_date': trip.arrival_date,
                                   'seat': seat})
        return render(request, self.template_name, {'upcoming_trips': upcoming_trips, 'past_trips': past_trips})


class Profile(LoginRequiredMixin, FormView):
    login_url = '/login/'
    form_class = ProfileForm
    template_name = 'reservations/profile.html'

    def form_valid(self, form):
        user = self.request.user
        user.first_name = form.data['first_name']
        user.last_name = form.data['last_name']
        user.save()
        return render(self.request, 'reservations/profile.html', {'queryset': self.request.user})

    def form_invalid(self, form):
        messages.add_message(self.request, messages.ERROR, 'Something went wrong...')
        return render(request=self.request, template_name=self.template_name)

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {'queryset': request.user})


class Logout(LoginRequiredMixin, ListView):
    template_name = 'reservations/login.html'

    def get(self, request, *args, **kwargs):
        logout(request)
        print(request.user)
        return redirect(to='login')


class NewReservation(LoginRequiredMixin, ListView):
    template_name = 'reservations/new_reservation.html'
    trip_dict = {}

    def get(self, request, *args, **kwargs):
        trip_id = self.args[0]
        trip = Trip.objects.all().filter(id=trip_id).first()

        return render(request=request, template_name=self.template_name)
