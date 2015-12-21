from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.urlresolvers import reverse
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django.core.mail import send_mail


class UserManager(BaseUserManager):
    def create_user(self, first_name='', last_name='', email='', phone_number='', password=None):

        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(email=self.normalize_email(email),)

        user.set_password(password)
        user.first_name = first_name
        user.last_name = last_name
        user.phone_number = phone_number
        user.is_active = False

        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        user = self.create_user(email, password=password)
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    """
    Custom user class.
    """
    email = models.EmailField(_('email address'), unique=True, db_index=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(_('staff status'), default=False)
    date_joined = models.DateTimeField(default=timezone.now)
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=30, blank=True)
    phone_number = models.CharField(_('phone number'), max_length=30, blank=True)
    username = models.CharField(_('username'), max_length=30, blank=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __unicode__(self):
        return self.email

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def get_full_name(self):
        """
        Returns the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        """
        Returns the short name for the user.
        """
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        send_mail(subject, message, from_email, [self.email], **kwargs)

    def get_absolute_url(self):
        return reverse('user', kwargs={'pk': self.pk})


class Trip(models.Model):
    id = models.AutoField(primary_key=True)
    departure_city = models.CharField(max_length=100, blank=False)
    departure_address = models.CharField(max_length=254, blank=False, default='Comedores Universitarios de Fuentenueva '
                                                                              'Calle Rector Marín Ocete, s/n, 18071 '
                                                                              'Granada, Spain')
    departure_address_url = models.URLField(max_length=254, blank=False, default='https://goo.gl/maps/U2YjHAnupps')
    arrival_city = models.CharField(max_length=100, blank=False)
    arrival_address_url = models.URLField(max_length=254, blank=False, default='https://goo.gl/maps/eNjTxV7BcRU2')
    arrival_address = models.CharField(max_length=254, blank=False, default='Estacion de Autobuses de Ronda'
                                                                            'Plaza de Concepción García Redondo, '
                                                                            's/n, 29400 Ronda, Málaga, Spain')
    departure_date = models.DateTimeField()
    arrival_date = models.DateTimeField()
    total_seats = models.IntegerField(default=0, blank=True)
    public_price = models.DecimalField(max_digits=6, decimal_places=2, default=0.0, blank=False)
    cost = models.DecimalField(max_digits=6, decimal_places=2, default=0.0, blank=False)

    def __str__(self):
        return '%s -> %s departing at %s' % (self.departure_city, self.arrival_city, self.departure_date)

    def available_seats(self):
        return self.total_seats - self.reservation_set.count()


class Reservation(models.Model):
    user_id = models.ForeignKey(User)
    trip_id = models.ForeignKey(Trip)
    seat = models.CharField(max_length=10, blank=True)
    total_paid = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return '%s: %s -> %s on %s' % (self.user_id.get_full_name(),
                                       self.trip_id.departure_city,
                                       self.trip_id.arrival_city,
                                       self.trip_id.departure_date)

