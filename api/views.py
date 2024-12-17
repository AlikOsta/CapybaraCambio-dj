from django.shortcuts import render
from rest_framework.generics import ListAPIView
from rest_framework.generics import RetrieveAPIView
from rest_framework.views import APIView
from app.models import Exchange, SubLocation, Currency, ExchangePair, DeliveryExchange
from .serializers import ExchangeSerializer, SubLocationSerializer, CurrencySerializer, ExchangePairSerializer
from rest_framework.response import Response


class CurrencyCityListAPI(APIView):
    def get(self, request, *args, **kwargs):
        currency = Currency.objects.all()
        city = SubLocation.objects.all()

        return Response({'currency': CurrencySerializer(currency, many=True).data, 'city': SubLocationSerializer(city, many=True).data})
    
    
class ExchangePairListAPI(APIView):
    def get(self, request, *args, **kwargs):
        exchange_pair = ExchangePair.objects.all()

        return Response({'exchange_pair': ExchangePairSerializer(exchange_pair, many=True).data})


class ExchangeDetailAPI(RetrieveAPIView):
    queryset = Exchange.objects.select_related('city', 'delivery__currency_delivery', 'delivery__template')
    serializer_class = ExchangeSerializer


class ExchangeListAPI(ListAPIView):
    queryset = Exchange.objects.select_related('city', 'delivery__currency_delivery', 'delivery__template')
    serializer_class = ExchangeSerializer