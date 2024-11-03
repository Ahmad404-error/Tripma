from django.shortcuts import render, redirect
from .forms import SignUpForm
from .forms import PassengerForm
from .forms import TicketForm
from django.contrib.auth import login, get_user_model
from .models import Flight
from django.db.models import Q
from django.http import JsonResponse
from .models import Country, Passenger, Ticket, Airport, Card
from datetime import datetime
from django.contrib.auth.decorators import login_required

# мое
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.core.mail import send_mail
from django.urls import reverse
from AirTravelHub.settings import DEFAULT_FROM_EMAIL
from django.contrib import messages



def index(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False  # Отключаем активность до подтверждения почты
            user.set_password(form.cleaned_data['password1'])
            user.save()
            form.send_confirmation_email(request, user)
            messages.success(request, 'Письмо для подтверждения регистрации отправлено на вашу почту.')
            return redirect('login')
    else:
        form = SignUpForm()
    return render(request, 'main/index.html', {'form': form})    
    # if request.method == 'POST':
    #     form = SignUpForm(request.POST)
    #     is_valid = form.is_valid()
    #     if is_valid:
    #         user = form.save()
    #         login(request, user)
    #         # Добавьте редирект или сообщение об успехе здесь
    #         return redirect('home')  # Замените 'success_url' на нужный вам URL
    #     else:
    #         # Обработка ошибки формы
    #         pass
    # else:
    #     form = SignUpForm()
    # return render(request, 'main/index.html', {'form': form})
    


def flights(request):
    form = SignUpForm
    flights = Flight.objects.all()
    # Получаем данные из GET-запроса
    departure_airport = request.GET.get('from')  # Аэропорт вылета
    arrival_airport = request.GET.get('to')  # Аэропорт прилета
    departure_date = request.GET.get('date')  # Дата вылета
    data = list(range(1, 61))  # Метки по оси X

    if departure_airport:
        flights = flights.filter(
            Q(departure_airport__name__icontains=departure_airport) |
            Q(departure_airport__iata_code__icontains=departure_airport) |
            Q(departure_airport__city__icontains=departure_airport)
        )

    if arrival_airport:
        flights = flights.filter(
            Q(arrival_airport__name__icontains=arrival_airport) |
            Q(arrival_airport__iata_code__icontains=arrival_airport) |
            Q(arrival_airport__city__icontains=arrival_airport)
        )

    if departure_date:
        flights = flights.filter(departure_date=departure_date)
    
    return render(request, 'main/flights.html', {'flights': flights, 'form': form, 'data': data})

@login_required 
def document(request):
    try:
        passenger = Passenger.objects.get(user=request.user)
        return render(request, 'main/account_details.html', {'passenger': passenger})
    
    except:
        if request.method == 'POST':
            form = PassengerForm(request.POST)
            if form.is_valid():
                passenger = form.save(commit=False)
                passenger.user = request.user
                passenger.save()
                return redirect('home')  # Перенаправляем на страницу успеха
            else:
                print(form.errors)
        else:
            form = PassengerForm()

        return render(request, 'main/account.html', {'form': form})

@login_required
def document_redact(request):
    if request.method == 'POST':
        form = PassengerForm(request.POST)
        gender = request.POST.get('gender')
        citizenship = request.POST.get('citizenship')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        passport_number = request.POST.get('passport_number')
        birthday = request.POST.get('birthday')

        middle = request.POST.get('middle')
        suffix = request.POST.get('suffix')
        phone_number = request.POST.get('phone_number')
        redress_number = request.POST.get('redress_number')
        travel_number = request.POST.get('travel_number')
        bag = request.POST.get('bag')
        email = request.POST.get('email')

        first_name_add = request.POST.get('first_name_add')
        last_name_add = request.POST.get('last_name_add')
        email_add = request.POST.get('email_add')
        phone_number_add = request.POST.get('phone_number_add')

        departure = request.POST.get('departure_airport')
        arrival = request.POST.get('arrival_airport')
        departureDate = request.POST.get('departure_date')
        departureTime = request.POST.get('departure_time')
        arrivalTime = request.POST.get('arrival_time')
        airline = request.POST.get('airline')
        flight = request.POST.get('flight')
        taxes = request.POST.get('taxes')
        price = request.POST.get('price')
        total = request.POST.get('total')
        logo = request.POST.get('logo')
        cityDeparture = request.POST.get('cityDeparture')
        countryDeparture = request.POST.get('countryDeparture')
        cityArrival = request.POST.get('cityArrival')
        countryArrival = request.POST.get('countryArrival')
        passenger = Passenger.objects.get(user = request.user)
        if gender:
            passenger.gender = gender
        if citizenship or citizenship=='':
            passenger.citizenship = citizenship
        if first_name:
            passenger.first_name = first_name
        if last_name:
            passenger.last_name = last_name
        if passport_number or passport_number=='':
            passenger.passport_number = passport_number
        if birthday or birthday =='':
            passenger.birthday = birthday
        if middle or middle == '':
            passenger.middle = middle
        if suffix or suffix=='':
            passenger.suffix = suffix
        if phone_number:
            passenger.phone_number = phone_number
        if redress_number or redress_number=='':
            passenger.redress_number = redress_number
        if travel_number:
            passenger.travel_number = travel_number
        if bag or bag =='':
            passenger.bag = bag
        if email:
            passenger.email = email
        if first_name_add:
            passenger.first_name_add = first_name_add
        if last_name_add:
            passenger.last_name_add = last_name_add
        if email_add:
            passenger.email_add = email_add
        if phone_number_add:
            passenger.phone_number_add = phone_number_add

        if departure:
            passenger.departure_airport = departure
        if arrival:
            passenger.arrival_airport = arrival
        if departureDate:
            passenger.departure_date = departureDate
        if departureTime:
            passenger.departure_time = departureTime
        if arrivalTime:
            passenger.arrival_time = arrivalTime
        if airline:
            passenger.airline = airline
        if flight:
            passenger.flight = flight
        if taxes:
            passenger.taxes = taxes
        if price:
            passenger.price = price
        if total:
            passenger.total = total
        if logo:
            passenger.logo = logo
        if cityDeparture:
            passenger.cityDeparture = cityDeparture
        if cityArrival:
            passenger.cityArrival = cityArrival
        if countryDeparture:
            passenger.countryDeparture = countryDeparture
        if countryArrival:
            passenger.countryArrival = countryArrival
        passenger.save()
        return redirect('home')  # Перенаправляем на страницу успеха

    else:
        form = PassengerForm()
    return render(request, 'main/account_details.html', {'form': form})
    

def country_autocomplete(request):
    if 'term' in request.GET:
        term = request.GET.get('term')
        countrys = Country.objects.filter(name__icontains=term)[:10]

        results = []
        for country in countrys:
            results.append({
                'label': country.name,
                'value': country.name,
            })
        return JsonResponse(results, safe=False)
    
    return JsonResponse([], safe=False)

User = get_user_model()

def activate_account(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Ваш аккаунт активирован! Теперь вы можете войти.')
        return redirect('home')
    else:
        messages.error(request, 'Ссылка активации недействительна.')
        return redirect('register')

def send_confirmation_email(request, user):
    token = default_token_generator.make_token(user)
    uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
    current_site = get_current_site(request)
    
    activation_link = reverse('activate', kwargs={'uidb64': uidb64, 'token': token})
    full_activation_link = f'http://{current_site.domain}{activation_link}'
    
    subject = 'Подтверждение регистрации'
    message = render_to_string('main/registration/confirmation_email.html', {
        'user': user,
        'activation_link': full_activation_link,
    })
    
    send_mail(subject, message, DEFAULT_FROM_EMAIL , [user.email])


def passenger_info(request):
    flightNumber = request.GET.get('flightNumber')
    departureAirport = request.GET.get('departureAirport')
    arrivalAirport = request.GET.get('arrivalAirport')
    logo = request.GET.get('logo')
    airline = request.GET.get('airline')
    departureDate = request.GET.get('departureDate')
    departureTime = request.GET.get('departureTime')
    arrivalTime = request.GET.get('arrivalTime')
    taxes = request.GET.get('taxes')
    price = request.GET.get('price')
    total = request.GET.get('total')

    user = request.user
    first_name = request.POST.get('first_name')
    last_name = request.POST.get('last_name')
    birthday = request.POST.get('birthday')

    passenger = Passenger.objects.get(user = request.user)
    email = user.email
    phone_number = request.POST.get('phone_number')
    middle = request.POST.get('middle')
    suffix = request.POST.get('suffix')
    redress_number = request.POST.get('redress_number')
    travel_number = request.POST.get('travel_number')
    bag = request.POST.get('bag')

    first_name_add = request.POST.get('first_name_add')
    last_name_add = request.POST.get('last_name_add')
    email_add = request.POST.get('email_add')
    phone_number_add = request.POST.get('phone_number_add')

    cityDeparture = request.GET.get('cityDeparture')
    cityArrival = request.GET.get('cityArrival')
    countryDeparture = request.GET.get('countryDeparture')
    countryArrival = request.GET.get('countryArrival')
    return render(request, 'main/passenger_info.html', {'flightNumber': flightNumber, 'logo': logo, 'airline': airline, 'departureAirport': departureAirport,
                                                         'departureDate': departureDate, 'departureTime': departureTime, 'arrivalAirport': arrivalAirport,
                                                         'arrivalTime': arrivalTime, 'price': price, 'total': total, 'taxes': taxes,
                                                         'first_name': first_name, 'last_name': last_name, 'birthday': birthday,
                                                         'passenger': passenger, 'email': email, 'phone_number': phone_number, 'middle': middle, 'suffix': suffix, 
                                                         'redress_number': redress_number, 'travel_number': travel_number, 'bag': bag, 'first_name_add': first_name_add,
                                                         'last_name_add':last_name_add, 'email_add': email_add, 'phone_number_add': phone_number_add,
                                                         'cityDeparture':cityDeparture, 'cityArrival': cityArrival, 'countryDeparture': countryDeparture, 'countryArrival': countryArrival})


def seat(request):
    passenger = Passenger.objects.get(user = request.user)
    airport = Airport.objects.all()
    return render(request, 'main/seat.html', {'passenger': passenger, 'airport': {airport}})

def payment(request):
    if request.method == 'POST':
        form = TicketForm(request.POST)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.passenger = Passenger.objects.get(user=request.user)
            ticket.total = int(ticket.price) + 121
            ticket.cls = round(int(ticket.price)-(int(ticket.price)/1.8), 2)
            passenger = Passenger.objects.get(user = request.user)
            ticket.save()
            return render(request, 'main/payment.html', {'form': form, 'ticket': ticket, 'passenger': passenger})
        else:
            passenger = Passenger.objects.get(user = request.user)
            error = str('Choose seat')
            return render(request, 'main/seat.html', {'passenger': passenger, 'error': error})
    else:
        form = TicketForm()
    return render(request, 'main/home.html', {'form': form})

def card(request):
    if request.method == 'POST':
        errors = {}
        name = request.POST.get('name')
        passenger = Passenger.objects.get(user=request.user)
        number = request.POST.get('number')
        date = request.POST.get('date')
        ccv = request.POST.get('ccv')

        if len(number) != 16 or not number.isdigit():
            errors['number'] = "Card number must be 16 digits long."
        if len(date) != 5 or date[2] != '/':
            errors['date'] = "Expiration date must be in YY/MM format."
        if len(ccv) != 3 or not ccv.isdigit():
            errors['ccv'] = "CCV must be 3 digits long."

        # Если есть ошибки, возвращаем на ту же страницу с ошибками
        if errors:
            ticket = Ticket.objects.filter(passenger__user=request.user).last()
            if ticket:
                ticket.total = int(ticket.price) + 121
                ticket.cls = round(int(ticket.price) - (int(ticket.price) / 1.8), 2)
            name = request.POST.get('name')
            number = request.POST.get('number')
            date = request.POST.get('date')
            ccv = request.POST.get('ccv')
            print(name, number, date, ccv)
            return render(request, 'main/payment.html', {'errors': errors, 'passenger':passenger, 'ticket': ticket, 'name': name, 'number': number, 'date': date, 'ccv': ccv})
        else:
            card = Card(
            passenger=passenger,
            name=name, 
            number=number, 
            date=date, 
            ccv=ccv)
            card.save()
            return redirect('success')  # Перенаправление на страницу успеха

    return render(request, 'main/payment.html')  # Отображение страницы с формой


@login_required
def passenger_data(request):
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'User not authenticated'}, status=403)
    else:
        passenger = Passenger.objects.get(user = request.user)
        passenger_data = {
            'id': passenger.id,
            'gender': passenger.gender,
            'citizenship': passenger.citizenship,
            'first_name': passenger.first_name,
            'last_name': passenger.last_name,
            'passport_number': passenger.passport_number,
            'birthday': passenger.birthday,

            'middle': passenger.middle,
            'suffix': passenger.suffix,
            'phone_number': passenger.phone_number,
            'redress_number': passenger.redress_number,
            'travel_number': passenger.travel_number,
            'bag': passenger.bag,
            'email': passenger.email,

            'first_name_add': passenger.first_name_add,
            'last_name_add': passenger.last_name_add,
            'email_add': passenger.email_add,
            'phone_number_add': passenger.phone_number_add,

            'departure': passenger.departure_airport,
            'arrival': passenger.arrival_airport,
            'departureDate': passenger.departure_date,
            'departureTime': passenger.departure_time,
            'arrivalTime': passenger.arrival_time,
            'airline': passenger.airline,
            'flight': passenger.flight,
            'taxes': passenger.taxes,
            'price': passenger.price,
            'total': passenger.total,
            'logo': passenger.logo,
        }
        return JsonResponse(passenger_data)
    
def success(request):
    return render(request, 'main/success.html')