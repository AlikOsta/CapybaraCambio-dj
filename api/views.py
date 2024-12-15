from django.shortcuts import render
from rest_framework import generics
from app.models import Exchange
from .serializers import ExchangeSerializer


class ExchangeListAPI(generics.ListAPIView):
    exchanges_list = Exchange.objects.all()
    serializer_class = ExchangeSerializer
