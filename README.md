## Sistema de avaliação de I.A
Disciplina: BANCO DE DADOS I\
Docente: Anderson Paulo Avila Santos\
Discentes: André Tomonaga Schettini | Vitor da Costa Garcia

### Introdução
Algoritmos de inteligência artificial e aprendizado de máquina são amplamente utilizados na resolução de problemas que envolvem grandes quantidades de dados. Nossa ideia é criar um sistema de avaliação onde organizadores podem criar competições problema para os usuários competidores desenvolverem abordagens para resolvê-las enquanto competem entre si em busca da melhor resolução possível.

### Descrição do fluxo do sistema
O usuário do sistema deve ter armazenadas informações como ID usuário, nome, email, senha, data nascimento, idade e , como informações opcionais, endereço com número, rua, bairro, cidade, estado e país.

O sistema conta com duas categorias de usuário: Organizador e Competidor. Os organizadores têm permissão para criar competições e os competidores têm permissão para participar das competições. Um usuário pode estar contido em ambas as categorias, ou seja, um usuário pode ser organizador e participar de outras competições, como pode ser apenas um usuário comum, que tem permissão de ver os rankings etc.

As competições devem ter armazenadas informações como ID competição, título, descrição, tipo da competição, tipo de oficialidade, regras, data de criação, data início, data fim, métrica de desempenho, organizador e dificuldade.

A competição é dividida em dois tipos: Simulação e Predição. A competição simulação, para ser criada, deve ser fornecido um ambiente. Por outro lado, a competição predição, para ser criada, deve ter um dataset rotulado para os competidores, um dataset para submissão sem os rótulos, e os rótulos do dataset de submissão, que será usado para avaliar a eficiência da abordagem do competidor. Ambos os tipos de competição podem ser oficiais ou não oficiais. As competições oficiais devem ter uma premiação em dinheiro, enquanto as não-oficiais, não.

Para participar de competições, os competidores devem criar equipes para determinada competição. Um competidor pode participar de diversas competições ao mesmo tempo. A equipe está associada com a competição, ou seja, ela é identificada pela competição combinada com o seu ID. Toda equipe deve ter um nome.

As equipes podem submeter respostas à competição. Devem ser armazenadas para cada submissão a data e hora do envio, o arquivo submetido e a pontuação obtida (baseado na métrica de desempenho definida pelo organizador).

Os competidores podem receber premiações dependendo de seu desempenho em certa competição. Existem 4 tipos de premiação: Medalhas de ouro, prata, bronze e prêmiação em dinheiro. Todas as competições tem premiações de medalhas, enquanto apenas as competições oficiais tem premiação em dinheiro. As premiações são concedidas na data final da competição para todos os competidores das equipes vencedoras. No caso de competições oficiais, além das medalhas, os competidores podem receber a premiação em dinheiro. Devem ser armazenas para cada premiação o tipo, a data que a premiação foi obtida e a colocação final do competidor.

### Modelo conceitual

<img width="1256" height="782" alt="image" src="https://github.com/user-attachments/assets/ff8db08f-0b4a-49ba-89e2-2369fb8b2d92" />

### Modelo relacional

USUARIO = {PK ID, NOME, EMAIL, SENHA, DATANASCIMENTO, NUMERO, RUA, CIDADE, ESTADO, PAIS}
ORGANIZADOR = {PK FK ID_USUARIO, CPF}
COMPETICAO_PRED = {PK ID_COMPETICAO, FK ID_ORG_COMPETICAO, FLG_OFICIAL, TITULO, DESCRICAO, DIFICULDADE, DATA_CRIACAO, DATA_INICIO, DATA_FIM, METRICA_DESEMPENHO, DATASET_TT, DATASET_SUBMISSAO, DATASET_GABARITO, PREMIACAO, FLG_PREMIADA, FLG_DELETADA}
COMPETICAO_SIMUL = {PK ID_COMPETICAO, PK FK ID_ORG_COMPETICAO, FLG_OFICIAL, TITULO, DESCRICAO, DIFICULDADE, DATA_CRIACAO, DATA_INICIO, DATA_FIM, METRICA_DESEMPENHO, AMBIENTE, PREMIACAO, FLG_PREMIADA, FLG_DELETADA}
COMPETICAO_REGRAS_PRED = {PK FK ID_COMPETICAO, PK N_ORDEM, REGRA}
COMPETICAO_REGRAS_SIMUL = {PK FK ID_COMPETICAO, PK N_ORDEM, REGRA}
EQUIPE_PRED = {PK ID, PK FK ID_COMPETICAO, NOME}
EQUIPE_SIMUL = {PK ID, PK FK ID_COMPETICAO, NOME}
AGGR_COMPO_EQUIPE_PRED = {PK FK ID_EQUIPE, PK FK ID_COMPETICAO, PK FK ID_COMPETIDOR, PK DATA_HORA_INICIO, DATA_HORA_FIM}
AGGR_COMPO_EQUIPE_SIMUL = {PK FK ID_EQUIPE, PK FK ID_COMPETICAO, PK FK ID_COMPETIDOR, PK DATA_HORA_INICIO, DATA_HORA_FIM}
AGGR_PREMIO_COMPETIDOR_PRED = {PK FK ID_COMPETIDOR, PK FK ID_COMPETICAO, PK DATA_RECEBIMENTO, PK TIPO, CLASSIFICACAO, VALOR}
AGGR_PREMIO_COMPETIDOR_SIMUL = {PK FK ID_COMPETIDOR, PK FK ID_COMPETICAO, PK DATA_RECEBIMENTO, PK TIPO, CLASSIFICACAO, VALOR}
AGGR_SUBMISSAO_EQUIPE_PRED = {PK FK ID_EQUIPE, PK FK ID_COMPETICAO, PK DATA_HORA_ENVIO, ARQ_SUBMISSAO, SCORE}
AGGR_SUBMISSAO_EQUIPE_SIMUL = {PK FK ID_EQUIPE, PK FK ID_COMPETICAO, PK DATA_HORA_ENVIO, ARQ_SUBMISSAO, SCORE}

### Modelo lógico

O modelo lógico do projeto está no arquivo ./sistema_avaliacao_ia/main/scripts/main.sql
