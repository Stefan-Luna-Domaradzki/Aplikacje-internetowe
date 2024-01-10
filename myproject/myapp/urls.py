from django.urls import path
from . import views

# all the urls in our project
urlpatterns = [
    path('', views.register, name='register'),
    path('index', views.index, name='index'),
    path('register', views.register, name='register'),
    path('login', views.login, name='login'),
    path('test_events', views.test_events, name='test_events'),
    path('test_events2', views.test_events2, name='test_events2'),
    path('account_info', views.index, name='account_info'),
    path('add_event', views.add_event, name='add_event'),
    path('account_settings', views.account_settings, name='account_settings'),
    path('logout', views.login, name='logout'),
    path('delete_event/<int:event_id>/', views.delete_event, name='delete_event'),
    
]