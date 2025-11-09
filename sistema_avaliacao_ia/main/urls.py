from django.urls import path
from main.views import index
from main import views

app_name = "main"
urlpatterns = [
    path("", index, name="index"),
    path("register/", views.register_view, name="register"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),

    path("user/", views.user, name="user-profile"),

    path("competicoes/", views.comp, name="comp"),
    path("competicoes/new/", views.comp_form, name="comp-form"),
    path("ranking/", views.ranking, name="ranking"),
    path("reports/", views.reports, name="reports"),
]