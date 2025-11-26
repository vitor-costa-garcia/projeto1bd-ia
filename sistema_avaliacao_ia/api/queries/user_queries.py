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

def check_user_team_membership(user_id, compid):
    with connection.cursor() as cursor:
        cursor.execute(
            """
            SELECT id_equipe FROM composicao_equipe_pred
            WHERE id_competidor = %s AND id_competicao = %s AND data_hora_fim IS NULL
            UNION ALL
            SELECT id_equipe FROM composicao_equipe_simul
            WHERE id_competidor = %s AND id_competicao = %s AND data_hora_fim IS NULL
            LIMIT 1
            """,
            [user_id, compid, user_id, compid]
        )
        result = cursor.fetchone()
    return result[0] if result else None

def get_user_prizes(request, userid):
    with connection.cursor() as cursor:
        cursor.execute(
            """
            WITH todos_premios AS (
                SELECT tipo, valor FROM premios_competidor_pred WHERE id_competidor = %s
                UNION ALL
                SELECT tipo, valor FROM premios_competidor_simul WHERE id_competidor = %s
            ),
            tipos AS (
                SELECT * FROM (VALUES (0), (1), (2), (3)) AS t(tipo)
            )
            SELECT
                t.tipo,
                CASE 
                    WHEN t.tipo = 3 THEN COALESCE(SUM(tp.valor), 0)
                    ELSE COALESCE(COUNT(tp.tipo), 0)
                END as total
            FROM
                tipos t
            LEFT JOIN
                todos_premios tp
                ON t.tipo = tp.tipo
            GROUP BY
                t.tipo
            ORDER BY 
                t.tipo ASC;
            """,
            [userid, userid]
        )

        result = cursor.fetchall()

    return JsonResponse({"user_prizes": result})

def get_user_stats(request, userid):
    with connection.cursor() as cursor:
        cursor.execute(
            """
            SELECT COUNT(*) FROM (
                SELECT id_competicao FROM composicao_equipe_pred WHERE id_competidor = %s
                UNION
                SELECT id_competicao FROM composicao_equipe_simul WHERE id_competidor = %s
            ) as total
            """, [userid, userid]
        )
        total_comps = cursor.fetchone()[0]

        cursor.execute(
            """
            SELECT COUNT(*) FROM (
                SELECT s.id_equipe FROM submissao_equipe_pred s
                JOIN composicao_equipe_pred c ON s.id_equipe = c.id_equipe
                WHERE c.id_competidor = %s
                UNION ALL
                SELECT s.id_equipe FROM submissao_equipe_simul s
                JOIN composicao_equipe_simul c ON s.id_equipe = c.id_equipe
                WHERE c.id_competidor = %s
            ) as total
            """, [userid, userid]
        )
        total_subs = cursor.fetchone()[0]

        cursor.execute(
            """
            SELECT TO_CHAR(data_envio, 'YYYY-MM-DD') as dia, COUNT(*) as qtd
            FROM (
                SELECT data_hora_envio as data_envio FROM submissao_equipe_pred s
                JOIN composicao_equipe_pred c ON s.id_equipe = c.id_equipe
                WHERE c.id_competidor = %s
                UNION ALL
                SELECT data_hora_envio as data_envio FROM submissao_equipe_simul s
                JOIN composicao_equipe_simul c ON s.id_equipe = c.id_equipe
                WHERE c.id_competidor = %s
            ) as envios
            GROUP BY dia
            ORDER BY dia ASC
            LIMIT 30
            """, [userid, userid]
        )
        daily_activity = cursor.fetchall()

        cursor.execute(
            """
            SELECT 'Predição', COUNT(*) FROM composicao_equipe_pred WHERE id_competidor = %s
            UNION ALL
            SELECT 'Simulação', COUNT(*) FROM composicao_equipe_simul WHERE id_competidor = %s
            """, [userid, userid]
        )
        comp_types = cursor.fetchall()

    return JsonResponse({
        "stats": {
            "total_competitions": total_comps,
            "total_submissions": total_subs,
            "activity_dates": [row[0] for row in daily_activity],
            "activity_counts": [row[1] for row in daily_activity],
            "type_labels": [row[0] for row in comp_types],
            "type_counts": [row[1] for row in comp_types]
        }
    })

def get_global_ranking(request):
    sort_by = request.GET.get('sort', 'gold')
    
    order_clause = "COALESCE(s.ouro, 0) DESC, COALESCE(s.prata, 0) DESC, COALESCE(s.bronze, 0) DESC"
    
    if sort_by == 'money':
        order_clause = "COALESCE(s.dinheiro, 0) DESC"
    elif sort_by == 'comps':
        order_clause = "COALESCE(p.total_comps, 0) DESC"
    elif sort_by == 'points':
        order_clause = "COALESCE(s.pontos_totais, 0) DESC"
    elif sort_by == 'name':
        order_clause = "u.nome ASC"

    with connection.cursor() as cursor:
        cursor.execute(
            f"""
            WITH user_stats AS (
                SELECT
                    id_competidor,
                    COUNT(CASE WHEN tipo = 0 THEN 1 END) as ouro,
                    COUNT(CASE WHEN tipo = 1 THEN 1 END) as prata,
                    COUNT(CASE WHEN tipo = 2 THEN 1 END) as bronze,
                    SUM(COALESCE(valor, 0)) as dinheiro,
                    SUM(
                        CASE 
                            WHEN classificacao = 1 THEN 1000
                            WHEN classificacao = 2 THEN 500
                            WHEN classificacao = 3 THEN 250
                            WHEN classificacao <= 10 THEN 100
                            ELSE 10
                        END
                    ) as pontos_totais
                FROM (
                    SELECT id_competidor, tipo, valor, classificacao FROM premios_competidor_pred
                    UNION ALL
                    SELECT id_competidor, tipo, valor, classificacao FROM premios_competidor_simul
                ) all_prizes
                GROUP BY id_competidor
            ),
            participation AS (
                SELECT id_competidor, COUNT(*) as total_comps
                FROM (
                    SELECT id_competidor FROM composicao_equipe_pred
                    UNION ALL
                    SELECT id_competidor FROM composicao_equipe_simul
                ) all_comps
                GROUP BY id_competidor
            )
            SELECT
                u.id,
                u.nome,
                COALESCE(s.ouro, 0),
                COALESCE(s.prata, 0),
                COALESCE(s.bronze, 0),
                COALESCE(s.dinheiro, 0),
                COALESCE(p.total_comps, 0),
                COALESCE(s.pontos_totais, 0)
            FROM usuario u
            LEFT JOIN user_stats s ON u.id = s.id_competidor
            LEFT JOIN participation p ON u.id = p.id_competidor
            ORDER BY {order_clause}
            LIMIT 100;
            """
        )
        ranking_data = cursor.fetchall()

    return JsonResponse({"ranking": ranking_data})
