from django.db import models
from django.contrib.auth.models import User 

# Create your models here.
class Airport(models.Model):
    iata_code = models.CharField(max_length=3, unique=True)
    name = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)



class Passenger(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
    ]
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default='Unknown') 
    citizenship = models.CharField(max_length=100, default='Unknown') 
    first_name = models.CharField(max_length=100)  # Имя
    last_name = models.CharField(max_length=100)  # Фамилия
    # email = models.EmailField()  # Электронная почта
    passport_number = models.CharField(max_length=20)  # Номер паспорта
    birthday = models.DateField()  # Дата рождения
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"



class Airline(models.Model):
    name = models.CharField(max_length=100)  # Название авиакомпании
    code = models.CharField(max_length=10, unique=True)  # Код авиакомпании (например, SU для Aeroflot)

    def __str__(self):
        return self.name

class Flight(models.Model):
    flight_number = models.CharField(max_length=10)  # Номер рейса (например, SU123)
    airline = models.ForeignKey(Airline, on_delete=models.CASCADE)  # Связь с авиакомпанией
    departure_airport = models.ForeignKey('Airport', on_delete=models.CASCADE, related_name='departing_flights')  # Аэропорт вылета
    arrival_airport = models.ForeignKey('Airport', on_delete=models.CASCADE, related_name='arriving_flights')  # Аэропорт прилета
    departure_date = models.DateField()  # Дата вылета
    departure_time = models.TimeField()  # Время вылета
    arrival_date = models.DateField()  # Дата прилета
    arrival_time = models.TimeField()  # Время прилета
    aircraft = models.CharField(max_length=50)  # Тип самолёта (например, Boeing 737)
    duration = models.DurationField()  # Продолжительность полёта
    status = models.CharField(max_length=20, choices=[('Scheduled', 'Scheduled'), ('Delayed', 'Delayed'), ('Cancelled', 'Cancelled')])  # Статус рейса

    def __str__(self):
        return f"{self.airline.code} {self.flight_number} from {self.departure_airport} to {self.arrival_airport}"

class FlightPrice(models.Model):
    flight = models.ForeignKey(Flight, on_delete=models.CASCADE)  # Связь с рейсом
    travel_class = models.CharField(max_length=20, choices=[('Economy', 'Economy'), ('Business', 'Business'), ('First', 'First')])  # Класс обслуживания
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Цена билета для данного класса обслуживания

    def __str__(self):
        return f"{self.flight.flight_number} - {self.travel_class} Class: {self.price}"
    

class Ticket(models.Model):
    passenger = models.ForeignKey(Passenger, on_delete=models.CASCADE)  # Связь с пассажиром
    flight = models.ForeignKey(Flight, on_delete=models.CASCADE)  # Связь с рейсом (Flight — это другая модель)
    booking_date = models.DateTimeField(auto_now_add=True)  # Дата бронирования
    ticket_number = models.CharField(max_length=50, unique=True)  # Уникальный номер билета
    seat_number = models.CharField(max_length=5)  # Номер места
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Цена билета
    payment_status = models.CharField(max_length=20, choices=[('Paid', 'Paid'), ('Pending', 'Pending')])  # Статус оплаты
    ticket_status = models.CharField(max_length=20, choices=[('Confirmed', 'Confirmed'), ('Cancelled', 'Cancelled')])  # Статус билета

    def __str__(self):
        return f"Ticket {self.ticket_number} for {self.passenger}"
    
class Country(models.Model):
    name = models.CharField(max_length=100)  
    code = models.CharField(max_length=10, unique=True) 

    def __str__(self):
        return self.name