"""
URL configuration for sistema_avaliacao_ia project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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

from django.contrib import admin
from django.urls import path, include
from main.views import *

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include('main.urls')),
    path("api/user/", include('api.urls.user_urls')),
    path("api/comp/", include('api.urls.comp_urls')),
    path("comp", comp, name="comp"),
    path("comp/form", comp_form, name="comp_form"),
    path("ranking", ranking, name="ranking"),
    path("reports", reports, name="reports"),
    path("user", user, name="user"),
]
