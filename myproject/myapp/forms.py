from django.forms import ModelForm
from django import forms
from .models import Event


class EventForm(ModelForm):
    class Meta:
        model = Event
        exclude = ['user']  # Exclude the 'user' field from the form

    def __init__(self, *args, **kwargs):
        super(EventForm, self).__init__(*args, **kwargs)

    def save_with_user(self, user, commit=True):
        # Zapisz nowe wydarzenie, przypisując zalogowanego użytkownika do pola 'user'
        event = super(EventForm, self).save(commit=False)
        event.user = user
        if commit:
            event.save()
        return event
