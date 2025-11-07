from django.urls import path
from api.queries.comp_queries import *

urlpatterns = [
    path('get-all-competitions/', get_all_competitions),
    path('post-competition/', post_competition),
]