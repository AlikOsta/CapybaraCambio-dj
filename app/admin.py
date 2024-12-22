from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Exchange, BaseVerification, VerificationExchange, BaseDelivery, DeliveryExchange, Currency, ExchangePair, SuperLocation, SubLocation, Comment
from .models import Support, CustomUser
from django.utils import timezone


@admin.register(Support)
class SupportAdmin(admin.ModelAdmin):
    list_display = ('name', 'url_support')


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    # Поля для отображения в списке
    list_display = ("username", "balance", "is_active", "is_staff")
    list_filter = ("is_active", "username", "is_staff")

    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("username", "password1", "password2", "email", "balance", "is_active", "is_staff"),
        }),
    )

    fieldsets = (
        (None, {"fields": ("username", "password")}),
        ("Personal info", {"fields": ("email", "balance")}),
        ("Permissions", {"fields": ("is_active", "is_staff")}),
    )

    search_fields = ("username", "email")  
    ordering = ("username",)


class VerificationExchangeInline(admin.TabularInline):
    model = VerificationExchange
    extra = 0
    fields = ('exchange', 'activated_at', 'expires_at', 'is_active')
    readonly_fields = ('activated_at', 'expires_at')

    def get_formset(self, request, obj=None, **kwargs):
        formset = super().get_formset(request, obj, **kwargs)
        form = formset.form
        form.base_fields['expires_at'].initial = timezone.now() + timezone.timedelta(days=30)
        return formset
    

class DeliveryExchangeInline(admin.TabularInline):
    model = DeliveryExchange
    extra = 0
    fields = ('exchange', 'price', "currency_delivery", 'delivery_time', 'description', 'is_active')


@admin.register(Exchange)
class ExchangeAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'rating', 'is_active', 'city', 'slug', 'has_verified', 'has_active_delivery')
    search_fields = ('name', 'owner__username', 'city__name')
    list_filter = ('is_active', 'city')
    readonly_fields = ('created_at', 'updated_at')
    exclude = ('slug',)
    fieldsets = (
        (None, {
            'fields': ('owner', 'name', 'url_operator', 'logo', 'description', 'city', 'is_active')
        }),
        
    )
    actions = ['activate_exchanges', 'deactivate_exchanges']

    @admin.action(description='Активировать выбранные обменники')
    def activate_exchanges(self, request, queryset):
        queryset.update(is_active=True)
    
    @admin.action(description='Деактивировать выбранные обменники')
    def deactivate_exchanges(self, request, queryset):
        queryset.update(is_active=False)


@admin.register(BaseVerification)
class VerificationAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'days')
    search_fields = ('name',)


@admin.register(VerificationExchange)
class VerificationExchangeAdmin(admin.ModelAdmin):
    list_display = ('exchange', 'activated_at', 'expires_at', 'is_active')
    list_filter = ('is_active',)
    readonly_fields = ('activated_at', 'expires_at')
    search_fields = ('exchange__name',)


@admin.register(BaseDelivery)
class DeliveryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(DeliveryExchange)
class DeliveryExchangeAdmin(admin.ModelAdmin):
    list_display = ('exchange', 'price', 'delivery_time', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('exchange__name', 'description')


@admin.register(Currency)
class CurrencyAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'logo')
    search_fields = ('code', 'name')


@admin.register(ExchangePair)
class ExchangePairAdmin(admin.ModelAdmin):
    list_display = ('exchange', 'give_currency', 'give_rate', 'get_currency', 'get_rate')
    search_fields = ('exchange__name', 'give_currency__code', 'get_currency__code')
    list_filter = ('exchange',)
    readonly_fields = ('created_at', 'updated_at')


class SubLocationInline(admin.TabularInline):
    model = SubLocation
    extra = 1
    verbose_name = "Подлокация"
    verbose_name_plural = "Подлокации"


@admin.register(SuperLocation)
class SuperLocationAdmin(admin.ModelAdmin):
    exclude = ("super_location",)
    inlines = [SubLocationInline]
    list_display = ('name', 'order')
    search_fields = ('name',)
    ordering = ('order', 'name')



@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('exchange', 'author', 'rating', 'content', 'is_active', 'created_at')
    list_filter = ('is_active', 'rating')
    search_fields = ('author', 'content')