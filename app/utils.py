
# from .forms_handlers import prepare_delivery_form
# from .forms import VerificationForm, ExchangePairForm, ExchangeForm
# from .models import BaseVerification, BaseDelivery, Currency

# def get_context_data(exchange, exchange_pairs, comments):
#     """Сформировать контекст для шаблона"""
#     return {
#         'exchange': exchange,
#         'exchange_pair': exchange_pairs,
#         'comment': comments,
#         'verification_form': VerificationForm(),
#         'delivery_form': prepare_delivery_form(exchange),
#         'form': ExchangePairForm(),
#         'exchange_form': ExchangeForm(instance=exchange),
#         'verification_templates': BaseVerification.objects.all(),
#         'delivery_templates': BaseDelivery.objects.all(),
#         'give_currency_templates': Currency.objects.all(),
#         'get_currency_templates': Currency.objects.all(),
#     }
