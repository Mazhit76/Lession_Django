"""shop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from shop.settings import MEDIA_ROOT, MEDIA_URL
from django import urls
from django.contrib import admin
from django.urls import path, include, re_path
from mainapp import views as mainapp_views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [

    path('admin/', admin.site.urls),
    path('authapp/', include('authapp.urls')),
    path('', mainapp_views.main, name='main'),
    path('products/', include('mainapp.urls', namespace='products')),
    path('baskets/', include('basketapp.urls', namespace='baskets')),
    path('admin-staff/', include('adminapp.urls', namespace='admin_staff')),
    path('', include('social_django.urls', namespace='social')),
    path('order/', include('ordersapp.urls', namespace='order')),

]
# Подгружаем файлы изображений, т.е. указываем путь откуда подгружать
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
