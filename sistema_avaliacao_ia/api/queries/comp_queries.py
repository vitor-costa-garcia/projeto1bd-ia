from django.db import IntegrityError, connection, transaction
from django.http import JsonResponse, FileResponse
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import FileSystemStorage
import datetime
import os
from django.contrib.auth.hashers import make_password
import pandas as pd
import numpy as np
from django.conf import settings
import math

def rmse_from_csv(file1, file2):

    df1 = pd.read_csv(file1)
    df2 = pd.read_csv(file2)

    if df1.shape != df2.shape:
        raise ValueError(
            f"CSV shapes differ: {df1.shape} vs {df2.shape}"
        )

    arr1 = df1.to_numpy(dtype=float)
    arr2 = df2.to_numpy(dtype=float)

    rmse = np.sqrt(np.mean((arr1 - arr2) ** 2))
    return rmse

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
                        COALESCE(EQ.team_count, 0) AS total_equipes,
                        A.data_criacao
                    FROM
                        competicao_pred A
                    JOIN 
                        usuario B ON A.id_org_competicao = B.id
                    LEFT JOIN 
                        (SELECT id_competicao, COUNT(id) as team_count
                         FROM equipe_pred
                         GROUP BY id_competicao) AS EQ
                    ON A.id_competicao = EQ.id_competicao
                    WHERE A.flg_deletada = false

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
                        COALESCE(EQ.team_count, 0) AS total_equipes,
                        A.data_criacao
                    FROM
                        competicao_simul A
                    JOIN 
                        usuario B ON A.id_org_competicao = B.id
                    LEFT JOIN 
                        (SELECT id_competicao, COUNT(id) as team_count
                         FROM equipe_simul
                         GROUP BY id_competicao) AS EQ
                    ON A.id_competicao = EQ.id_competicao
                    WHERE A.flg_deletada = false

                    ORDER BY data_criacao DESC
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
                        A.id_org_competicao = B.id AND A.flg_deletada = false
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
                        A.id_org_competicao = B.id AND A.flg_deletada = false
                    """
                    )

        result = cursor.fetchall()
        return JsonResponse({"competitions":result})

@csrf_exempt
def post_submission(request, compid, equipeid):
    if request.method != "POST":
        return JsonResponse({"error": "POST only endpoint"}, status=405)

    try:
        submission = request.FILES.get('submission-input')
        if not submission:
            return JsonResponse({"error": "Nenhum arquivo enviado"}, status=400)
        
        is_pred = compid % 2
        id_org = None

        with connection.cursor() as cursor:
            if is_pred:
                cursor.execute("SELECT id_org_competicao, dataset_gabarito FROM competicao_pred WHERE id_competicao = %s", [compid])
            else:
                cursor.execute("SELECT id_org_competicao, ambiente FROM competicao_simul WHERE id_competicao = %s", [compid])
            
            result = cursor.fetchone()
            if not result:
                return JsonResponse({"error": "Competição não encontrada"}, status=404)
            
            id_org = result[0]
            resource_path = result[1]

            if is_pred:
                cursor.execute("SELECT COUNT(*) FROM submissao_equipe_pred WHERE id_equipe = %s AND id_competicao = %s", [equipeid, compid])
            else:
                cursor.execute("SELECT COUNT(*) FROM submissao_equipe_simul WHERE id_equipe = %s AND id_competicao = %s", [equipeid, compid])
            
            nsub = cursor.fetchone()[0]

        fs = FileSystemStorage(location="./uploads/submissoes")
        filename = f"{compid}_{equipeid}_{nsub}.csv"
        fs.save(filename, submission)
        submission_path = os.path.join(settings.BASE_DIR, 'uploads', 'submissoes', filename)
        
        score = 0.0
        if is_pred:
            gabarito_path = os.path.join(settings.BASE_DIR, 'uploads', resource_path)
            try:
                score = rmse_from_csv(submission_path, gabarito_path)
            except Exception as e:
                 return JsonResponse({"error": f"Erro ao calcular RMSE: {str(e)}"}, status=400)
        else:
            score = 0.0

        with connection.cursor() as cursor:
            if is_pred:
                cursor.execute("""
                    INSERT INTO submissao_equipe_pred (
                        id_equipe,
                        id_competicao,
                        id_org_competicao,
                        data_hora_envio,
                        arq_submissao,
                        score
                    ) VALUES (%s, %s, %s, NOW(), %s, %s)
                """, [equipeid, compid, id_org, f"submissoes/{filename}", float(score)])
            else:
                cursor.execute("""
                    INSERT INTO submissao_equipe_simul (
                        id_equipe,
                        id_competicao,
                        id_org_competicao,
                        data_hora_envio,
                        arq_submissao,
                        score
                    ) VALUES (%s, %s, %s, NOW(), %s, %s)
                """, [equipeid, compid, id_org, f"submissoes/{filename}", float(score)])

        return JsonResponse({"rmse": score, "score": score}, status=201)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

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

@transaction.atomic
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

        regras = request.POST.getlist('regra')

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
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
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

                if regras:
                    for i, regra in enumerate(regras):
                        cursor.execute(
                            "INSERT INTO competicao_regras_pred (id_competicao, n_ordem, regra) VALUES (%s, %s, %s)",
                            [new_comp_id, i + 1, regra]
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

                if regras:
                    for i, regra in enumerate(regras):
                        cursor.execute(
                            "INSERT INTO competicao_regras_simul (id_competicao, n_ordem, regra) VALUES (%s, %s, %s)",
                            [new_comp_id, i + 1, regra]
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
                        A.premiacao,
                        A.id_org_competicao
                    FROM
                        competicao_pred A, usuario B
                    WHERE
                        A.id_competicao = %s AND
                        B.id = A.id_org_competicao AND A.flg_deletada = false""", [compid])

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
                        A.premiacao,
                        A.id_org_competicao
                    FROM
                        competicao_simul A, usuario B
                    WHERE
                        A.id_competicao = %s AND
                        B.id = A.id_org_competicao AND A.flg_deletada = false""", [compid])

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
    
def get_submissions(request, compid, equipeid):
    with connection.cursor() as cursor:
        match int(compid)%2:
            case 1:
                cursor.execute(
                    """
                    SELECT
                        data_hora_envio,
                        score
                    FROM
                        submissao_equipe_pred
                    WHERE
                        id_competicao = %s AND
                        id_equipe = %s""", [compid, equipeid]
                )
            case 0:
                cursor.execute(
                    """
                    SELECT
                        data_hora_envio,
                        score
                    FROM
                        submissao_equipe_simul
                    WHERE
                        id_competicao = %s AND
                        id_equipe = %s""", [compid, equipeid]
                )
        result_sub = cursor.fetchall() or [0]
    return JsonResponse({"submissoes": result_sub})

def get_top20_ranking(request, compid):
    with connection.cursor() as cursor:
        match int(compid) % 2:
            case 1:
                cursor.execute("""
                    SELECT 
                        e.nome AS equipe_nome,
                        MIN(s.score) AS best_score
                    FROM 
                        submissao_equipe_pred s
                    JOIN 
                        equipe_pred e ON e.id = s.id_equipe
                    WHERE 
                        s.id_competicao = %s
                    GROUP BY 
                        e.nome
                    ORDER BY 
                        best_score ASC
                    LIMIT 20;""",
                    [compid]
                )

            case 0:
                cursor.execute(
                    """
                    SELECT 
                        e.nome AS equipe_nome,
                        MIN(s.score) AS best_score
                    FROM 
                        submissao_equipe_simul s
                    JOIN 
                        equipe_simul e ON e.id = s.id_equipe
                    WHERE 
                        s.id_competicao = %s
                    GROUP BY 
                        e.nome
                    ORDER BY 
                        best_score ASC
                    LIMIT 20;
                    """,
                    [compid]
                )
        ranking = cursor.fetchall()
    return JsonResponse({"ranking_top20": ranking})

@transaction.atomic
def verify_end_competition(request, compid):
    with connection.cursor() as cursor:
        has_ended = False
        has_awarded = True
        is_official = False
        premiacao_total = 0.0
        is_pred = int(compid) % 2

        if is_pred:
            cursor.execute(
                """
                SELECT data_fim <= NOW(), flg_premiada, flg_oficial, premiacao
                FROM competicao_pred
                WHERE id_competicao = %s
                """,
                [compid]
            )
        else:
            cursor.execute(
                """
                SELECT data_fim <= NOW(), flg_premiada, flg_oficial, premiacao
                FROM competicao_simul
                WHERE id_competicao = %s
                """,
                [compid]
            )
        
        result = cursor.fetchone()
        if not result:
            return JsonResponse({"error": "Competição não encontrada"}, status=404)

        has_ended, has_awarded, is_official, premiacao_total = result

        if not has_ended or has_awarded:
            return JsonResponse({"message": "Competição não elegível para premiação."})

        top_50_teams = []
        if is_pred:
            cursor.execute("""
                SELECT 
                    e.id AS id_equipe,
                    MIN(s.score) AS best_score
                FROM 
                    submissao_equipe_pred s
                JOIN 
                    equipe_pred e ON e.id = s.id_equipe
                WHERE 
                    s.id_competicao = %s
                GROUP BY 
                    e.id
                ORDER BY 
                    best_score ASC
                LIMIT 50;
                """,
                [compid]
            )
        else:
            cursor.execute("""
                SELECT 
                    e.id AS id_equipe,
                    MIN(s.score) AS best_score
                FROM 
                    submissao_equipe_simul s
                JOIN 
                    equipe_simul e ON e.id = s.id_equipe
                WHERE 
                    s.id_competicao = %s
                GROUP BY 
                    e.id
                ORDER BY 
                    best_score ASC
                LIMIT 50;
                """,
                [compid]
            )
        top_50_teams = cursor.fetchall()

        for i, team in enumerate(top_50_teams):
            team_id = team[0]
            classificacao = i + 1

            tipo = 0
            if classificacao > 15:
                tipo = 2
            elif classificacao > 5:
                tipo = 1
            
            team_members = []
            if is_pred:
                cursor.execute("""
                    SELECT id_competidor FROM composicao_equipe_pred
                    WHERE id_equipe = %s AND id_competicao = %s AND data_hora_fim IS NULL
                    """,
                    [team_id, compid]
                )
            else:
                cursor.execute("""
                    SELECT id_competidor FROM composicao_equipe_simul
                    WHERE id_equipe = %s AND id_competicao = %s AND data_hora_fim IS NULL
                    """,
                    [team_id, compid]
                )
            team_members = cursor.fetchall()
            
            if not team_members:
                continue 

            valor_premio = 0
            if is_official and premiacao_total and float(premiacao_total) > 0:
                valor_premio = float(premiacao_total) / len(team_members)

            for member in team_members:
                competitor_id = member[0]
                if is_pred:
                    cursor.execute(
                        """
                        INSERT INTO premios_competidor_pred (id_competidor, id_competicao, data_recebimento, tipo, classificacao, valor)
                        VALUES (%s, %s, NOW(), %s, %s, %s)
                        """,
                        [competitor_id, compid, tipo, classificacao, valor_premio if valor_premio > 0 else None]
                    )
                else:
                     cursor.execute(
                        """
                        INSERT INTO premios_competidor_simul (id_competidor, id_competicao, data_recebimento, tipo, classificacao, valor)
                        VALUES (%s, %s, NOW(), %s, %s, %s)
                        """,
                        [competitor_id, compid, tipo, classificacao, valor_premio if valor_premio > 0 else None]
                    )

        if is_pred:
            cursor.execute(
                "UPDATE competicao_pred SET flg_premiada = true WHERE id_competicao = %s",
                [compid]
            )
        else:
            cursor.execute(
                "UPDATE competicao_simul SET flg_premiada = true WHERE id_competicao = %s",
                [compid]
            )

    return JsonResponse({"message": "Premiação processada com sucesso."})


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
            if not result or result[0] is None:
                return JsonResponse({"error": "Competição não encontrada ou dados da competição corrompidos (Organizador não encontrado)."}, status=404)
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

@transaction.atomic
@csrf_exempt
def delete_competition(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST only endpoint"}, status=405)
    
    try:
        data = request.POST
        compid = int(data.get('compid'))
        id_org = int(data.get('id_org'))
        user_id = int(data.get('user_id'))

        if id_org != user_id:
            return JsonResponse({"error": "Usuário não autorizado."}, status=403)
            
        with connection.cursor() as cursor:
            if compid % 2:
                cursor.execute(
                    "UPDATE competicao_pred SET flg_deletada = true WHERE id_competicao = %s AND id_org_competicao = %s",
                    [compid, id_org]
                )
            else:
                cursor.execute(
                    "UPDATE competicao_simul SET flg_deletada = true WHERE id_competicao = %s AND id_org_competicao = %s",
                    [compid, id_org]
                )
        
        return JsonResponse({"message": "Competição deletada com sucesso."}, status=200)

    except Exception as e:
        return JsonResponse({"error": f"Um erro inesperado ocorreu: {e}"}, status=500)

def get_competition_stats(request, compid):
    is_pred = int(compid) % 2
    table_sub = 'submissao_equipe_pred' if is_pred else 'submissao_equipe_simul'
    table_team = 'equipe_pred' if is_pred else 'equipe_simul'

    with connection.cursor() as cursor:
        cursor.execute(f"SELECT COUNT(*) FROM {table_sub} WHERE id_competicao = %s", [compid])
        total_submissions = cursor.fetchone()[0]

        cursor.execute(f"SELECT AVG(score) FROM {table_sub} WHERE id_competicao = %s", [compid])
        avg_score = cursor.fetchone()[0] or 0.0

        cursor.execute(f"SELECT MAX(score) FROM {table_sub} WHERE id_competicao = %s", [compid])
        best_score = cursor.fetchone()[0] or 0.0

        cursor.execute(
            f"""
            SELECT DATE(data_hora_envio) as dia, COUNT(*) 
            FROM {table_sub} 
            WHERE id_competicao = %s 
            GROUP BY dia 
            ORDER BY dia ASC
            """, 
            [compid]
        )
        daily_submissions = cursor.fetchall()

        cursor.execute(
            f"""
            SELECT MAX(score) 
            FROM {table_sub} 
            WHERE id_competicao = %s 
            GROUP BY id_equipe
            """, 
            [compid]
        )
        team_scores = [row[0] for row in cursor.fetchall()]

    return JsonResponse({
        "stats": {
            "total_submissions": total_submissions,
            "avg_score": round(avg_score, 4),
            "best_score": round(best_score, 4),
            "daily_submissions_dates": [row[0].strftime('%Y-%m-%d') for row in daily_submissions],
            "daily_submissions_counts": [row[1] for row in daily_submissions],
            "team_scores": team_scores
        }
    })

def get_regras_competition(request, compid):
    is_pred = int(compid) % 2
    table_regras = 'competicao_regras_pred' if is_pred else 'competicao_regras_simul'

    with connection.cursor() as cursor:
        cursor.execute(
            f"SELECT regra FROM {table_regras} WHERE id_competicao = %s ORDER BY n_ordem",
            [compid]
        )
        regras = [row[0] for row in cursor.fetchall()]

    return JsonResponse({"regras": regras})

@transaction.atomic
def process_expired_competitions():
    messages_log = []
    
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT id_competicao, 'PRED' as tipo FROM competicao_pred 
            WHERE data_fim <= NOW() AND flg_premiada = false AND flg_deletada = false
            UNION
            SELECT id_competicao, 'SIMUL' as tipo FROM competicao_simul 
            WHERE data_fim <= NOW() AND flg_premiada = false AND flg_deletada = false
        """)
        pending_comps = cursor.fetchall()

        if not pending_comps:
            return "Nenhuma competição pendente."

        for comp_row in pending_comps:
            compid = comp_row[0]
            comp_type_str = comp_row[1]
            is_pred = (comp_type_str == 'PRED')
            

            table_comp = 'competicao_pred' if is_pred else 'competicao_simul'
            table_sub = 'submissao_equipe_pred' if is_pred else 'submissao_equipe_simul'
            table_team = 'equipe_pred' if is_pred else 'equipe_simul'
            table_members = 'composicao_equipe_pred' if is_pred else 'composicao_equipe_simul'
            table_prizes = 'premios_competidor_pred' if is_pred else 'premios_competidor_simul'

            cursor.execute(f"SELECT flg_oficial, premiacao, id_org_competicao FROM {table_comp} WHERE id_competicao = %s", [compid])
            comp_info = cursor.fetchone()
            
            is_official = comp_info[0]
            total_money = comp_info[1]
            id_org = comp_info[2]

            if is_pred:
                order_by = "MIN(s.score) ASC"
            else:
                order_by = "MAX(s.score) DESC"

            cursor.execute(f"""
                SELECT e.id
                FROM {table_sub} s
                JOIN {table_team} e ON s.id_equipe = e.id
                WHERE s.id_competicao = %s
                GROUP BY e.id
                ORDER BY {order_by}
            """, [compid])
            
            ranked_teams = cursor.fetchall()
            total_teams = len(ranked_teams)
            

            if total_teams == 0:
                cursor.execute(f"UPDATE {table_comp} SET flg_premiada = true WHERE id_competicao = %s", [compid])
                continue

            gold_cutoff = 10
            
            silver_count = math.ceil(total_teams * 0.05) 
            bronze_count = math.ceil(total_teams * 0.10)
            
            silver_cutoff = gold_cutoff + silver_count
            bronze_cutoff = silver_cutoff + bronze_count

            for rank_index, row in enumerate(ranked_teams):
                team_id = row[0]
                rank = rank_index + 1
                
                cursor.execute(f"""
                    SELECT id_competidor FROM {table_members}
                    WHERE id_equipe = %s AND id_competicao = %s AND data_hora_fim IS NULL
                """, [team_id, compid])
                members = cursor.fetchall()

                if not members:
                    continue

                medal_type = -1
                medal_name = "Nenhuma"
                
                if rank <= gold_cutoff:
                    medal_type = 0 
                    medal_name = "OURO"
                elif rank <= silver_cutoff:
                    medal_type = 1 
                    medal_name = "PRATA"
                elif rank <= bronze_cutoff:
                    medal_type = 2 
                    medal_name = "BRONZE"

                money_share = 0
                if rank == 1 and is_official and total_money and float(total_money) > 0:
                    money_share = float(total_money) / len(members)

                for member in members:
                    member_id = member[0]
                    
                    if medal_type != -1:
                        cursor.execute(f"""
                            INSERT INTO {table_prizes} (id_competidor, id_competicao, id_org_competicao, data_recebimento, tipo, classificacao, valor)
                            VALUES (%s, %s, %s, CURRENT_DATE, %s, %s, NULL)
                        """, [member_id, compid, id_org, medal_type, rank])

                    if money_share > 0:
                        cursor.execute(f"""
                            INSERT INTO {table_prizes} (id_competidor, id_competicao, id_org_competicao, data_recebimento, tipo, classificacao, valor)
                            VALUES (%s, %s, %s, CURRENT_DATE, 3, %s, %s)
                        """, [member_id, compid, id_org, 1, money_share])

            cursor.execute(f"UPDATE {table_comp} SET flg_premiada = true WHERE id_competicao = %s", [compid])
            messages_log.append(f"Competição {compid}: Processada.")

    return "\n".join(messages_log)