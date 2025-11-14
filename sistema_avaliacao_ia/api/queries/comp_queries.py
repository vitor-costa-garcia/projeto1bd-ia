from django.db import IntegrityError, connection
from django.http import JsonResponse, FileResponse
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import FileSystemStorage
from datetime import date
import os

def get_all_competitions(request):
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
                        A.dificuldade,
                        A.premiacao 
                    FROM
                        competicao_pred A, usuario B
                    WHERE
                        A.id_org_competicao = B.id

                    UNION

                    SELECT 
                        A.id_competicao,
                        A.titulo,
                        'Simulação' as tipo,
                        B.nome as nome_organizador,
                        A.data_inicio,
                        A.data_fim,
                        A.flg_oficial,
                        A.dificuldade,
                        A.premiacao 
                    FROM
                        competicao_simul A, usuario B
                    WHERE
                        A.id_org_competicao = B.id
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
                     premiacao,  -- CNPJ removido
                     dataset_tt, dataset_submissao, dataset_gabarito) 
                    VALUES (%s01, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    RETURNING id_competicao
                    """,
                    [
                        nextid, id_org, flg_oficial, data.get('titulo'), data.get('descricao'), data.get('dificuldade'),
                        data.get('data_inicio'), data.get('data_fim'), metrica,
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

            elif tipo_comp == '1':
                metrica = data.get('metrica_simulacao')

                nextid = get_nextseq_comp(type=1, add=False)
                
                cursor.execute(
                    """
                    INSERT INTO competicao_simul
                    (id_competicao, id_org_competicao, flg_oficial, titulo, descricao, dificuldade, 
                     data_inicio, data_fim, metrica_desempenho, 
                     premiacao, ambiente) -- CNPJ removido
                    VALUES (%s02, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    RETURNING id_competicao
                    """,
                    [
                        nextid, id_org, flg_oficial, data.get('titulo'), data.get('descricao'), data.get('dificuldade'),
                        data.get('data_inicio'), data.get('data_fim'), metrica,
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
                        id_competicao = %s AND
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

        # Equipes
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

        # Competidores ativos na competição
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
        raise JsonResponse({"error": "error downloading the file"}, status=500)
    
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