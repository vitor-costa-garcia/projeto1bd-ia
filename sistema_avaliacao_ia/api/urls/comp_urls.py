from django.urls import path
from api.queries.comp_queries import *

urlpatterns = [
    path('get-all-competitions/', get_all_competitions),
    path('post-competition/', post_competition),
    path('get-competition/<int:compid>/', get_competition),
    path('download-competition-file/<int:compid>/<int:type_file>/', download_competition_file),
]