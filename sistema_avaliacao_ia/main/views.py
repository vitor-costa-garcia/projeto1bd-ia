from django.db import connection
from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password
from api.queries.user_queries import get_all_user
from api.queries.comp_queries import get_all_competitions
import requests

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

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        senha_form = request.POST.get('senha')

        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT id, nome, senha FROM usuario WHERE email = %s",
                [email]
            )
            user_data = cursor.fetchone()

        if user_data and check_password(senha_form, user_data[2]):
            request.session['user_id'] = user_data[0]
            request.session['user_name'] = user_data[1]
            
            messages.success(request, 'Login realizado com sucesso!')
            
            return redirect('main:comp')

        messages.error(request, 'Email ou senha inválidos.')
        return render(request, 'login.html')

    return render(request, 'login.html')
def register_view(request):
    if request.method == 'POST':
        payload = {
            'nome': request.POST.get('nome'),
            'email': request.POST.get('email'),
            'senha': request.POST.get('senha'),
            'datanascimento': request.POST.get('datanascimento'),
            'numero': request.POST.get('numero'),
            'rua': request.POST.get('rua'),
            'cidade': request.POST.get('cidade'),
            'estado': request.POST.get('estado'),
            'pais': request.POST.get('pais'),
        }

        try:
            api_url = "http://127.0.0.1:8000/api/user/create-user/"
            response = requests.post(api_url, data=payload)
            data = response.json()

            if response.status_code == 201 and 'user_id' in data:
                messages.success(request, 'Conta criada com sucesso! Faça o login.')
                return redirect('main:login')
            else:
                error_msg = data.get('error', 'Ocorreu um erro desconhecido.')
                messages.error(request, error_msg)
        
        except requests.exceptions.RequestException as e:
            messages.error(request, f"Erro de conexão com a API: {e}")

        return render(request, "user/user_form.html")

    return render(request, "user/user_form.html")

def logout_view(request):
    try:
        del request.session['user_id']
        del request.session['user_name']
    except KeyError:
        pass 
    return redirect('main:index')