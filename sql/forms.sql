-- USUARIO
INSERT INTO usuario (
    nome,
    email,
    senha,
    datanascimento,
    numero,
    cidade,
    estado,
    pais,
) VALUES (
    %s,
    %s,
    %s,
    %s,
    %d,
    %s,
    %s,
    %s,
);

-- USUARIO_TIPO
INSERT INTO usuario_tipo (
    id_usuario,
    tipo
) VALUES (
    %d,
    %d
);

-- ORGANIZADOR
INSERT INTO organizador (
    id_usuario,
    cpf
) VALUES (
    %d,
    %d
);

-- PATROCINADOR
INSERT INTO patrocinador (
    cnpj,
    nome_fantasia,
    endereco,
    telefone
) VALUES (
    %s,
    %s,
    %s,
    %s
);

--------------------------------------
--PREDICÃO
--------------------------------------

-- COMPETIÇÃO PREDIÇÃO
INSERT INTO competicao_pred (
    id_org_competicao,
    flg_oficial,
    dataset_tt,
    dataset_submissao,
    dataset_gabarito,
    cnpj_patrocinador,
    premiacao
) VALUES (
    %d,
    %d,
    %s,
    %s,
    %s,
    %s,
    %f
);

-- REGRAS COMPETIÇÃO PREDICÃO
INSERT INTO competicao_regras_pred (
    id_competicao,
    id_org_competicao,
    n_ordem,
    regra
) VALUES (
    %d,
    %d,
    %d,
    %s
);

-- EQUIPES COMPETIÇÃO PREDIÇÃO
INSERT INTO equipe_pred (
    id_competicao,
    id_org_competicao,
    nome
) VALUES (
    %d,
    %d,
    %s
);

-- PARTICIPANTES EQUIPES DE COMPETIÇÕES PREDIÇÃO
INSERT INTO composicao_equipe_pred(
    id_equipe,
    id_competicao,
    id_org_competicao,
    id_competidor,
    data_hora_inicio,
    data_hora_fim
) VALUES (
    %d,
    %d,
    %d,
    %d,
    %s,
    %s
);

-- PREMIOS COMPETIDORES EM COMPETIÇÕES PREDIÇÃO
INSERT INTO premios_competidor_pred(
    id_competidor,
    id_competicao,
    id_org_competicao,
    data_recebimento,
    tipo,
    classificacao,
    valor
) VALUES (
    %d,
    %d,
    %d,
    %s,
    %d,
    %d,
    %f
);

-- SUBMISSÕES EM COMPETIÇÕES DE PREDIÇÃO DAS EQUIPES
INSERT INTO submissao_equipe_pred (
    id_competicao,
    id_org_competicao,
    id_equipe,
    data_hora_envio,
    arq_submissao,
    score
) VALUES (
    %d,
    %d,
    %d,
    %s,
    %s,
    %f
);

--------------------------------------
-- SIMULAÇÃO
--------------------------------------

-- COMPETIÇÃO SIMULAÇÃO
INSERT INTO competicao_simul (
    id_org_competicao,
    flg_oficial,
    ambiente,
    cnpj_patrocinador,
    premiacao
) VALUES (
    %d,
    %d,
    %s,
    %s,
    %f
);

-- REGRAS COMPETIÇÃO SIMULAÇÃO
INSERT INTO competicao_regras_simul (
    id_competicao,
    id_org_competicao,
    n_ordem,
    regra
) VALUES (
    %d,
    %d,
    %d,
    %s
);

-- EQUIPES COMPETIÇÃO SIMULAÇÃO
INSERT INTO equipe_simul (
    id_competicao,
    id_org_competicao,
    nome
) VALUES (
    %d,
    %d,
    %s
);

-- PARTICIPANTES EQUIPES DE COMPETIÇÕES SIMULAÇÃO
INSERT INTO composicao_equipe_simul(
    id_equipe,
    id_competicao,
    id_org_competicao,
    id_competidor,
    data_hora_inicio,
    data_hora_fim
) VALUES (
    %d,
    %d,
    %d,
    %d,
    %s,
    %s
);

-- PREMIOS COMPETIDORES EM COMPETIÇÕES SIMULAÇÃO
INSERT INTO premios_competidor_simul(
    id_competidor,
    id_competicao,
    id_org_competicao,
    data_recebimento,
    tipo,
    classificacao,
    valor
) VALUES (
    %d,
    %d,
    %d,
    %s,
    %d,
    %d,
    %f
);

-- SUBMISSÕES EM COMPETIÇÕES DE SIMULAÇÃO DAS EQUIPES
INSERT INTO submissao_equipe_simul (
    id_competicao,
    id_org_competicao,
    id_equipe,
    data_hora_envio,
    arq_submissao,
    score
) VALUES (
    %d,
    %d,
    %d,
    %s,
    %s,
    %f
);

