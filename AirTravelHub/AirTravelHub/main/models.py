from django.db import models
from django.contrib.auth.models import User, AbstractUser, Group, Permission

# Create your models here.
class Airport(models.Model):
    iata_code = models.CharField(max_length=3, unique=True)
    name = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)

    def __str__(self):
        return f"{self.city}"


class CustomUser(AbstractUser):
    # Добавляем related_name, чтобы избежать конфликта с моделью User по умолчанию
    is_active = models.BooleanField(default=False)  # Отключаем аккаунт до подтверждения
    passport_number = models.CharField(max_length=10, verbose_name="Паспортные данные", help_text="Введите номер паспорта", default="huy")
    groups = models.ManyToManyField(
        Group,
        related_name='customuser_set',  # Уникальное related_name для предотвращения конфликта
        blank=True,
        help_text='Группы, к которым принадлежит этот пользователь.',
        verbose_name='группы',
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='customuser_permissions_set',  # Уникальное related_name для предотвращения конфликта
        blank=True,
        help_text='Конкретные разрешения для этого пользователя.',
        verbose_name='разрешения пользователя',
    )

class Passenger(models.Model):
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
    ]
    gender = models.CharField(max_length=6, choices=GENDER_CHOICES, default='Gender') 
    citizenship = models.CharField(max_length=100, default='citizenship') 
    first_name = models.CharField(max_length=100)  # Имя
    last_name = models.CharField(max_length=100)  # Фамилия
    passport_number = models.CharField(max_length=20)  # Номер паспорта
    birthday = models.CharField(max_length=10)  # Дата рождения

    email = models.EmailField(default='Unknown')  # Электронная почта
    phone_number = models.CharField(max_length=16, default='Unknown')
    middle = models.CharField(max_length=100, default='Unknown')
    suffix = models.CharField(max_length=100, default='Unknown')
    redress_number = models.CharField(max_length=100, default='Unknown')
    travel_number = models.CharField(max_length=100, default='Unknown')
    bag = models.CharField(max_length=100, default=0)

    #Дополнительная информация
    first_name_add = models.CharField(max_length=100, default='Unknown')  # Имя
    last_name_add = models.CharField(max_length=100, default='Unknown')  # Фамилия
    email_add = models.EmailField(default='Unknown')  # Электронная почта
    phone_number_add = models.CharField(max_length=16, default='Unknown')

    # Поля, связанные с рейсом
    departure_airport = models.CharField(max_length=100, default='Unknown')
    arrival_airport = models.CharField(max_length=100, default='Unknown')
    departure_date = models.CharField(max_length=20, default='1000-01-01')  # Дата вылета
    departure_time = models.CharField(max_length=20, default='00:00:00')  # Время вылета
    arrival_time = models.CharField(max_length=20, default='00:00:00')  # Время прилета
    logo = models.CharField(max_length=100, default='Unknown')  # Логотип авиакомпании
    airline = models.CharField(max_length=100, default='Unknown')
    flight = models.CharField(max_length=100, default='Unknown')
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)  # Цена за билет
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)  # Общая стоимость
    taxes = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    cityDeparture = models.CharField(max_length=100, default='Unknown')
    countryDeparture = models.CharField(max_length=100, default='Unknown')
    cityArrival = models.CharField(max_length=100, default='Unknown')
    countryArrival = models.CharField(max_length=100, default='Unknown')

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
    departure_time = models.TimeField(null=True)  # Время вылета
    arrival_date = models.DateField()  # Дата прилета
    arrival_time = models.TimeField(null=True)  # Время прилета
    aircraft = models.CharField(max_length=50)  # Тип самолёта (например, Boeing 737)
    duration = models.DurationField()  # Продолжительность полёта
    status = models.CharField(max_length=20, choices=[('Scheduled', 'Scheduled'), ('Delayed', 'Delayed'), ('Cancelled', 'Cancelled')])  # Статус рейса
    price_history = models.JSONField(blank=True, null=True)

    def __str__(self):
        return self.flight_number

class FlightPrice(models.Model):
    flight = models.ForeignKey(Flight, on_delete=models.CASCADE)  # Связь с рейсом
    travel_class = models.CharField(max_length=20, choices=[('Economy', 'Economy'), ('Business', 'Business'), ('First', 'First')])  # Класс обслуживания
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Цена билета для данного класса обслуживания

    def __str__(self):
        return f"{self.flight.flight_number} - {self.travel_class} Class: {self.price}"
    

class Ticket(models.Model):
    passenger = models.ForeignKey(Passenger, on_delete=models.CASCADE)  # Связь с пассажиром
    flight = models.CharField(max_length=50, unique=False)  # Связь с рейсом (Flight — это другая модель)
    booking_date = models.DateTimeField(auto_now_add=False)  # Дата бронирования
    ticket_number = models.CharField(max_length=50, unique=False)  # Уникальный номер билета
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