from django.urls import path
from main.views import index
from main import views

app_name = "main"
urlpatterns = [
    path("", index, name="index"),
    path("register/", views.register_view, name="register"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),

    path("competicoes/", views.comp, name="comp")
]