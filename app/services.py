
from django.shortcuts import get_object_or_404
from .models import Exchange, Comment, ExchangePair

def get_exchange_with_owner(exchange_id, user):
    """Получить обменник, принадлежащий пользователю"""
    return get_object_or_404(Exchange, id=exchange_id, owner=user)

def get_active_comments(exchange):
    """Получить активные комментарии для обменника"""
    return Comment.objects.filter(is_active=True, exchange=exchange)

def get_exchange_pairs(exchange):
    """Получить валютные пары для обменника"""
    return ExchangePair.objects.filter(exchange=exchange)
