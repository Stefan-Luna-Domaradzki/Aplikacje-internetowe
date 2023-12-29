from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User, auth
from django.contrib import messages
from .models import Feature
from .models import Event
from .forms import EventForm

# Create your views here.
def index(request):
    features = Feature.objects.all()

    return render(request, 'index.html', {'features': features})


def counter(request):
    words = request.POST['text']
    amount_of_words = len(words.split())
    return render(request, 'counter.html', {'amount': amount_of_words})


def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        if password == password2:
            if User.objects.filter(email=email).exists():
                messages.info(request, 'Email Already Used')
                return redirect('register')

            elif User.objects.filter(username=username).exists():
                messages.info(request, 'Username Already Used')
                return redirect('register')
            else:
                user = User.objects.create_user(username=username,
                                                email=email,
                                                password=password
                                                )
                user.save();
                return redirect('login')
        else:
            messages.info(request, 'Passwords Not The Same')
            return redirect('register')
    else:
        return render(request, 'register.html')


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('test_events')
        else:
            messages.info(request, 'Credentials Invalid')
            return redirect('login')

    else:
        return render(request, 'login.html')


def test_events(request):
    if request.user.is_authenticated:
        low_priority_events = Event.objects.filter(user=request.user, priority='low')
        medium_priority_events = Event.objects.filter(user=request.user, priority='medium')
        high_priority_events = Event.objects.filter(user=request.user, priority='high')

        return render(request, 'test_events.html', {
            'low_priority_events': low_priority_events,
            'medium_priority_events': medium_priority_events,
            'high_priority_events': high_priority_events,
            'username': request.user.username
        })
    else:
        return render(request, 'register.html')


def test_events2(request):
    if request.user.is_authenticated:
        low_priority_events = Event.objects.filter(user=request.user, priority='low')
        medium_priority_events = Event.objects.filter(user=request.user, priority='medium')
        high_priority_events = Event.objects.filter(user=request.user, priority='high')

        return render(request, 'test_events.html', {
            'low_priority_events': low_priority_events,
            'medium_priority_events': medium_priority_events,
            'high_priority_events': high_priority_events,
            'username': request.user.username
        })
    else:
        return render(request, 'register.html')


def add_event(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        details = request.POST.get('details')
        deadline = request.POST.get('deadline')
        priority = request.POST.get('priority')

        # Sprawdź, czy wszystkie pola zostały wypełnione
        if not name or not details or not deadline or not priority:
            messages.error(request, 'All fields are required.')
        else:
            # Stworzenie nowego obiektu Event i zapisanie go
            event = Event(
                user=request.user,  # Użytkownik zalogowany
                name=name,
                details=details,
                deadline=deadline,
                priority=priority
            )
            event.save()

            messages.success(request, 'Event added successfully.')

    return render(request, 'add_event.html')


def account_settings():
    return None