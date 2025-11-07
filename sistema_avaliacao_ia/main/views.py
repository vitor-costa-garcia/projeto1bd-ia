from django.shortcuts import render
from api.queries.user_queries import get_all_user
from api.queries.comp_queries import get_all_competitions
import requests

# Create your views here.

def index(request):
    return render(request, "index.html")

def comp(request):
    resp = requests.get("http://127.0.0.1:8000/api/comp/get-all-competitions/")
    competitions = resp.json()['competitions']

    context = {
        "competitions" : competitions
    }
    return render(request, "comp/comp.html", context)

def comp_form(request):
    return render(request, "comp/comp_form.html")

def ranking(request):
    resp = requests.get("http://127.0.0.1:8000/api/user/get-all-users/")
    rankinglist = resp.json()['users']

    context = {
        "rankinglist" : rankinglist
    }
    return render(request, "ranking/ranking.html", context)

def reports(request):
    return render(request, "reports/reports.html")

def user(request):
    return render(request, "user/user.html")