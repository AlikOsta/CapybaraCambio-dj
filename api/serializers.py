from rest_framework import serializers
from app.models import Exchange, SubLocation, Currency, ExchangePair, DeliveryExchange, VerificationExchange, BaseVerification, BaseDelivery, Comment


class SubLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubLocation
        fields = ['name']


class CurrencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Currency
        fields = ['code', 'name', 'logo']


class BaseVerificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = BaseVerification
        fields = ['name', 'logo']


class BaseDeliverySerializer(serializers.ModelSerializer):
    class Meta:
        model = BaseDelivery
        fields = ['name', 'logo']


class VerificationExchangeSerializer(serializers.ModelSerializer):
    template = BaseVerificationSerializer()
    
    class Meta:
        model = VerificationExchange
        fields = ['template']


class DeliveryExchangeSerializer(serializers.ModelSerializer):
    currency_delivery = CurrencySerializer()
    template = BaseDeliverySerializer()

    class Meta:
        model = DeliveryExchange
        fields = ['template', 'price', 'delivery_time', 'currency_delivery', 'description', 'is_active', ]


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['content', 'rating', 'created_at', 'author', 'telegram_id', 'is_active']


class ExchangeSerializer(serializers.ModelSerializer):
    city = SubLocationSerializer()
    delivery = DeliveryExchangeSerializer(required=False, allow_null=True)
    
    verifications = VerificationExchangeSerializer(required=False, allow_null=True)

    comments = CommentSerializer(many=True, required=False, allow_null=True)

    class Meta:
        model = Exchange
        fields = ['city', 'name', 'url_operator', 'logo', 'description', 'rating', 'is_active',  'delivery', 'verifications', 'comments']


class ExchangeNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exchange
        fields = ['name']
    

class ExchangePairSerializer(serializers.ModelSerializer):
    # exchange = ExchangeSerializer() 
    exchange = ExchangeNameSerializer()
    give_currency = CurrencySerializer()
    get_currency = CurrencySerializer()

    class Meta:
        model = ExchangePair
        fields = ['updated_at', 'give_rate', 'get_rate', 'give_currency', 'get_currency', 'exchange', 'is_active']
