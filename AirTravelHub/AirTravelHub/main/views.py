from django.shortcuts import render, redirect
from .forms import SignUpForm
from .forms import PassengerForm
from django.contrib.auth import login, get_user_model
from .models import Flight
from django.db.models import Q
from django.http import JsonResponse
from .models import Country, Passenger

# мое
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
# from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.core.mail import send_mail
from django.urls import reverse
from AirTravelHub.settings import DEFAULT_FROM_EMAIL
from django.contrib import messages


def index(request):
    form = None
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
    


def flight_search(request):
    flights = Flight.objects.all()
    # Получаем данные из GET-запроса
    departure_airport = request.GET.get('from')  # Аэропорт вылета
    arrival_airport = request.GET.get('to')  # Аэропорт прилета
    departure_date = request.GET.get('date')  # Дата вылета

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
    
    return render(request, 'main/flight_search.html', {'flights': flights})

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

