from django import forms
from captcha.fields import CaptchaField

class LoginCaptcha(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        fields = ('username', 'password', 'captcha')


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())
    captcha = CaptchaField()