
from django.shortcuts import get_object_or_404
from .models import Exchange, Comment, ExchangePair

def get_exchange_with_owner(exchange_slug, user):
    """Получить обменник, принадлежащий пользователю"""
    return get_object_or_404(Exchange, slug=exchange_slug, owner=user)

def get_active_comments(exchange):
    """Получить активные комментарии для обменника"""
    return Comment.objects.filter(is_active=True, exchange=exchange)

def get_exchange_pairs(exchange):
    """Получить валютные пары для обменника"""
    return ExchangePair.objects.filter(exchange=exchange).order_by('-is_active')

