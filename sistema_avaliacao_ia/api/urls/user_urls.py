from django.urls import path
from api.queries.user_queries import get_all_user

urlpatterns = [
    path('get-all-users/', get_all_user),
]