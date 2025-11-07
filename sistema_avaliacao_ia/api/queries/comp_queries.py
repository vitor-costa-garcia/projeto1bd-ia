from django.db import connection
from django.http import JsonResponse
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import FileSystemStorage

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
                        A.dificuldade
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
                        A.dificuldade
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

@csrf_exempt
def post_competition(request):
    if request.method != "POST":
        return JsonResponse({"error":"POST only endpoint"}, status=405)
    
    titulo = request.POST.get('titulo')
    descricao = request.POST.get('descricao')
    tipo = request.POST.get('tipo')
    dificuldade = request.POST.get('dificuldade')
    oficial = request.POST.get('oficial')
    metrica_desempenho = request.POST.get('metrica-desempenho')

    patrocinador = None
    premiacao = None
    dataset_tt = None
    dataset_submissao = None
    dataset_gabarito = None
    ambiente = None

    if oficial == 1:
        patrocinador = request.POST.get('patrocinador')
        premiacao = request.POST.get('premiacao')

    print(request.POST)
    print(request.FILES)

    if tipo == 0:
        dataset_tt = request.FILES['dataset-tt']
        dataset_submissao = request.FILES['dataset-submissao']
        dataset_gabarito = request.FILES['dataset-gabarito']

        if dataset_tt and dataset_submissao and dataset_gabarito:
            # É NECESSARIO CRIAR LOGICA PARA PADRONIZAR O NOME DOS DATASETS
            # QUE SÃO RECEBIDOS AO CRIAR A COMPETIÇÃO PARA CONSEGUIR FAZER
            # A BUSCA DOS DATASETS DE DETERMINADA COMPETIÇÃO
            print("IM HERE")
            fs = FileSystemStorage(location="./uploads/datasets")
            fs.save(dataset_tt.name, dataset_tt)
            fs.save(dataset_submissao.name, dataset_submissao)
            fs.save(dataset_gabarito.name, dataset_gabarito)
    else:
        ambiente = request.FILES.get('ambiente')
        if ambiente:
            # MESMO PROBLEMA DE PADRONIZACAO DE NOME COM O AMBIENTE
            # DE DETERMINADA COMPETIÇÃO. NECESSARIO CRIAR LOGICA
            # DE NOME PARA FACILITAR BUSCA
            fs = FileSystemStorage(location="./uploads/ambientes")
            fs.save(ambiente.name, ambiente)


    print(dataset_tt)

    return redirect("/comp")
