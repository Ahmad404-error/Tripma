from django.shortcuts import render, redirect
from .forms import SignUpForm
from .forms import PassengerForm
from django.contrib.auth import login
from .models import Flight
from django.db.models import Q
from django.http import JsonResponse
from .models import Country


def index(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        is_valid = form.is_valid()
        if is_valid:
            user = form.save()
            login(request, user)
            # Добавьте редирект или сообщение об успехе здесь
            return redirect('home')  # Замените 'success_url' на нужный вам URL
        else:
            # Обработка ошибки формы
            pass
    else:
        form = SignUpForm()
    return render(request, 'main/index.html', {'form': form})


def flight_search(request):
    flights = Flight.objects.all()

    # Получаем данные из GET-запроса
    departure_airport = request.GET.get('from')  # Аэропорт вылета
    arrival_airport = request.GET.get('to')  # Аэропорт прилета
    departure_date = request.GET.get('date')  # Дата вылета

    if departure_airport:
        flights = flights.filter(
            Q(departure_airport__name__icontains=departure_airport) |
            Q(departure_airport__iata_code__icontains=departure_airport)
        )

    if arrival_airport:
        flights = flights.filter(
            Q(arrival_airport__name__icontains=arrival_airport) |
            Q(arrival_airport__iata_code__icontains=arrival_airport)
        )

    if departure_date:
        flights = flights.filter(departure_date=departure_date)
    
    return render(request, 'main/flight_search.html', {'flights': flights})

def account(request):
    if request.method == 'POST':
        form = PassengerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')  # Перенаправляем на страницу успеха
        else:
            print(form.errors)
    else:
        form = PassengerForm()

    return render(request, 'main/account.html', {'form': form})

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
