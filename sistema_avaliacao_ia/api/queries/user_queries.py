from django.db import connection, IntegrityError, transaction
from django.http import JsonResponse, FileResponse
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import FileSystemStorage
from datetime import date
import os
from django.contrib.auth.hashers import make_password

def get_user(request, id):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM usuario WHERE id = %s", [id])
        result = cursor.fetchall()

    return JsonResponse({"users": result})
    
def get_all_user(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT id, nome, email FROM usuario")
        result =  cursor.fetchall()
    
    return JsonResponse({"users": result})

@csrf_exempt
def create_user(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST only endpoint"}, status=405)
    
    try:
        data = request.POST
        nome = data.get('nome')
        email = data.get('email')
        senha_plana = data.get('senha')
        datanasc = data.get('datanascimento')
        
        numero = data.get('numero') or None
        rua = data.get('rua') or None
        cidade = data.get('cidade') or None
        estado = data.get('estado') or None
        pais = data.get('pais') or None

        if not all([nome, email, senha_plana, datanasc]):
             return JsonResponse({"error": "Campos obrigatórios faltando"}, status=400)

        hashed_password = make_password(senha_plana)

        with connection.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO usuario 
                (nome, email, senha, datanascimento, numero, rua, cidade, estado, pais)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                RETURNING id, nome
                """,
                [nome, email, hashed_password, datanasc, numero, rua, cidade, estado, pais]
            )
            new_user = cursor.fetchone()
            
            return JsonResponse({
                "user_id": new_user[0],
                "user_nome": new_user[1]
            }, status=201)

    except IntegrityError as e:
        return JsonResponse({"error": f"Erro de Banco de Dados: {e}"}, status=400)
    except Exception as e:
        return JsonResponse({"error": f"Um erro inesperado ocorreu: {e}"}, status=500)

@csrf_exempt
def create_organizer(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST only endpoint"}, status=405)

    try:
        data = request.POST
        id_usuario = data.get('id_usuario')
        cpf = data.get('cpf')

        if not id_usuario or not cpf:
            return JsonResponse({"error": "id_usuario e cpf são obrigatórios."}, status=400)

        with connection.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO organizador (id_usuario, cpf)
                VALUES (%s, %s)
                """,
                [id_usuario, cpf]
            )
        
        return JsonResponse({"message": "Usuário registrado como organizador com sucesso."}, status=201)

    except IntegrityError as e:
        error_message = str(e)
        if "UNIQUE_CPF_ORGANIZADOR" in error_message:
            return JsonResponse({"error": "Este CPF já está em uso."}, status=400)
        if "PK_ID_USUARIO_ORGANIZADOR" in error_message:
            return JsonResponse({"error": "Este usuário já é um organizador."}, status=400)
        return JsonResponse({"error": f"Erro de banco de dados: {e}"}, status=400)
    
    except Exception as e:
        return JsonResponse({"error": f"Um erro inesperado ocorreu: {e}"}, status=500)

def fetch_user_auth_data_by_email(email):
    with connection.cursor() as cursor:
        cursor.execute(
            "SELECT id, nome, senha FROM usuario WHERE email = %s",
            [email]
        )
        user_data = cursor.fetchone()
    
    return user_data

def check_if_user_is_organizer(user_id):
    with connection.cursor() as cursor:
        cursor.execute(
            "SELECT 1 FROM organizador WHERE id_usuario = %s",
            [user_id]
        )
        result = cursor.fetchone()
    
    return result is not None

def search_users(request):
    query = request.GET.get('q', '').strip()
    current_user_id = request.GET.get('exclude', 0)
    
    if not query:
        return JsonResponse({"users": []})

    with connection.cursor() as cursor:
        search_query = f"%{query}%"
        cursor.execute(
            """
            SELECT id, nome FROM usuario
            WHERE nome ILIKE %s AND id != %s
            LIMIT 10
            """,
            [search_query, current_user_id]
        )
        users = cursor.fetchall()
    
    return JsonResponse({"users": users})