from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views
from django.contrib.auth.views import LogoutView

app_name = 'app'

urlpatterns = [

    path('exchange-selection/', views.exchange_selection, name='ex_selection'),
    path('exchange/<uuid:id>/', views.ExchangeDetailView.as_view(), name='ex_detail'),
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='app:login'), name='logout'),
    
    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)