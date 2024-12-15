
from .forms import DeliveryForm

def prepare_delivery_form(exchange):
    """Подготовить форму доставки с начальными данными"""
    initial_data = {}
    if exchange.has_active_delivery():
        delivery = exchange.delivery
        initial_data = {
            'template': delivery.template,
            'price': delivery.price,
            'delivery_time': delivery.delivery_time,
            'description': delivery.description,
        }
    return DeliveryForm(initial=initial_data)
