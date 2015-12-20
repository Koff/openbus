from django.contrib import admin
from reservations.models import Reservation, User, Trip
from django.contrib.auth.admin import UserAdmin


class ReservationsInline(admin.TabularInline):
    model = Reservation


class TripAdmin(admin.ModelAdmin):
    def total_revenue(self):
        return sum([reservation.total_paid for reservation in self.reservation_set.all()])

    list_display = ('departure_city', 'arrival_city', 'departure_date', 'arrival_date', 'total_seats', 'available_seats'
                    , total_revenue, 'cost')
    readonly_fields = (total_revenue, 'available_seats')
    fields = ('departure_city', 'arrival_city', 'departure_date', 'arrival_date', 'total_seats', 'cost', readonly_fields)

    inlines = [ReservationsInline]


class OpenUserAdmin(UserAdmin):
    readonly_fields = ('date_joined', 'last_login')
    fields = ('first_name', 'last_name', 'email', 'password', 'phone_number', readonly_fields)
    fieldsets = ()
    list_display = ('id', 'first_name', 'last_name', 'email', 'phone_number')
    search_fields = ('first_name', 'last_name', 'email', 'phone_number')

    inlines = [ReservationsInline]

admin.site.register(Reservation)
admin.site.register(User, OpenUserAdmin)
admin.site.register(Trip, TripAdmin)


