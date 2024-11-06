from django.contrib import admin

# Register your models here.
from .models import Passenger, Airline, Flight, Airport, Ticket, FlightPrice, Country, Card, ShareEmail
from .models import CustomUser

admin.site.register(CustomUser)


@admin.register(Passenger)
class MyModelAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name')  # Определите, какие поля отображать в списке

@admin.register(Country)
class MyModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'code')  # Определите, какие поля отображать в списке

@admin.register(Airline)
class MyModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'code')  # Определите, какие поля отображать в списке


@admin.register(Flight)
class MyModelAdmin(admin.ModelAdmin):
    list_display = ('flight_number', 'airline')  # Определите, какие поля отображать в списк


@admin.register(Airport)
class MyModelAdmin(admin.ModelAdmin):
    list_display = ('iata_code', 'name', 'city')  # Определите, какие поля отображать в списке


@admin.register(Ticket)
class MyModelAdmin(admin.ModelAdmin):
    list_display = ('passenger', 'seat_number')  # Определите, какие поля отображать в списке


@admin.register(FlightPrice)
class MyModelAdmin(admin.ModelAdmin):
    list_display = ('flight', 'price')  # Определите, какие поля отображать в списке

@admin.register(Card)
class MyModelAdmin(admin.ModelAdmin):
    list_display = ('passenger', 'name', 'number', 'date', 'ccv')  # Определите, какие поля отображать в списке

@admin.register(ShareEmail)
class MyModelAdmin(admin.ModelAdmin):
    list_display = ('passenger', 'email')  # Определите, какие поля отображать в списке

