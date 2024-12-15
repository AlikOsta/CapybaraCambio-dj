from django.urls import path
from .views import ExchangeListAPI, CurrencyCityListAPI, ExchangePairListAPI, ExchangeDetailAPI


urlpatterns = [
    path('v1/exchange/', ExchangeListAPI.as_view(), name='exchange-list'),
    path('v1/exchange/<uuid:pk>/', ExchangeDetailAPI.as_view(), name='exchange-detail'),
    path('v1/currency-city/', CurrencyCityListAPI.as_view(), name='currency-city-list'),
    path('v1/exchange-pair/', ExchangePairListAPI.as_view(), name='exchange-pair-list'),
]
