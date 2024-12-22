from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin

from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required

from django.core.exceptions import ValidationError
from django.db import transaction
from django.views import View

from . import services 
from .forms_handlers import prepare_delivery_form
from .handlers import handle_form

from . import forms
from . import models


class UserLoginView(LoginView):
    template_name = 'app/login.html'
    authentication_form = forms.CustomAuthenticationForm 

    def get_success_url(self):
        return reverse_lazy('app:exchange_selection')
    
    def dispatch(self, request, *args, **kwargs):
        """Переадресация авторизованных пользователей"""
        if request.user.is_authenticated:
            return redirect('app:exchange_selection')
        return super().dispatch(request, *args, **kwargs)  
    


@login_required
def exchange_selection(request):
    exchange_price = models.Exchange._meta.get_field('price').default

    if request.method == 'POST':
        form = forms.ExchangeForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                with transaction.atomic():
                    new_exchange = form.save(commit=False)
                    new_exchange.pk = None
                    new_exchange.owner = request.user
                    new_exchange.save()
                    return redirect('app:login')
            except ValidationError as e:
                form.add_error(None, str(e))
    else:
        form = forms.ExchangeForm(initial={'owner': request.user, 'city': models.SubLocation.objects.first()})

    context=  {
        'user_exchanges': models.Exchange.objects.filter(owner=request.user),
        'user': request.user,
        'form': form,
        'exchange_price': exchange_price,
        'support': models.Support.objects.first(),
    }


    return render(request, 'app/exchange_selection.html', context)



# class ExchangeDetailView(LoginRequiredMixin, View):
#     template_name = 'app/exchange_detail.html'

#     def get(self, request, id):
#         exchange = services.get_exchange_with_owner(id, request.user)
#         comments = services.get_active_comments(exchange)
#         exchange_pairs = services.get_exchange_pairs(exchange)
#         context = services.get_context_data(exchange, exchange_pairs, comments)
#         return render(request, self.template_name, context)

#     def post(self, request, id):
#         exchange = services.get_exchange_with_owner(id, request.user)
#         form_type = self._determine_form_type(request.POST)
#         return JsonResponse(handle_form(request, form_type, exchange))

#     def _determine_form_type(self, post_data):
#         """Определить тип формы"""
#         return post_data.get('form_type', 'exchange_pair')


def exchange_detail(request, exchange_slug):
    exchange = services.get_exchange_with_owner(exchange_slug, request.user)
    comments = services.get_active_comments(exchange)
    exchange_pairs = services.get_exchange_pairs(exchange)

    context = {
        'exchange': exchange,
        'exchange_pairs': exchange_pairs,
        'form': forms.ExchangePairForm(),

    }

    return render(request, 'app/exchange_detail.html', context)
    


