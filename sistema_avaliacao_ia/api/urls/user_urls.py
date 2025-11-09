from django.urls import path
from api.queries.user_queries import get_all_user, get_user, create_user

urlpatterns = [
    path('get-all-users/', get_all_user),
    path('get-user/<int:id>/', get_user),
    path('create-user/', create_user),
]