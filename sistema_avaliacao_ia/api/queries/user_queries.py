from django.db import connection
from django.http import JsonResponse
from django.contrib.auth.hashers import make_password
from django.views.decorators.csrf import csrf_exempt

def get_user(request, id):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM usuario WHERE id = %d", [id])
        result = cursor.fetchall()

    return JsonResponse({"users": result})

def fetch_user_auth_data_by_email(email):
    with connection.cursor() as cursor:
        cursor.execute(
            "SELECT id, nome, senha FROM usuario WHERE email = %s",
            [email]
        )
        user_data = cursor.fetchone()
    
    return user_data
    
def get_all_user(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT id, nome, email FROM usuario", [id])
        result =  cursor.fetchall()
    
    return JsonResponse({"users": result})

@csrf_exempt
def create_user(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST only endpoint"}, status=405)

    try:
        nome = request.POST.get('nome')
        email = request.POST.get('email')
        senha_plana = request.POST.get('senha')
        datanasc = request.POST.get('datanascimento')
        
        numero = request.POST.get('numero') or None
        rua = request.POST.get('rua') or None
        cidade = request.POST.get('cidade') or None
        estado = request.POST.get('estado') or None
        pais = request.POST.get('pais') or None

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

    except Exception as e:
        # Erro (ex: email duplicado)
        return JsonResponse({"error": f"Erro ao criar usuário: {e}"}, status=400)