from django.shortcuts import render
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View

class UserLoginView(LoginView):
    pass


@login_required
def exchange_selection(request):
    pass


class ExchangeDetailView(LoginRequiredMixin, View):
    pass