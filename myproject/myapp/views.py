from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.models import User, auth
from django.contrib import messages
from .models import Feature
from .models import Event
from .forms import LoginForm
from django.contrib.auth import authenticate, login


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
        login_form = LoginForm(request.POST)

        if login_form.is_valid():
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']

            user = auth.authenticate(username=username, password=password)

            if user is not None:
                auth.login(request, user)
                return redirect('test_events')
            else:
                messages.info(request, 'Credentials Invalid')
                return redirect('login')
    else:
        login_form = LoginForm()

    context = {'LoginForm': login_form}
    return render(request, 'login.html', context)


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
        # Jeśli użytkownik nie jest zalogowany, możesz przekierować go na stronę logowania lub zaimplementować inne zachowanie.
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
        # Jeśli użytkownik nie jest zalogowany, możesz przekierować go na stronę logowania lub zaimplementować inne zachowanie.
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
            return redirect('add_event')

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
        return redirect('add_event') # Przekierowanie na tę samą stronę po dodaniu wydarzenia

    return render(request, 'add_event.html')


def account_settings():
    return None


def delete_event(request, event_id):
    # Pobierz obiekt zdarzenia
    event = get_object_or_404(Event, id=event_id)

    # Usuń zdarzenie
    event.delete()

    # Przekieruj do strony test_events po usunięciu
    return redirect('test_events')


def change_priority_higher(request, event_id):

    # Pobierz obiekt zdarzenia
    event = get_object_or_404(Event, id=event_id)

    # Zmień priorytet
    if event.priority == 'low':
        event.priority = 'medium'
    elif event.priority == 'medium':
        event.priority = 'high'


    # Zapisz zmiany
    event.save()

    # Przekieruj do strony test_events po zmianie priorytetu
    return redirect('test_events')


def change_priority_lower(request, event_id):

    # Pobierz obiekt zdarzenia
    event = get_object_or_404(Event, id=event_id)

    # Zmień priorytet
    if event.priority == 'medium':
        event.priority = 'low'
    elif event.priority == 'high':
        event.priority = 'medium'


    # Zapisz zmiany
    event.save()

    # Przekieruj do strony test_events po zmianie priorytetu
    return redirect('test_events')
