from django.db import connection
from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password
from api.queries.user_queries import check_if_user_is_organizer, fetch_user_auth_data_by_email, get_all_user, check_user_team_membership
from api.queries.comp_queries import get_all_competitions, get_team_members
from datetime import datetime
from django.utils import timezone
import requests

def index(request):
    if request.session.get('user_id'):
        return redirect('main:comp')
    else:
        return redirect('main:login')

def comp(request):
    resp = requests.get("http://127.0.0.1:8000/api/comp/get-all-competitions/")
    competitions_data = resp.json()['competitions'] or []

    processed_competitions = []
    for comp_list in competitions_data:
        try:
            comp_list[5] = datetime.fromisoformat(comp_list[5].replace(" ", "T"))
        except (ValueError, TypeError, IndexError):
            pass
        try:
            comp_list[6] = datetime.fromisoformat(comp_list[6].replace(" ", "T"))
        except (ValueError, TypeError, IndexError):
            pass
        processed_competitions.append(comp_list)
    
    now = timezone.now()

    is_organizer = False
    user_id = request.session.get('user_id')
    user_name = request.session.get('user_name')

    if user_id:
        is_organizer = check_if_user_is_organizer(user_id)

    context = {
        "competitions" : processed_competitions,
        "is_organizer": is_organizer,
        "now": now,
        "user_name": user_name
    }
    return render(request, "comp/comp.html", context)

def comp_form(request):
    if request.method == 'POST':
        user_id = request.session.get('user_id')
        if not user_id:
            messages.error(request, 'Você precisa estar logado para criar uma competição.')
            return redirect('main:login') 

        payload = request.POST.copy()
        
        payload['id_org_competicao'] = user_id
        
        try:
            api_url = "http://127.0.0.1:8000/api/comp/post-competition/"
            
            response = requests.post(api_url, data=payload, files=request.FILES)
            
            data = response.json()

            if response.status_code == 201:
                messages.success(request, 'Competição criada com sucesso!')
                return redirect('main:comp')
            else:
                error_msg = data.get('error', 'Ocorreu um erro desconhecido.')
                messages.error(request, error_msg)
        
        except requests.exceptions.RequestException as e:
            messages.error(request, f"Erro de conexão com a API: {e}")

    server_today = timezone.now().strftime('%Y-%m-%d')
    context = {
        'server_today': server_today,
        "user_name": request.session.get('user_name')
    }
    return render(request, "comp/comp_form.html", context)

def comp_view(request, compid):
    requests.get(f"http://127.0.0.1:8000/api/comp/verify-end-competition/{compid}/")

    user_id = request.session.get('user_id')
    equipe_id = None
    team_members = []
    submission_data = []
    
    if user_id:
        equipe_id = check_user_team_membership(user_id, compid)
        if equipe_id:
            team_members = get_team_members(compid, equipe_id)
            api_url = f"http://127.0.0.1:8000/api/comp/get-submissions/{compid}/{equipe_id}"
            response = requests.get(api_url)
            submission_data = response.json()['submissoes']
    
    api_url = f"http://127.0.0.1:8000/api/comp/get-ranking-comp/{compid}"
    response = requests.get(api_url)
    rank_data = response.json()
    ranking_data = rank_data["ranking_top20"]

    api_url = f"http://127.0.0.1:8000/api/comp/get-competition/{compid}"
    response = requests.get(api_url)

    compdata = response.json()
    data = compdata['competition'][0]
    n_eq = compdata['n_teams'][0]
    n_ca = compdata['n_comp'][0]
    
    try:
        data[7] = datetime.fromisoformat(data[7].replace(" ", "T"))
    except (ValueError, TypeError, IndexError):
        pass
    try:
        data[8] = datetime.fromisoformat(data[8].replace(" ", "T"))
    except (ValueError, TypeError, IndexError):
        pass

    context = {
            "compid": data[0],
            "organizador": data[1],
            "titulo": data[2],
            "descricao": data[3],
            "dificuldade": data[4],
            "flg_oficial": data[5],
            "data_criacao": data[6],
            "data_inicio": data[7],
            "data_fim": data[8],
            "metrica_desempenho": data[9],
            "premiacao": data[10],
            "n_equipes": n_eq[0],
            "n_comp": n_ca[0],
            "user_name": request.session.get('user_name'),
            "user_has_team": equipe_id is not None,
            "equipe_id": equipe_id,
            "team_members": team_members,
            "current_user_id": user_id,
            "submissoes": submission_data,
            "ranking_top20": ranking_data
        }

    if compid%2:
        return render(request, "comp/comp_pred.html", context = context)
    else:
        return render(request, "comp/comp_simul.html", context = context)


def ranking(request):
    resp = requests.get("http://127.0.0.1:8000/api/user/get-all-users/")
    rankinglist = resp.json()['users']

    context = {
        "rankinglist" : rankinglist,
        "user_name": request.session.get('user_name')
    }
    return render(request, "ranking/ranking.html", context)

def reports(request):
    context = {
        "user_name": request.session.get('user_name')
    }
    return render(request, "reports/reports.html", context)

def user(request):
    user_id = request.session.get('user_id')
    if not user_id:
        messages.error(request, 'Você precisa estar logado para ver seu perfil.')
        return redirect('main:login')

    is_organizer = check_if_user_is_organizer(user_id)

    api_url = f"http://127.0.0.1:8000/api/user/get-user-prizes/{user_id}/"
    resp = requests.get(api_url)
    user_prizes = resp.json()['user_prizes']
    
    context = {
        'is_organizer': is_organizer,
        "user_name": request.session.get('user_name'),
        "user_prizes": user_prizes
    }
    
    return render(request, "user/user.html", context)

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        senha_form = request.POST.get('senha')

        user_data = fetch_user_auth_data_by_email(email)

        if user_data and check_password(senha_form, user_data[2]):
            request.session['user_id'] = data[0]
            request.session['user_name'] = data[1]
            
            messages.success(request, 'Login realizado com sucesso!')
            
            return redirect('main:index')

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
                messages.success(request, 'Conta criada com sucesso!')
                return redirect('main:login')
            else:
                error_msg = data.get('error', 'Ocorreu um erro desconhecido.')
                messages.error(request, error_msg)
        
        except requests.exceptions.RequestException as e:
            messages.error(request, f"Erro de conexão com a API: {e}")

        return render(request, "user/register_user.html")

    return render(request, "user/register_user.html")

def logout_view(request):
    try:
        del request.session['user_id']
        del request.session['user_name']
    except KeyError:
        pass 
    return redirect('main:index')

def become_organizer(request):
    if request.method != 'POST':
        return redirect('main:user-profile')

    user_id = request.session.get('user_id')
    cpf = request.POST.get('cpf')

    if not user_id:
        messages.error(request, 'Sessão expirada. Faça login novamente.')
        return redirect('main:login')
    
    payload = {
        'id_usuario': user_id,
        'cpf': cpf
    }

    try:
        api_url = "http://127.0.0.1:8000/api/user/create-organizer/"
        response = requests.post(api_url, data=payload)
        data = response.json()

        if response.status_code == 201:
            messages.success(request, 'Você agora é um organizador!')
        else:
            messages.error(request, data.get('error', 'Um erro ocorreu.'))
            
    except requests.exceptions.RequestException as e:
        messages.error(request, f"Erro de conexão com a API: {e}")

    return redirect('main:user-profile')

def create_team_view(request, compid):
    user_id = request.session.get('user_id')
    if not user_id:
        messages.error(request, 'Você precisa estar logado para criar uma equipe.')
        return redirect('main:login')
    
    if request.method == 'POST':
        nome_equipe = request.POST.get('nome_equipe')
        
        payload = {
            'compid': compid,
            'id_competidor': user_id,
            'nome_equipe': nome_equipe,
            'members': request.POST.getlist('members')
        }
        
        try:
            api_url = "http://127.0.0.1:8000/api/comp/create-team/"
            response = requests.post(api_url, data=payload)
            data = response.json()

            if response.status_code == 201:
                messages.success(request, f"Equipe '{nome_equipe}' criada com sucesso!")
                return redirect('main:comp-viewer', compid=compid)
            else:
                messages.error(request, data.get('error', 'Ocorreu um erro desconhecido.'))
        
        except requests.exceptions.RequestException as e:
            messages.error(request, f"Erro de conexão com a API: {e}")

    context = {
        "user_name": request.session.get('user_name'),
        "compid": compid,
        "current_user_id": user_id
    }
    return render(request, "equipe/equipe_form.html", context)

def comp_submission(request, compid, equipeid):
    if request.method == 'POST':
        user_id = request.session.get('user_id')
        if not user_id:
            messages.error(request, 'Você precisa estar logado para enviar uma submissão.')
            return redirect('main:login') 

        payload = request.POST.copy()
        files = request.FILES

        try:
            api_url = f"http://127.0.0.1:8000/api/comp/post-submission/{compid}/{equipeid}/"
            response = requests.post(
                api_url,
                data=payload,
                files={'submission-input': files.get('submission-input')}
            )

            data = response.json()

            if response.status_code == 201:
                messages.success(request, 'Submissão criada com sucesso!')
                return redirect('main:comp')
            else:
                error = data.get("error", "Erro desconhecido")
                messages.error(request, error)
        
        except Exception as e:
            messages.error(request, f"Erro de conexão com a API: {e}")

    return redirect('main:comp')

def comp_report_view(request, compid):
    api_url = f"http://127.0.0.1:8000/api/comp/get-competition/{compid}"
    response = requests.get(api_url)
    
    comp_title = "Relatório"
    if response.ok and response.json().get('competition'):
        comp_title = response.json()['competition'][0][2]

    context = {
        "user_name": request.session.get('user_name'),
        "compid": compid,
        "comp_title": comp_title
    }
    return render(request, "reports/comp_report.html", context)