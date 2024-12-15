from django.urls import path
from . import views


app_name = 'api'

urlpatterns = [
    path('exchange_list/', views.exchange_list, name='exchange_list'),

]
