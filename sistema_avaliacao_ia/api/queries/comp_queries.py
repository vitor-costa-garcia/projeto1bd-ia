from django.db import IntegrityError, connection, transaction
from django.http import JsonResponse, FileResponse
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import FileSystemStorage
from datetime import date
import os
from django.contrib.auth.hashers import make_password

def get_all_competitions(request):
    with connection.cursor() as cursor:
        cursor.execute(
                    """
                    SELECT 
                        A.id_competicao,
                        A.titulo,
                        A.descricao,
                        'Predição' as tipo,
                        B.nome as nome_organizador,
                        A.data_inicio,
                        A.data_fim,
                        A.flg_oficial,
                        A.dificuldade,
                        A.premiacao,
                        COALESCE(EQ.team_count, 0) AS total_equipes
                    FROM
                        competicao_pred A
                    JOIN 
                        usuario B ON A.id_org_competicao = B.id
                    LEFT JOIN 
                        (SELECT id_competicao, id_org_competicao, COUNT(id) as team_count
                         FROM equipe_pred
                         GROUP BY id_competicao, id_org_competicao) AS EQ
                    ON A.id_competicao = EQ.id_competicao AND A.id_org_competicao = EQ.id_org_competicao

                    UNION

                    SELECT 
                        A.id_competicao,
                        A.titulo,
                        A.descricao,
                        'Simulação' as tipo,
                        B.nome as nome_organizador,
                        A.data_inicio,
                        A.data_fim,
                        A.flg_oficial,
                        A.dificuldade,
                        A.premiacao,
                        COALESCE(EQ.team_count, 0) AS total_equipes
                    FROM
                        competicao_simul A
                    JOIN 
                        usuario B ON A.id_org_competicao = B.id
                    LEFT JOIN 
                        (SELECT id_competicao, id_org_competicao, COUNT(id) as team_count
                         FROM equipe_simul
                         GROUP BY id_competicao, id_org_competicao) AS EQ
                    ON A.id_competicao = EQ.id_competicao AND A.id_org_competicao = EQ.id_org_competicao
                    """
                    )

        result = cursor.fetchall()
        return JsonResponse({"competitions":result})

def get_predict_competitions(request):
    with connection.cursor() as cursor:
        cursor.execute(
                    """
                    SELECT 
                        A.id_competicao,
                        A.titulo,
                        'Predição' as tipo,
                        B.nome as nome_organizador,
                        A.data_inicio,
                        A.data_fim,
                        A.flg_oficial,
                        A.dificuldade
                    FROM
                        competicao_pred A, usuario B
                    WHERE
                        A.id_org_competicao = B.id
                    """
                    )

        result = cursor.fetchall()
        return JsonResponse({"competitions":result})


def get_simulation_competitions(request):
    with connection.cursor() as cursor:
        cursor.execute(
                    """
                    SELECT 
                        A.id_competicao,
                        A.titulo,
                        'Simulação' as tipo,
                        B.nome as nome_organizador,
                        A.data_inicio,
                        A.data_fim,
                        A.flg_oficial,
                        A.dificuldade
                    FROM
                        competicao_simul A, usuario B
                    WHERE
                        A.id_org_competicao = B.id
                    """
                    )

        result = cursor.fetchall()
        return JsonResponse({"competitions":result})

def post_submission(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST only endpoint"}, status=405)

    try:
        data = request.POST

        submission = data.get('submission') #dar um jeito de pegar o id da competição aqui

    except:
        pass

def get_nextseq_comp(type, add):
    with connection.cursor() as cursor:
        if type == 0:
            cursor.execute("SELECT nextval('competicao_pred_id_competicao_seq');")
            result = cursor.fetchall()
            if add:
                cursor.execute("SELECT setval('competicao_pred_id_competicao_seq', nextval('competicao_pred_id_competicao_seq'), false);")

        elif type == 1:
            cursor.execute("SELECT nextval('competicao_simul_id_competicao_seq');")
            result = cursor.fetchall()
            if add:
                cursor.execute("SELECT setval('competicao_simul_id_competicao_seq', nextval('competicao_simul_id_competicao_seq'), false);")

    return result[0][0]

@csrf_exempt
def post_competition(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST only endpoint"}, status=405)

    try:
        data = request.POST
        
        id_org = data.get('id_org_competicao')
        tipo_comp = data.get('tipo')
        
        flg_oficial = data.get('oficial', '0')
        premiacao = data.get('premiacao') or None

        if premiacao:
            premiacao = premiacao.replace(',', '.')

        if flg_oficial == '0':
            premiacao = None
        elif flg_oficial == '1':
            if not premiacao or float(premiacao) <= 0:
                return JsonResponse({"error": "Competições oficiais devem ter uma premiação maior que R$ 0,00."}, status=400)        
        
        data_inicio = data.get('data_inicio') or None
        data_fim = data.get('data_fim') or None
        
        if not data_inicio or not data_fim:
            return JsonResponse({"error": "Data de início e fim são obrigatórias."}, status=400)

        with connection.cursor() as cursor:
            new_comp_id = None 
            
            if tipo_comp == '0':
                metrica = data.get('metrica_predicao')

                nextid = get_nextseq_comp(type=0, add=False)
                
                cursor.execute(
                    """
                    INSERT INTO competicao_pred 
                    (id_competicao, id_org_competicao, flg_oficial, titulo, descricao, dificuldade, 
                     data_inicio, data_fim, metrica_desempenho, 
                     premiacao,
                     dataset_tt, dataset_submissao, dataset_gabarito) 
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    RETURNING id_competicao
                    """,
                    [
                        nextid, id_org, flg_oficial, data.get('titulo'), data.get('descricao'), data.get('dificuldade'),
                        data_inicio, data_fim, metrica,
                        premiacao,
                        'temp', 'temp', 'temp' 
                    ]
                )
                new_comp_id = cursor.fetchone()[0]

                f_tt = salvar_arquivo(request.FILES['dataset-tt'], new_comp_id, 'datasets')
                f_sub = salvar_arquivo(request.FILES['dataset-submissao'], new_comp_id, 'datasets')
                f_gab = salvar_arquivo(request.FILES['dataset-gabarito'], new_comp_id, 'datasets')

                cursor.execute(
                    """
                    UPDATE competicao_pred 
                    SET dataset_tt = %s, dataset_submissao = %s, dataset_gabarito = %s
                    WHERE id_competicao = %s AND id_org_competicao = %s
                    """,
                    [f_tt, f_sub, f_gab, new_comp_id, id_org]
                )

                get_nextseq_comp(type=0, add=True)


            elif tipo_comp == '1':
                metrica = data.get('metrica_simulacao')

                nextid = get_nextseq_comp(type=1, add=False)
                
                cursor.execute(
                    """
                    INSERT INTO competicao_simul
                    (id_competicao, id_org_competicao, flg_oficial, titulo, descricao, dificuldade, 
                     data_inicio, data_fim, metrica_desempenho, 
                     premiacao, ambiente)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    RETURNING id_competicao
                    """,
                    [
                        nextid, id_org, flg_oficial, data.get('titulo'), data.get('descricao'), data.get('dificuldade'),
                        data_inicio, data_fim, metrica,
                        premiacao,
                        'temp' 
                    ]
                )
                new_comp_id = cursor.fetchone()[0]
                
                f_ambiente = salvar_arquivo(request.FILES['ambiente'], new_comp_id, 'ambientes')
                
                cursor.execute(
                    """
                    UPDATE competicao_simul
                    SET ambiente = %s
                    WHERE id_competicao = %s AND id_org_competicao = %s
                    """,
                    [f_ambiente, new_comp_id, id_org]
                )

                get_nextseq_comp(type=1, add=True)

            else:
                return JsonResponse({"error": "Tipo de competição inválido. Selecione 'Predição' ou 'Simulação'."}, status=400)

        return JsonResponse({"message": "Competição criada com sucesso", "id_competicao": new_comp_id}, status=201)

    except IntegrityError as e:
        return JsonResponse({"error": f"Erro de Banco de Dados: {e}"}, status=400)
    except KeyError as e:
        return JsonResponse({"error": f"Arquivo ou campo obrigatório faltando: {e}"}, status=400)
    except Exception as e:
        return JsonResponse({"error": f"Um erro inesperado ocorreu: {e}"}, status=500)

def get_competition(request, compid):
    
    with connection.cursor() as cursor:
        match int(compid)%2:
            case 1:
                cursor.execute(
                    """
                    SELECT
                        A.id_competicao,
                        B.nome,
                        A.titulo,
                        A.descricao,
                        A.dificuldade,
                        A.flg_oficial,
                        A.data_criacao,
                        A.data_inicio,
                        A.data_fim,
                        A.metrica_desempenho,
                        A.premiacao
                    FROM
                        competicao_pred A, usuario B
                    WHERE
                        A.id_competicao = %s AND
                        B.id = A.id_org_competicao""", [compid])

            case 0:
                cursor.execute(
                    """
                    SELECT
                        A.id_competicao,
                        B.nome,
                        A.titulo,
                        A.descricao,
                        A.dificuldade,
                        A.flg_oficial,
                        A.data_criacao,
                        A.data_inicio,
                        A.data_fim,
                        A.metrica_desempenho,
                        A.premiacao
                    FROM
                        competicao_simul A, usuario B
                    WHERE
                        A.id_competicao = %s AND
                        B.id = A.id_org_competicao""", [compid])

        result = cursor.fetchall()

        cursor.execute(
            """ 
            SELECT
                COUNT(id) as n_equipes
            FROM (
                SELECT * FROM equipe_pred
                UNION ALL
                SELECT * FROM equipe_simul
            ) AS equipes
            WHERE id_competicao = %s
            ;
            """, [compid]
        )

        result_eq = cursor.fetchall() or [0]

        cursor.execute(
            """
            SELECT
                COUNT(id_competidor) AS qtd_competidores_ativos
            FROM (
                SELECT * FROM composicao_equipe_pred
                UNION ALL
                SELECT * FROM composicao_equipe_simul
            )
            WHERE
                data_hora_fim IS NULL AND
                id_competicao  = %s
            ;
            """, [compid]
        )

        result_ca = cursor.fetchall() or [0]

        return JsonResponse({"competition": result, "n_teams": result_eq, "n_comp":result_ca})

def salvar_arquivo(file, id_competicao, tipo_pasta):
    fs = FileSystemStorage(location=f"./uploads/{tipo_pasta}")
    filename = f"{id_competicao}_{file.name}"
    fs.save(filename, file)
    return os.path.join(tipo_pasta, filename)

def download_file(filepath):
    file_path = os.path.join(f"./uploads/{filepath}")
    if os.path.exists(file_path):
        response = FileResponse(open(file_path, "rb"), as_attachment=True)
        return response
    else:
        return JsonResponse({"error": "error downloading the file"}, status=500)
    
def download_competition_file(request, compid, type_file):
    with connection.cursor() as cursor:
        match compid%2:
            case 1:
                match type_file:
                    case 0:
                        cursor.execute("SELECT dataset_tt FROM competicao_pred WHERE id_competicao = %s", [compid])
                        result = cursor.fetchall()[0][0]
                        return download_file(result)

                    case 1:
                        cursor.execute("SELECT dataset_submissao FROM competicao_pred WHERE id_competicao = %s", [compid])
                        result = cursor.fetchall()[0][0]
                        return download_file(result)

            case 0:
                cursor.execute("SELECT ambiente FROM competicao_simul WHERE id_competicao = %s", [compid])
                result = cursor.fetchall()[0][0]
                return download_file(result)

@transaction.atomic
@csrf_exempt
def create_team(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST only endpoint"}, status=405)
    
    try:
        data = request.POST
        compid = int(data.get('compid'))
        id_competidor_criador = data.get('id_competidor')
        nome_equipe = data.get('nome_equipe')
        membros_adicionais_ids = data.getlist('members')

        if not all([compid, id_competidor_criador, nome_equipe]):
            return JsonResponse({"error": "compid, id_competidor, e nome_equipe são obrigatórios."}, status=400)
        
        if not nome_equipe.strip():
            return JsonResponse({"error": "O nome da equipe não pode ser vazio ou conter apenas espaços."}, status=400)
        
        with connection.cursor() as cursor:
            id_org = None
            is_pred = compid % 2
            
            if is_pred:
                cursor.execute("SELECT id_org_competicao FROM competicao_pred WHERE id_competicao = %s", [compid])
            else:
                cursor.execute("SELECT id_org_competicao FROM competicao_simul WHERE id_competicao = %s", [compid])
            
            result = cursor.fetchone()
            if not result:
                return JsonResponse({"error": "Competição não encontrada."}, status=404)
            id_org = result[0]
            
            new_team_id = None
            
            todos_membros = set([id_competidor_criador] + membros_adicionais_ids)

            if is_pred:
                cursor.execute(
                    """
                    INSERT INTO equipe_pred (id_competicao, id_org_competicao, nome)
                    VALUES (%s, %s, %s)
                    RETURNING id
                    """,
                    [compid, id_org, nome_equipe]
                )
                new_team_id = cursor.fetchone()[0]
                
                for member_id in todos_membros:
                    cursor.execute(
                        """
                        INSERT INTO composicao_equipe_pred (id_equipe, id_competicao, id_org_competicao, id_competidor, data_hora_inicio)
                        VALUES (%s, %s, %s, %s, CURRENT_TIMESTAMP)
                        """,
                        [new_team_id, compid, id_org, member_id]
                    )
            else:
                cursor.execute(
                    """
                    INSERT INTO equipe_simul (id_competicao, id_org_competicao, nome)
                    VALUES (%s, %s, %s)
                    RETURNING id
                    """,
                    [compid, id_org, nome_equipe]
                )
                new_team_id = cursor.fetchone()[0]
                
                for member_id in todos_membros:
                    cursor.execute(
                        """
                        INSERT INTO composicao_equipe_simul (id_equipe, id_competicao, id_org_competicao, id_competidor, data_hora_inicio)
                        VALUES (%s, %s, %s, %s, CURRENT_TIMESTAMP)
                        """,
                        [new_team_id, compid, id_org, member_id]
                    )
        
        return JsonResponse({"message": "Equipe criada com sucesso!", "id_equipe": new_team_id}, status=201)

    except IntegrityError as e:
        return JsonResponse({"error": f"Erro de Banco de Dados: {e}"}, status=400)
    except Exception as e:
        return JsonResponse({"error": f"Um erro inesperado ocorreu: {e}"}, status=500)

def get_team_members(compid, equipe_id):
    with connection.cursor() as cursor:
        if compid % 2:
            cursor.execute(
                """
                SELECT u.id, u.nome
                FROM composicao_equipe_pred c
                JOIN usuario u ON c.id_competidor = u.id
                WHERE c.id_equipe = %s AND c.id_competicao = %s AND c.data_hora_fim IS NULL
                """,
                [equipe_id, compid]
            )
        else:
            cursor.execute(
                """
                SELECT u.id, u.nome
                FROM composicao_equipe_simul c
                JOIN usuario u ON c.id_competidor = u.id
                WHERE c.id_equipe = %s AND c.id_competicao = %s AND c.data_hora_fim IS NULL
                """,
                [equipe_id, compid]
            )
        return cursor.fetchall()

@transaction.atomic
@csrf_exempt
def add_member_to_team(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST only endpoint"}, status=405)
    
    try:
        data = request.POST
        compid = int(data.get('compid'))
        equipe_id = int(data.get('equipe_id'))
        id_competidor = int(data.get('id_competidor'))
        
        with connection.cursor() as cursor:
            id_org = None
            is_pred = compid % 2
            
            if is_pred:
                cursor.execute("SELECT id_org_competicao FROM competicao_pred WHERE id_competicao = %s", [compid])
            else:
                cursor.execute("SELECT id_org_competicao FROM competicao_simul WHERE id_competicao = %s", [compid])
            
            result = cursor.fetchone()
            if not result:
                return JsonResponse({"error": "Competição não encontrada."}, status=404)
            id_org = result[0]

            if is_pred:
                cursor.execute(
                    """
                    INSERT INTO composicao_equipe_pred (id_equipe, id_competicao, id_org_competicao, id_competidor, data_hora_inicio)
                    VALUES (%s, %s, %s, %s, CURRENT_TIMESTAMP)
                    """,
                    [equipe_id, compid, id_org, id_competidor]
                )
            else:
                cursor.execute(
                    """
                    INSERT INTO composicao_equipe_simul (id_equipe, id_competicao, id_org_competicao, id_competidor, data_hora_inicio)
                    VALUES (%s, %s, %s, %s, CURRENT_TIMESTAMP)
                    """,
                    [equipe_id, compid, id_org, id_competidor]
                )
        
        return JsonResponse({"message": "Membro adicionado com sucesso."}, status=201)

    except IntegrityError as e:
        return JsonResponse({"error": "Este usuário já está na equipe."}, status=400)
    except Exception as e:
        return JsonResponse({"error": f"Um erro inesperado ocorreu: {e}"}, status=500)

@transaction.atomic
@csrf_exempt
def remove_member_from_team(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST only endpoint"}, status=405)
    
    try:
        data = request.POST
        compid = int(data.get('compid'))
        equipe_id = int(data.get('equipe_id'))
        id_competidor = int(data.get('id_competidor'))
        
        with connection.cursor() as cursor:
            if compid % 2:
                cursor.execute(
                    """
                    UPDATE composicao_equipe_pred
                    SET data_hora_fim = CURRENT_TIMESTAMP
                    WHERE id_equipe = %s AND id_competicao = %s AND id_competidor = %s
                    """,
                    [equipe_id, compid, id_competidor]
                )
            else:
                cursor.execute(
                    """
                    UPDATE composicao_equipe_simul
                    SET data_hora_fim = CURRENT_TIMESTAMP
                    WHERE id_equipe = %s AND id_competicao = %s AND id_competidor = %s
                    """,
                    [equipe_id, compid, id_competidor]
                )
        
        return JsonResponse({"message": "Membro removido com sucesso."}, status=200)

    except Exception as e:
        return JsonResponse({"error": f"Um erro inesperado ocorreu: {e}"}, status=500)