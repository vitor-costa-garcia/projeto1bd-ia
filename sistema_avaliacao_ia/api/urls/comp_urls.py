from django.urls import path
from api.queries.comp_queries import *

urlpatterns = [
    path('get-all-competitions/', get_all_competitions),
    path('post-competition/', post_competition),
    path('get-competition/<int:compid>/', get_competition),
    path('get-regras/<int:compid>/', get_regras_competition),
    path('get-ranking-comp/<int:compid>/', get_top20_ranking),
    path('get-submissions/<int:compid>/<int:equipeid>', get_submissions),
    path('download-competition-file/<int:compid>/<int:type_file>/', download_competition_file),
    path('verify-end-competition/<int:compid>/', verify_end_competition),
    path('create-team/', create_team),
    path('add-member-to-team/', add_member_to_team),
    path('remove-member-from-team/', remove_member_from_team),
    path('post-submission/<int:compid>/<int:equipeid>/', post_submission),
    path('delete-competition/', delete_competition),
]