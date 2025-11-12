from django.db import IntegrityError, connection
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
        return JsonResponse({"error": f"Erro ao criar usuário: {e}"}, status=400)
    
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

def check_if_user_is_organizer(user_id):
    with connection.cursor() as cursor:
        cursor.execute(
            "SELECT 1 FROM organizador WHERE id_usuario = %s",
            [user_id]
        )
        result = cursor.fetchone()
    
    return result is not None