from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import AuthenticationForm
from .models import VerificationExchange, DeliveryExchange
from .models import SuperLocation, SubLocation, Comment
from .models import ExchangePair, Exchange, Currency


class CustomAuthenticationForm(AuthenticationForm):
    '''Форма аутентификации пользователя'''
    error_messages = {
        "invalid_login": (
            "Неверное имя пользователя или пароль."
        ),
        "inactive": ("Ваш аккаунт неактивен."),
    }


class UserCommentForm(forms.ModelForm):
    '''Форма комментария'''
    class Meta:
        model = Comment
        exclude = ['is_active']  
        widgets = {'exchange': forms.HiddenInput} 
    rating = forms.ChoiceField(choices=[(i, str(i)) for i in range(1, 6)], widget=forms.RadioSelect, initial=5,label="Рейтинг")


class VerificationForm(forms.ModelForm):
    '''Форма верификации обменника'''
    class Meta:
        model = VerificationExchange
        fields = ['template']

    def clean(self):
        cleaned_data = super().clean()
        template = cleaned_data.get('template')
        
        if not template:
            raise ValidationError("Template is required")
            
        return cleaned_data


class DeliveryForm(forms.ModelForm):
    '''Форма доставки обменника'''
    class Meta:
        model = DeliveryExchange
        fields = ['template', 'price', 'delivery_time', 'currency_delivery', 'description']
        labels = { 
            'template': 'Способ доставки',
            'price': 'Стоимость доставки',
            'delivery_time': 'Время доставки (в часах)',
            'currency_delivery': 'Валюта доставки',
            'description': 'Условия доставки'
        }
        widgets = {
            'template': forms.Select(attrs={
                'class': 'form-control',
                'placeholder': 'Выберите способ доставки'
            }),
            'price': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Укажите стоимость',
                'min': '0'
            }),
            'delivery_time': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Укажите время в часах',
                'min': '0'
            }),
            'currency_delivery': forms.Select(attrs={
                'class': 'form-control',
                'placeholder': 'Выберите валюту доставки'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Опишите условия доставки',
                'rows': 3
            })
        }

    def clean(self):
        cleaned_data = super().clean()
        template = cleaned_data.get('template')
        price = cleaned_data.get('price')
        
        if not template:
            raise ValidationError("Шаблон доставки обязателен")
            
        return cleaned_data


class SubLocationForm(forms.ModelForm):
    '''Форма подлокации'''
    super_location = forms.ModelChoiceField(
        queryset=SuperLocation.objects.all(),
        empty_label=None,
        label='Страна',
        required=True
    )

    class Meta:
        model = SubLocation
        fields = '__all__'


class ExchangePairForm(forms.ModelForm):
    '''Форма пары обмена'''
    class Meta:
        model = ExchangePair
        fields = ['give_currency', 'get_currency', 'give_rate', 'get_rate']
        widgets  = {
            'give_currency': forms.Select(attrs={'class': 'form-control'}),
            'get_currency': forms.Select(attrs={'class': 'form-control'}),
            'give_rate': forms.NumberInput(attrs={'class': 'form-control', 'min': '0'}),
            'get_rate': forms.NumberInput(attrs={'class': 'form-control', 'min': '0'})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['give_currency'].queryset = Currency.objects.all()
        self.fields['get_currency'].queryset = Currency.objects.all()

    def clean(self):
        cleaned_data = super().clean()
        from_currency = cleaned_data.get('give_currency')
        to_currency = cleaned_data.get('get_currency')
        
        if from_currency == to_currency:
            raise ValidationError("Валюта отправления и получения не могут быть одинаковыми.")


class ExchangeForm(forms.ModelForm):
    '''Форма обмена'''
    class Meta:
        model = Exchange
        fields = ['name', 'url_operator', 'logo', 'description', 'city', 'is_active']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Название обменника', 'class': 'form-control'}),
            'url_operator': forms.TextInput(attrs={'placeholder': 'Ссылка: t.me/NameOperator', 'class': 'form-control'}),
            'description': forms.Textarea(attrs={'placeholder': 'Описание обменника', 'class': 'form-control h-80', 'rows': 6}),
            'city': forms.Select(attrs={'class': 'form-control'}),
            'logo': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)








