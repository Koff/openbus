from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import TemplateView, FormView, CreateView, ListView
from .models import Reservation, User, Trip
from .forms import RegistrationForm, LogInForm
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib import messages


class LoginRequiredMixin(object):
    @classmethod
    def as_view(cls, **initkwargs):
        view = super(LoginRequiredMixin, cls).as_view(**initkwargs)
        return login_required(view)


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
                print("The password is valid, but the account has been disabled!")
        else:
            # the authentication system was unable to verify the username and password
            messages.add_message(self.request, messages.ERROR, 'Invalid username or password')
            print("The username and password were incorrect.")
            return render(request=self.request, template_name='reservations/login.html')

        return super(LogInView, self).form_valid(form)


class HomeView(LoginRequiredMixin, ListView):
    model = Trip
    queryset = Trip.objects.all().order_by('departure_date')[:5]
    template_name = 'reservations/home.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {'queryset': self.queryset})


class MyTripsView(LoginRequiredMixin, ListView):
    model = Trip
    template_name = 'reservations/my_trips.html'

    def get(self, request, *args, **kwargs):
        queryset = []
        reservations = Reservation.objects.all().filter(user_id_id=request.user.id)
        for reservation in reservations:
            trip = Trip.objects.all().filter(id=reservation.trip_id_id)[0]
            seat = reservation.seat
            queryset.append({'departure_city': trip.departure_city,
                             'arrival_city': trip.arrival_city,
                             'departure_date': trip.departure_date,
                             'arrival_date': trip.arrival_date,
                             'seat': seat})
        return render(request, self.template_name, {'queryset': queryset})


class Profile(LoginRequiredMixin, ListView):
    model = User
    template_name = 'reservations/profile.html'

    def get(self, request, *args, **kwargs):
        queryset = []
        print(request.user)
        return render(request, self.template_name, {'queryset': queryset})


class Logout(LoginRequiredMixin, ListView):
    template_name = 'reservations/login.html'

    def get(self, request, *args, **kwargs):
        logout(request)
        print(request.user)
        return redirect(to='login')
