from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic.base import RedirectView
from rest_framework.authtoken.views import obtain_auth_token
from posts.views_auth import CustomLogoutView

def home(request):
    return HttpResponse("Главная страница работает!")

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home),
    path('api/', include('posts.urls')),
    # API для получения токена аутентификации
    path('api/auth/token/', obtain_auth_token, name='api_token_auth'),
    # переопределяем logout, чтобы он принимал GET
    path('accounts/logout/', CustomLogoutView.as_view(), name='logout'),
    path('accounts/', include('django.contrib.auth.urls')),
    # перенаправление с /logout на /accounts/logout/
    path('logout/', RedirectView.as_view(url='/accounts/logout/', permanent=False)),
]

# настройки для медиа в DEBUG
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)