from django.urls import path
from api.queries.comp_queries import (
    get_all_competitions, post_competition, get_competition, get_top20_ranking,
    get_submissions, verify_end_competition, download_competition_file,
    create_team, add_member_to_team, remove_member_from_team, post_submission,
    delete_competition, get_competition_stats, get_regras_competition
)

urlpatterns = [
    path('get-all-competitions/', get_all_competitions),
    path('post-competition/', post_competition),
    path('get-competition/<int:compid>/', get_competition),
    path('get-ranking-comp/<int:compid>/', get_top20_ranking),
    path('get-submissions/<int:compid>/<int:equipeid>', get_submissions),
    path('verify-end-competition/<int:compid>', verify_end_competition),
    path('download-competition-file/<int:compid>/<int:type_file>/', download_competition_file),
    path('create-team/', create_team),
    path('add-member-to-team/', add_member_to_team),
    path('remove-member-from-team/', remove_member_from_team),
    path('post-submission/<int:compid>/<int:equipeid>/', post_submission),
    path('delete-competition/', delete_competition),
    path('get-comp-stats/<int:compid>/', get_competition_stats),
    path('get-regras/<int:compid>/', get_regras_competition),
]