
from .forms import VerificationForm, DeliveryForm, ExchangePairForm, ExchangeForm
from .models import ExchangePair
from django.core.exceptions import ValidationError
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.utils import timezone

def handle_verification_form(request, exchange):
    """Обработка формы верификации"""
    form = VerificationForm(request.POST)
    if form.is_valid():
        try:
            verification = form.save(commit=False)
            verification.exchange = exchange
            verification.expires_at = timezone.now() + timezone.timedelta(days=verification.template.days)

            if exchange.owner.balance >= verification.template.price:
                exchange.owner.balance -= verification.template.price
                exchange.owner.save()
                verification.save()
                return {'success': True}
            else:
                return {'success': False, 'error': 'Недостаточно средств'}
                
        except ValidationError as e:
            return {'success': False, 'error': str(e)}
    return {'success': False, 'error': form.errors}

def handle_delivery_form(request, exchange):
    """Обработка формы доставки"""
    form = DeliveryForm(
        request.POST,
        instance=exchange.delivery if exchange.has_active_delivery() else None
    )
    if form.is_valid():
        try:
            delivery = form.save(commit=False)
            delivery.exchange = exchange
            delivery.is_active = True
            delivery.save()
            return {'success': True}
        except ValidationError as e:
            return {'success': False, 'error': str(e)}
    return {'success': False, 'error': form.errors}

def handle_exchange_pair_form(request, exchange):
    """Обработка формы валютной пары"""
    form = ExchangePairForm(request.POST)
    if form.is_valid():
        give_currency = form.cleaned_data['give_currency']
        get_currency = form.cleaned_data['get_currency']
        
        best_rate = ExchangePair.objects.filter(
            give_currency=give_currency,
            get_currency=get_currency,
            is_active=True
        ).order_by('-get_rate', 'give_rate').first()

        if best_rate:
            return {
                'success': True,
                'best_rate': {
                    'give_rate': best_rate.give_rate,
                    'get_rate': best_rate.get_rate,
                    'exchange_name': best_rate.exchange.name
                }
            }
        
        if ExchangePair.objects.filter(exchange=exchange, give_currency=give_currency, get_currency=get_currency).exists():
            return {'success': False, 'error': 'Такая валютная пара уже существует.'}
        try:
            pair = form.save(commit=False)
            pair.exchange = exchange
            pair.save()
            return {'success': True}
        except ValidationError as e:
            return {'success': False, 'error': str(e)}
    return {'success': False, 'error': 'Форма заполнена неверно'}
def handle_exchange_edit_form(request, exchange):
    """Обработка формы редактирования обменника"""
    form = ExchangeForm(request.POST, request.FILES, instance=exchange)
    if form.is_valid():
        try:
            exchange = form.save(commit=False)
            exchange.owner = request.user 
            exchange.save(update_fields=['name', 'url_operator', 'logo', 'description', 'city', 'is_active'])
            return {'success': True}
        except ValidationError as e:
            return {'success': False, 'error': str(e)}
    return {'success': False, 'error': form.errors}

def handle_edit_pair_form(request, exchange):
    """Обработка формы редактирования валютной пары"""
    pair_id = request.POST.get('pair_id')
    pair = get_object_or_404(ExchangePair, id=pair_id, exchange=exchange)
    try:
        pair.give_rate = request.POST.get('give_rate')
        pair.get_rate = request.POST.get('get_rate')
        pair.save(update_fields=['give_rate', 'get_rate'])
        return {'success': True}
    except ValidationError as e:
        return {'success': False, 'error': str(e)}
    except Exception as e:
        return {'success': False, 'error': str(e)}

FORM_HANDLERS = {
    'verification': handle_verification_form,
    'delivery': handle_delivery_form,
    'exchange_pair': handle_exchange_pair_form,
    'exchange': handle_exchange_edit_form,
    'edit_pair': handle_edit_pair_form,
}

def handle_form(request, form_type, exchange):
    """Выполнить обработку формы"""
    handler = FORM_HANDLERS.get(form_type)
    if handler:
        return handler(request, exchange)
    return {'success': False, 'error': f'Неизвестный тип формы: {form_type}'}

def handle_check_rate(request, exchange):
    give_currency_id = request.POST.get('give_currency')
    get_currency_id = request.POST.get('get_currency')
    
    best_rate = ExchangePair.objects.filter(
        give_currency_id=give_currency_id,
        get_currency_id=get_currency_id,
        is_active=True
    ).order_by('-get_rate', 'give_rate').first()

    if best_rate:
        return {
            'success': True,
            'best_rate': {
                'give_rate': str(best_rate.give_rate),
                'get_rate': str(best_rate.get_rate),
                'exchange_name': best_rate.exchange.name
            }
        }
    return {'success': False}

FORM_HANDLERS['check_rate'] = handle_check_rate
