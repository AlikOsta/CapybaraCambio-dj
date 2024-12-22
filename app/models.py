from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid
from django.db import transaction
from django.utils import timezone
from django.core.validators import FileExtensionValidator
from decimal import Decimal
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models.signals import post_delete
from django.dispatch import receiver
import re
from django.utils.timezone import now
from django.utils.text import slugify


class CustomUser(AbstractUser):
    '''Модель пользователя'''
    balance = models.IntegerField(default=350, verbose_name='Баланс')

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
    
    def __str__(self):
        return self.username
    

class Support(models.Model):
    '''Модель поддержки'''
    name = models.CharField(max_length=100, verbose_name='Имя')
    url_support = models.URLField(verbose_name='Ссылка на админа')
    

class BaseModel(models.Model):
    '''Базовая модель'''
    id = models.AutoField(primary_key=True) 
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')

    class Meta:
        abstract = True


class Currency(BaseModel):
    '''Модель валюты'''
    code = models.CharField(max_length=5, unique=True, verbose_name='Код валюты')
    name = models.CharField(max_length=50, verbose_name='Название валюты')
    logo = models.FileField(
        upload_to='currency_logos/',
        verbose_name='Лого валюты',
        validators=[FileExtensionValidator(['svg', 'png', 'jpg', 'jpeg'])],
        blank=True,
        null=True
    )

    class Meta:
        verbose_name = 'Валюта'
        verbose_name_plural = 'Валюты'
        ordering = ['code']

    def __str__(self):
        return self.name


class Exchange(BaseModel):
    '''Модель обмена'''
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name='Владелец')
    name = models.CharField(max_length=25, unique=True,  verbose_name='Название')
    url_operator = models.URLField(verbose_name="Ссылка на оператора")
    logo = models.ImageField(upload_to='exchange_logos/', default='exchange_logos/default_logo.png', verbose_name='Логотип обменника')
    description = models.TextField(max_length=150, verbose_name='Описание')
    city =models.ForeignKey("SubLocation", null=False, blank=False, on_delete=models.PROTECT, verbose_name='Город', db_index=True)
    rating = models.DecimalField(max_digits=3, decimal_places=1, default=0, verbose_name='Рейтинг', db_index=True)
    is_active = models.BooleanField(default=True, verbose_name='Активность', db_index=True)
    price = models.IntegerField(default=300, verbose_name='Стоимость размещения обменника')
    slug = models.SlugField(max_length=200, unique=True)

    class Meta:
        verbose_name = 'Обменник'
        verbose_name_plural = 'Обменники'
        indexes = [
            models.Index(fields=['is_active']),
            models.Index(fields=['rating']),
            models.Index(fields=['city']),
        ]

    def __str__(self):
        return self.name
    
    def has_verified(self):
        """Проверка на верификацию"""
        return hasattr(self, 'verifications') and self.verifications.is_active
    
    def get_verification_logo(self):
        """Получение логотипа верификации"""
        if self.has_verified():
            return self.verifications.logo.url
        return None
    
    def has_active_delivery(self):
        """Проверка на активность доставки"""
        return hasattr(self, 'delivery') and self.delivery.is_active
    
    def update_rating(self):
        """Обновление рейтинга"""
        comments = self.comments.filter(is_active=True)
        avg_rating = round(comments.aggregate(models.Avg('rating'))['rating__avg']or 0, 2)
        Exchange.objects.filter(pk=self.pk).update(rating=avg_rating)

    def save(self, *args, **kwargs):
        """Сохранение объекта"""
        is_new = not bool(self.pk)
        if is_new:
            try:
                with transaction.atomic():
                    user = CustomUser.objects.select_for_update().get(id=self.owner.id)
                    if user.balance >= self.price:
                        old_balance = user.balance
                        user.balance -= self.price
                        user.save()
                        self.owner = user
                    else:
                        raise ValueError('Недостаточно средств')
            except Exception as e:
                raise

        if not self.slug:
            self.slug = slugify(self.name)

        super().save(*args, **kwargs)

                        

class BaseVerification(BaseModel):
    '''Базовая модель верификации'''
    name = models.CharField(max_length=25, default='Верификация', unique=True, verbose_name='Название')
    logo = models.FileField(upload_to='verification_logos/', validators=[FileExtensionValidator(['svg', 'png', 'jpg', 'jpeg'])], verbose_name='Логотип верификации')
    price = models.IntegerField(default=0, verbose_name='Стоимость верификации')
    days = models.IntegerField(default=30, verbose_name='Количество дней')

    class Meta:
        verbose_name = 'Шаблон верификации'
        verbose_name_plural = 'Шаблоны верификации'
        ordering = ['name']

    def __str__(self):
        return self.name
    

class VerificationExchange(BaseModel):
    '''Модель верификации обменника'''
    exchange = models.OneToOneField(Exchange, on_delete=models.PROTECT, related_name='verifications', verbose_name='Обменник')
    template = models.ForeignKey(BaseVerification, on_delete=models.PROTECT, null=False, blank=False, default=1, verbose_name='Шаблон верификации')
    expires_at = models.DateTimeField(verbose_name='Дата окончания', db_index=True)
    activated_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата подключения', db_index=True)
    is_active = models.BooleanField(default=True, verbose_name='Активность', db_index=True)

    class Meta:
        verbose_name = 'Верификация обменника'
        verbose_name_plural = 'Верификации обменников'
        ordering = ['template__name'] 
        indexes = [
            models.Index(fields=['expires_at']),
            models.Index(fields=['is_active']),
        ]

    def save(self, *args, **kwargs):
        """Сохранение объекта"""
        if not self.pk: 
            self.is_active = True

            if not self.expires_at:
                if hasattr(self.template, 'days') and self.template.days is not None:
                    self.expires_at = timezone.now() + timezone.timedelta(days=self.template.days)
                else:
                    raise ValueError("Шаблон не содержит корректного значения для 'days'")

            if self.exchange.owner.balance >= self.template.price:
                self.exchange.owner.balance -= self.template.price
                self.exchange.owner.save()
            else:
                raise ValueError('Недостаточно средств для выполнения верификации')

        super().save(*args, **kwargs)

    def check_expiration(self):
        """Проверка истечения срока действия верификации и удаление объекта"""
        if self.expires_at < timezone.now():
            self.delete()

    def delete(self, using = ..., keep_parents = ...):
        return super().delete(using, keep_parents)

    def __str__(self):
        return f"Верификация {self.template.name} для обменника {self.exchange.name}"
    

class BaseDelivery(BaseModel):
    '''Базовая модель доставки'''
    name = models.CharField(max_length=25, default='Доставка', verbose_name='Название Доставки')
    logo = models.FileField(upload_to='delivery_logos/', validators=[FileExtensionValidator(['svg', 'png', 'jpg', 'jpeg'])], verbose_name='Логотип доставки')

    class Meta:
        verbose_name = 'Шаблон доставки'
        verbose_name_plural = 'Шаблоны доставки'
        ordering = ['name']

    def __str__(self):
        return self.name
    

class DeliveryExchange(BaseModel):
    '''Модель доставки обменника'''
    exchange = models.OneToOneField(Exchange, on_delete=models.PROTECT, related_name='delivery', verbose_name='Название обменника')
    template = models.ForeignKey(BaseDelivery, on_delete=models.PROTECT, null=False, blank=False, default=1, verbose_name='Вариант доставки')
    price = models.IntegerField(default=0, verbose_name='Стоимость доставки')
    delivery_time = models.IntegerField(default=0, verbose_name='Время доставки (час)')
    currency_delivery = models.ForeignKey(Currency, on_delete=models.PROTECT, null=False, blank=False, default=1, verbose_name='Валюта доставки')
    description = models.TextField(max_length=200, verbose_name='Условия доставки')
    is_active = models.BooleanField(default=True, verbose_name='Активность', db_index=True)

    class Meta:
        verbose_name = 'Доставка'
        verbose_name_plural = 'Доставки'
        ordering = ['template__name'] 

    def save(self, *args, **kwargs):
        if not self.pk:
            self.is_active = True
        super().save(*args, **kwargs)

    def activate(self):
        """Активируем доставку"""
        self.is_active = True
        self.save()

    def deactivate(self):
        """Деактивируем доставку"""
        self.is_active = False
        self.save()

    def __str__(self):
        return self.template.name
    

class ExchangePair(BaseModel):
    '''Модель пары валют'''
    exchange = models.ForeignKey(Exchange, on_delete=models.CASCADE, related_name='pairs', verbose_name='Обменник')
    give_currency = models.ForeignKey(Currency, on_delete=models.CASCADE, related_name='given_exchange_pairs', verbose_name='Валюта получения')
    give_rate = models.DecimalField(max_digits=10, default=0, decimal_places=2,  verbose_name='Курс обмена (отдая)')
    get_currency = models.ForeignKey(Currency, on_delete=models.CASCADE, related_name='received_exchange_pairs', verbose_name='Валюта выдачи')
    get_rate = models.DecimalField(max_digits=10, default=0, decimal_places=2, verbose_name='Курс обмена (получаю)')
    is_active = models.BooleanField(default=True, verbose_name='Активна', db_index=True) 

    class Meta:
        verbose_name = 'Валютная пара'
        verbose_name_plural = 'Валютые пары'
        ordering = ['exchange__name']
        indexes = [
            models.Index(fields=['is_active']),
        ]
        constraints = [
            models.UniqueConstraint(
                fields=['exchange', 'give_currency', 'get_currency'],
                name='unique_exchange_pair'
            )
        ]

    def __str__(self):
        return (
            f"Обмен: {self.give_currency} -> {self.get_currency} "
            f"(Курс: {self.give_rate} -> {self.get_rate})"
        ) 
    
    def clean(self):
        if self.give_rate <= 0 or self.get_rate <= 0:
            raise ValueError("Курсы обмена должны быть положительными значениями.")

        rate_ratio = self.give_rate / self.get_rate

        if rate_ratio > 1:
            self.get_rate = Decimal('1')
            self.give_rate = rate_ratio
        else:
            self.give_rate = Decimal('1')
            self.get_rate = Decimal('1') / rate_ratio


class Location(models.Model):
    """Базовая модель локации"""
    name = models.CharField(max_length=20, db_index=True, unique=True, verbose_name="Название")
    order = models.SmallIntegerField(default=0, db_index=True, verbose_name="Порядок")
    super_location = models.ForeignKey("SuperLocation", on_delete=models.PROTECT, null=True, blank=True, verbose_name="Страна")


class SuperLocationManager(models.Manager):
    '''Менеджер для фильтрации супергородов (стран)'''
    def get_queryset(self):
        return super().get_queryset().filter(super_location__isnull=True)


class SuperLocation(Location):
    """ Прокси-модель для супергородов (стран)"""
    objects = SuperLocationManager()

    def __str__(self):
        return self.name

    class Meta:
        proxy = True
        ordering = ('order', 'name')
        verbose_name = 'Страна'
        verbose_name_plural = 'Страны'


class SubLocationManager(models.Manager):
    '''Менеджер для фильтрации подгородов'''
    def get_queryset(self):
        return super().get_queryset().filter(super_location__isnull=False)


class SubLocation(Location):
    """ Прокси-модель для подгородов"""
    objects = SubLocationManager()

    def __str__(self):
        return '%s' % (self.name)

    class Meta:
        proxy = True
        ordering = ('super_location__order', 'super_location__name', 'order', 'name')
        verbose_name = 'Город'
        verbose_name_plural = 'Города'


class Comment(BaseModel):
    '''Модель комментария'''
    exchange = models.ForeignKey(Exchange, on_delete=models.CASCADE, related_name='comments', verbose_name='Обменник')
    author = models.CharField(max_length=50, verbose_name='Автор') 
    telegram_id = models.CharField(max_length=30, verbose_name='ID Telegram', blank=True, null=True)
    content = models.TextField(verbose_name='Комментарий')
    rating = models.PositiveIntegerField(default=5, verbose_name='Рейтинг', validators=[MinValueValidator(1), MaxValueValidator(5)])
    is_active = models.BooleanField(default=True, verbose_name='Активен')

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        """сохраняет комментарий и обновляет рейтинг обменника."""
        super().save(*args, **kwargs)
        self.exchange.update_rating()

    def clean(self):
        """ Проверка, что пользователь не оставил комментарий для данного обменника"""
        if Comment.objects.filter(exchange=self.exchange, telegram_id=self.telegram_id, is_active=True).exists():
            raise ValueError("Этот пользователь уже оставил комментарий для данного обменника.")
        super().clean()


@receiver(post_delete, sender=Comment)
def update_exchange_rating_on_delete(sender, instance, **kwargs):
    '''если удалили негативный отзыв с низкой оценкой, рейтинг обменника автоматически пересчитается в большую сторону.'''
    instance.exchange.update_rating()