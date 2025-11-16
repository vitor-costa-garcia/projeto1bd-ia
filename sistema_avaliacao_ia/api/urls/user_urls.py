from django.urls import path
from api.queries.user_queries import (
    get_all_user, 
    get_user, 
    create_user, 
    create_organizer, 
    search_users ,
    get_user_prizes
)

urlpatterns = [
    path('get-all-users/', get_all_user),
    path('get-user/<int:id>/', get_user),
    path('create-user/', create_user),
    path('create-organizer/', create_organizer),
    path('search-users/', search_users),
    path('get-user-prizes/<int:userid>/', get_user_prizes),
]