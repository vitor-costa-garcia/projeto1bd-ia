from django.db import models


# # Usuarios

# class Usuario(models.Model):
#     id = models.IntegerField(primary_key=True)
#     nome = models.CharField(max_length=20)
#     email = models.CharField(max_length=100)
#     senha = models.CharField(max_length=128)
#     datanascimento = models.DateField()
#     numero = models.IntegerField(null=False)
#     rua = models.CharField(max_length=50, null=False)
#     cidade = models.CharField(max_length=50, null=False)
#     estado = models.CharField(max_length=50, null=False)
#     pais = models.CharField(max_length=50, null=False)

# class UsuarioTipo(models.Model):
#     usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, primary_key=True)
#     tipo = models.IntegerField(primary_key=True)

# class Organizador(models.Model):
#     usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, primary_key=True)
#     cpf = models.CharField(max_length=14, unique=True)

# class Patrocinador(models.Model):
#     cnpj = models.CharField(max_length=18, primary_key=True)
#     nome_fantasia = models.CharField(max_length=30)
#     endereco = models.CharField(max_length=100)
#     telefone = models.CharField(max_length=14)

# #Competição predição

# class CompeticaoPred(models.Model):
#     id = models.IntegerField(primary_key=True)
#     id_organizador = models.ForeignKey(Organizador, primary_key=True, on_delete=models.CASCADE)
#     flg_oficial = models.BooleanField()
#     dataset_tt = models.CharField(max_length=200)
#     dataset_submissao = models.CharField(max_length=200)
#     dataset_gabarito = models.CharField(max_length=200)
#     cnpj_patrocinador = models.ForeignKey(Patrocinador, on_delete=models.CASCADE)
#     premiacao = models.FloatField(null=True)

# class CompeticaoPredRegras(models.Model):
#     id_competicao = models.ForeignKey(CompeticaoPred, primary_key=True, on_delete=models.CASCADE)
#     id_org_competicao = models.ForeignKey(Organizador, primary_key=True, on_delete=models.CASCADE)
#     n_ordem = models.IntegerField()
#     regra = models.CharField(max_length=200)

# class EquipeCompeticaoPred(models.Model):
#     id = models.IntegerField(primary_key=True)
#     id_competicao = models.ForeignKey(CompeticaoPred, primary_key=True, on_delete=models.CASCADE)
#     id_org_competicao = models.ForeignKey(Organizador, primary_key=True, on_delete=models.CASCADE)
#     nome = models.CharField(max_length=20)

# class ComposicaoEquipeCompeticaoPred(models.Model):
#     id_equipe = models.ForeignKey(EquipeCompeticaoPred, primary_key=True, on_delete=models.CASCADE)
#     id_competicao = models.ForeignKey(CompeticaoPred, primary_key=True, on_delete=models.CASCADE)
#     id_org_competicao = models.ForeignKey(Organizador, primary_key=True, on_delete=models.CASCADE)
#     id_competidor = models.ForeignKey(Usuario, primary_key=True, on_delete=models.CASCADE)
#     data_hora_inicio = models.DateTimeField(primary_key=True)
#     data_hora_fim = models.DateTimeField(null=True)

# class PremiosCompetidorPred(models.Model):
#     id_competidor = models.ForeignKey(Usuario, primary_key=True, on_delete=models.CASCADE)
#     id_competicao = models.ForeignKey(CompeticaoPred, primary_key=True, on_delete=models.CASCADE)
#     id_org_competicao = models.ForeignKey(Organizador, primary_key=True, on_delete=models.CASCADE)
#     data_recebimento = models.DateField(primary_key=True)
#     tipo = models.IntegerField(primary_key=True)
#     classificacao = models.IntegerField()
#     valor = models.FloatField(null=True)

# class SubmissaoEquipeCompeticaoPred(models.Model):
#     id_competicao = models.ForeignKey(CompeticaoPred, primary_key=True, on_delete=models.CASCADE)
#     id_org_competicao = models.ForeignKey(Organizador, primary_key=True, on_delete=models.CASCADE)
#     id_equipe = models.ForeignKey(EquipeCompeticaoPred, primary_key=True, on_delete=models.CASCADE)
#     data_hora_envio = models.DateTimeField(primary_key=True)
#     arq_submissao = models.CharField(max_length=200)
#     score = models.FloatField()

# # Competição simulação

# class CompeticaoSimul(models.Model):
#     id = models.IntegerField(primary_key=True)
#     id_organizador = models.ForeignKey(Organizador, primary_key=True, on_delete=models.CASCADE)
#     flg_oficial = models.BooleanField()
#     dataset_tt = models.CharField(max_length=200)
#     dataset_submissao = models.CharField(max_length=200)
#     dataset_gabarito = models.CharField(max_length=200)
#     cnpj_patrocinador = models.ForeignKey(Patrocinador, on_delete=models.CASCADE)
#     premiacao = models.FloatField(null=True)

# class CompeticaoSimulRegras(models.Model):
#     id_competicao = models.ForeignKey(CompeticaoSimul, primary_key=True, on_delete=models.CASCADE)
#     id_org_competicao = models.ForeignKey(Organizador, primary_key=True, on_delete=models.CASCADE)
#     n_ordem = models.IntegerField()
#     regra = models.CharField(max_length=200)

# class EquipeCompeticaoSimul(models.Model):
#     id = models.IntegerField(primary_key=True)
#     id_competicao = models.ForeignKey(CompeticaoSimul, primary_key=True, on_delete=models.CASCADE)
#     id_org_competicao = models.ForeignKey(Organizador, primary_key=True, on_delete=models.CASCADE)
#     nome = models.CharField(max_length=20)

# class ComposicaoEquipeCompeticaoSimul(models.Model):
#     id_equipe = models.ForeignKey(EquipeCompeticaoSimul, primary_key=True, on_delete=models.CASCADE)
#     id_competicao = models.ForeignKey(CompeticaoSimul, primary_key=True, on_delete=models.CASCADE)
#     id_org_competicao = models.ForeignKey(Organizador, primary_key=True, on_delete=models.CASCADE)
#     id_competidor = models.ForeignKey(Usuario, primary_key=True, on_delete=models.CASCADE)
#     data_hora_inicio = models.DateTimeField(primary_key=True)
#     data_hora_fim = models.DateTimeField(null=True)

# class PremiosCompetidorSimul(models.Model):
#     id_competidor = models.ForeignKey(Usuario, primary_key=True, on_delete=models.CASCADE)
#     id_competicao = models.ForeignKey(CompeticaoSimul, primary_key=True, on_delete=models.CASCADE)
#     id_org_competicao = models.ForeignKey(Organizador, primary_key=True, on_delete=models.CASCADE)
#     data_recebimento = models.DateField(primary_key=True)
#     tipo = models.IntegerField(primary_key=True)
#     classificacao = models.IntegerField()
#     valor = models.FloatField(null=True)

# class SubmissaoEquipeCompeticaoSimul(models.Model):
#     id_competicao = models.ForeignKey(CompeticaoSimul, primary_key=True, on_delete=models.CASCADE)
#     id_org_competicao = models.ForeignKey(Organizador, primary_key=True, on_delete=models.CASCADE)
#     id_equipe = models.ForeignKey(EquipeCompeticaoSimul, primary_key=True, on_delete=models.CASCADE)
#     data_hora_envio = models.DateTimeField(primary_key=True)
#     arq_submissao = models.CharField(max_length=200)
#     score = models.FloatField()
