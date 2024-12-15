from django.urls import path
from . import views


app_name = 'api'

urlpatterns = [
    path('v1/exchange_list/', views.ExchangeListAPI, name='exchange_list'),

]
