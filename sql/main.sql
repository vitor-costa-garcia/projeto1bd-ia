USUARIO_ESP = {PK FK ID_USUARIO, PK ESPECIALIZACAO}\
-- CREATE DATABASE sistema_comp_ia;

USUARIO = {PK ID, NOME, EMAIL, SENHA, DATANASCIMENTO, NUMERO, RUA, CIDADE, ESTADO, PAIS}
CREATE TABLE usuario(
    id SERIAL NOT NULL,
    nome VARCHAR(20) NOT NULL,
    email VARCHAR(100) NOT NULL,
    senha CHAR(128) NOT NULL,
    datanascimento DATE NOT NULL,
    numero VARCHAR(25),
    rua VARCHAR(50),
    cidade VARCHAR(50),
    estado VARCHAR(50),
    pais VARCHAR(50),
    CONSTRAINT "PK_ID_USUARIO" PRIMARY KEY (id)
);

USUARIO_TIPO = {PK FK ID_USUARIO, PK TIPO}
CREATE TABLE usuario_tipo(
    id_usuario INT NOT NULL,
    tipo INT NOT NULL CHECK(tipo = 0 OR tipo = 1),
    CONSTRAINT "PK_ID_USUARIO_TIPO" PRIMARY KEY (id_usuario, tipo),
    CONSTRAINT "FK_ID_USUARIO_TIPO" FOREIGN KEY (id_usuario) REFERENCES usuario(id)
);

ORGANIZADOR = {PK FK ID_USUARIO, CPF}
CREATE TABLE organizador(
    id_usuario INT NOT NULL,
    cpf VARCHAR(14) NOT NULL,
    CONSTRAINT "PK_ID_USUARIO_ORGANIZADOR" PRIMARY KEY (id_usuario),
    CONSTRAINT "UNIQUE_CPF_ORGANIZADOR" UNIQUE (cpf),
    CONSTRAINT "FK_ID_USUARIO_ORGANIZADOR" FOREIGN KEY (id_usuario) REFERENCES usuario(id)
);

PATROCINADOR = {PK CNPJ, NOME_FANTASIA, ENDERECO, TELEFONE}
CREATE TABLE patrocinador(
    cnpj VARCHAR(18) NOT NULL,
    nome_fantasia VARCHAR(30) NOT NULL,
    endereco VARCHAR(100) NOT NULL,
    telefone VARCHAR(20) NOT NULL,
    CONSTRAINT "PK_PATROCINADOR" PRIMARY KEY (cnpj)
);

COMPETICAO_PRED = {PK ID_COMPETICAO, PK FK ID_ORG_COMPETICAO, FLG_OFICIAL, TITULO, DESCRICAO, DIFICULDADE, DATA_CRIAÇÃO, DATA_INICIO, DATA_FIM, MÉTRICA_DESEMPENHO, DATASET_TT, DATASET_SUBMISSAO, DATASET_GABARITO, FK CNPJ_PATROCINADOR, PREMIACAO}
CREATE TABLE competicao_pred(
    id_competicao SERIAL NOT NULL,
    id_org_competicao INT NOT NULL,
    flg_oficial INT NOT NULL CHECK(flg_oficial BETWEEN 0 AND 1),
    dataset_tt VARCHAR(200) NOT NULL,
    dataset_submissao VARCHAR(200) NOT NULL,
    dataset_gabarito VARCHAR(200) NOT NULL,
    cnpj_patrocinador VARCHAR(18) CHECK((flg_oficial = 1 AND cnpj_patrocinador IS NOT NULL) OR (flg_oficial = 0 AND cnpj_patrocinador IS NULL)),
    premiacao MONEY CHECK((flg_oficial = 1 AND cnpj_patrocinador IS NOT NULL) OR (flg_oficial = 0 AND cnpj_patrocinador IS NULL)),
    CONSTRAINT "PK_COMPETICAO_PRED" PRIMARY KEY (id_competicao, id_org_competicao),
    CONSTRAINT "FK_ID_PATROCINADOR_COMP_PRED" FOREIGN KEY (cnpj_patrocinador) REFERENCES patrocinador(cnpj)
);

COMPETICAO_REGRAS_PRED = {PK FK ID_COMPETICAO, PK FK ID_ORG_COMPETICAO, PK N_ORDEM, REGRA}
CREATE TABLE competicao_regras_pred(
    id_competicao INT NOT NULL,
    id_org_competicao INT NOT NULL,
    n_ordem INT NOT NULL,
    regra VARCHAR(200) NOT NULL,
    CONSTRAINT "PK_REGRAS_COMPETICAO_PRED" PRIMARY KEY (id_competicao, id_org_competicao, n_ordem),
    CONSTRAINT "FK_REGRAS_COMPETICAO_PRED" FOREIGN KEY (id_competicao, id_org_competicao) REFERENCES competicao_pred(id_competicao,  id_org_competicao)
);

EQUIPE_PRED = {PK ID, PK FK ID_COMPETICAO, PK FK ID_ORG_COMPETICAO, NOME}\
CREATE TABLE equipe_pred(
    id SERIAL NOT NULL,
    id_competicao INT NOT NULL,
    id_org_competicao INT NOT NULL,
    nome VARCHAR(20) NOT NULL,
    CONSTRAINT "PK_EQUIPE_COMP_PRED" PRIMARY KEY (id, id_competicao, id_org_competicao),
    CONSTRAINT "FK_EQUIPE_COMP_PRED" FOREIGN KEY (id_competicao, id_org_competicao) REFERENCES competicao_pred(id_competicao, id_org_competicao)
);

AGGR_COMPOE_EQUIPE_PRED = {PK FK ID_EQUIPE, PK FK ID_COMPETICAO, PK FK ID_ORG_COMPETICAO, PK FK ID_COMPETIDOR, PK DATA_HORA_INICIO, DATA_HORA_FIM}\
CREATE TABLE composicao_equipe_pred(
    id_equipe INT NOT NULL,
    id_competicao INT NOT NULL,
    id_org_competicao INT NOT NULL,
    id_competidor INT NOT NULL,
    data_hora_inicio TIMESTAMP NOT NULL,
    data_hora_fim TIMESTAMP,
    CONSTRAINT "PK_PARTICIPACAO_EQUIPE_COMP_PRED" PRIMARY KEY (id_equipe, id_competicao, id_org_competicao, id_competidor, data_hora_inicio),
    CONSTRAINT "FK_PART_EQUIPE_COMPETICAO_PRED" FOREIGN KEY (id_equipe, id_competicao, id_org_competicao) REFERENCES equipe_pred(id, id_competicao, id_org_competicao),
    CONSTRAINT "FK_PART_EQUIPE_COMPETIDOR_COMP_PRED" FOREIGN KEY (id_competidor) REFERENCES usuario(id) 
);

AGGR_PREMIO_COMPETIDOR_PRED = {PK FK ID_COMPETIDO, PK FK ID_COMPETICAO, PK FK ID_ORG_COMPETICAO, PK DATA_RECEBIMENTO, PK TIPO, CLASSIFICACAO, VALOR}
CREATE TABLE premios_competidor_pred(
    id_competidor INT NOT NULL,
    id_competicao INT NOT NULL,
    id_org_competicao INT NOT NULL,
    data_recebimento DATE NOT NULL,
    tipo INT NOT NULL CHECK(tipo BETWEEN 0 AND 3),
    classificacao INT NOT NULL,
    valor MONEY,
    CONSTRAINT "PK_PREMIOS_COMP_PRED" PRIMARY KEY (id_competidor, id_competicao, id_org_competicao, data_recebimento, tipo),
    CONSTRAINT "FK_COMPETICAO_PRED_PREMIO" FOREIGN KEY (id_competicao, id_org_competicao) REFERENCES competicao_pred(id_competicao, id_org_competicao),
    CONSTRAINT "FK_COMPETIDOR_COMP_PRED" FOREIGN KEY (id_competidor) REFERENCES usuario(id)
);

AGGR_SUBMISSAO_EQUIPE_PRED = {PK FK ID_COMPETICAO, PK FK ID_ORG_COMPETICAO, PK FK ID_EQUIPE, PK DATA_HORA_ENVIO, ARQ_SUBMISSAO, SCORE}
CREATE TABLE submissao_equipe_pred(
    id_competicao INT NOT NULL,
    id_org_competicao INT NOT NULL,
    id_equipe INT NOT NULL,
    data_hora_envio TIMESTAMP NOT NULL,
    arq_submissao VARCHAR(200) NOT NULL,
    score REAL NOT NULL,
    CONSTRAINT "PK_SUBMISSAO_EQUIPE_PRED" PRIMARY KEY (id_competicao, id_org_competicao, id_equipe, data_hora_envio),
    CONSTRAINT "FK_SUBMISSAO_EQUIPE_PRED" FOREIGN KEY (id_competicao, id_org_competicao, id_equipe) REFERENCES equipe_pred(id_competicao, id_org_competicao, id)
)

COMPETICAO_SIMUL = {PK ID_COMPETICAO, PK FK ID_ORG_COMPETICAO, FLG_OFICIAL, TITULO, DESCRICAO, DIFICULDADE, DATA_CRIAÇÃO, DATA_INICIO, DATA_FIM, MÉTRICA_DESEMPENHO, AMBIENTE, FK CNPJ_PATROCINADOR, PREMIACAO}
CREATE TABLE competicao_simul(
    id_competicao SERIAL NOT NULL,
    id_org_competicao INT NOT NULL,
    flg_oficial INT NOT NULL CHECK(flg_oficial BETWEEN 0 AND 1),
    ambiente VARCHAR(200) NOT NULL, --Caminho arquivo
    cnpj_patrocinador VARCHAR(18) CHECK((flg_oficial = 1 AND cnpj_patrocinador IS NOT NULL) OR (flg_oficial = 0 AND cnpj_patrocinador IS NULL)),
    premiacao MONEY CHECK((flg_oficial = 1 AND cnpj_patrocinador IS NOT NULL) OR (flg_oficial = 0 AND cnpj_patrocinador IS NULL)),
    CONSTRAINT "PK_COMPETICAO_SIMUL_OFC" PRIMARY KEY (id_competicao, id_org_competicao),
    CONSTRAINT "FK_ID_PATROCINADOR_COMP_SIMUL" FOREIGN KEY (cnpj_patrocinador) REFERENCES patrocinador(cnpj)
);

COMPETICAO_REGRAS_SIMUL = {PK FK ID_COMPETICAO, PK FK ID_ORG_COMPETICAO, PK N_ORDEM, REGRA}\
CREATE TABLE competicao_regras_simul(
    id_competicao INT NOT NULL,
    id_org_competicao INT NOT NULL,
    n_ordem INT NOT NULL,
    regra VARCHAR(200) NOT NULL,
    CONSTRAINT "PK_REGRAS_COMPETICAO_SIMUL" PRIMARY KEY (id_competicao, id_org_competicao, n_ordem),
    CONSTRAINT "FK_COMPETICAO_SIMUL" FOREIGN KEY (id_competicao, id_org_competicao) REFERENCES competicao_simul(id_competicao, id_org_competicao)
);

EQUIPE_SIMUL = {PK ID, PK FK ID_COMPETICAO, PK FK ID_ORG_COMPETICAO, NOME}
CREATE TABLE equipe_simul(
    id SERIAL NOT NULL,
    id_competicao INT NOT NULL,
    id_org_competicao INT NOT NULL,
    nome VARCHAR(20) NOT NULL,
    CONSTRAINT "PK_EQUIPE_COMP_SIMUL" PRIMARY KEY (id, id_competicao, id_org_competicao),
    CONSTRAINT "FK_EQUIPE_COMP_SIMUL" FOREIGN KEY (id_competicao, id_org_competicao) REFERENCES competicao_simul(id_competicao, id_org_competicao)
);

AGGR_COMPOE_EQUIPE_SIMUL = {PK FK ID_EQUIPE, PK FK ID_COMPETICAO, PK FK ID_ORG_COMPETICAO, PK FK ID_COMPETIDOR, PK DATA_HORA_INICIO, DATA_HORA_FIM}\
CREATE TABLE composicao_equipe_simul(
    id_equipe INT NOT NULL,
    id_competicao INT NOT NULL,
    id_org_competicao INT NOT NULL,
    id_competidor INT NOT NULL,
    data_hora_inicio TIMESTAMP NOT NULL,
    data_hora_fim TIMESTAMP,
    CONSTRAINT "PK_PARTICIPACAO_EQUIPE_COMP_SIMUL" PRIMARY KEY (id_equipe, id_competicao, id_org_competicao, id_competidor, data_hora_inicio),
    CONSTRAINT "FK_PART_EQUIPE_COMPETICAO_SIMUL" FOREIGN KEY (id_equipe, id_competicao, id_org_competicao) REFERENCES equipe_simul(id, id_competicao, id_org_competicao),
    CONSTRAINT "FK_PART_EQUIPE_COMPETIDOR_COMP_SIMUL" FOREIGN KEY (id_competidor) REFERENCES usuario(id) 
);

AGGR_PREMIO_COMPETIDOR_SIMUL = {PK FK ID_COMPETIDOR,PK FK ID_COMPETICAO, PK FK ID_ORG_COMPETICAO, PK DATA_RECEBIMENTO, PK TIPO, CLASSIFICACAO, VALOR}
CREATE TABLE premios_competidor_simul(
    id_competidor INT NOT NULL,
    id_competicao INT NOT NULL,
    id_org_competicao INT NOT NULL,
    data_recebimento DATE NOT NULL,
    tipo INT NOT NULL CHECK(tipo BETWEEN 0 AND 3),
    classificacao INT NOT NULL,
    valor MONEY,
    CONSTRAINT "PK_PREMIOS_COMP_SIMUL" PRIMARY KEY (id_competidor, id_competicao, id_org_competicao, data_recebimento, tipo),
    CONSTRAINT "FK_COMPETICAO_SIMUL_PREMIO" FOREIGN KEY (id_competicao, id_org_competicao) REFERENCES competicao_simul(id_competicao, id_org_competicao),
    CONSTRAINT "FK_COMPETIDOR_COMP_SIMUL" FOREIGN KEY (id_competidor) REFERENCES usuario(id)
);

AGGR_SUBMISSAO_EQUIPE_SIMUL = {PK FK ID_COMPETICAO, PK FK ID_ORG_COMPETICAO, PK FK ID_EQUIPE, PK DATA_HORA_ENVIO, ARQ_SUBMISSAO, SCORE}
CREATE TABLE submissao_equipe_simul(
    id_competicao INT NOT NULL,
    id_org_competicao INT NOT NULL,
    id_equipe INT NOT NULL,
    data_hora_envio TIMESTAMP NOT NULL,
    arq_submissao VARCHAR(200) NOT NULL,
    score REAL NOT NULL,
    CONSTRAINT "PK_SUBMISSAO_EQUIPE_COMP_SIMUL" PRIMARY KEY (id_competicao, id_org_competicao, id_equipe, data_hora_envio),
    CONSTRAINT "FK_SUBMISSAO_EQUIPE_COMP_SIMUL" FOREIGN KEY (id_competicao, id_org_competicao, id_equipe) REFERENCES equipe_simul(id_competicao, id_org_competicao, id)
)
