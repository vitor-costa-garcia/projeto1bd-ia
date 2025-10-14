-- Populate usuario
INSERT INTO usuario (id, nome, email, senha, datanascimento, numero, rua, cidade, estado, pais) VALUES
(1, 'Alice', 'alice@mail.com', 'x'*128, '1998-04-12', 12, 'Rua das Flores', 'São Paulo', 'SP', 'Brasil'),
(2, 'Bruno', 'bruno@mail.com', 'y'*128, '1995-06-22', 45, 'Av. Paulista', 'São Paulo', 'SP', 'Brasil'),
(3, 'Carla', 'carla@mail.com', 'z'*128, '2000-09-03', 78, 'Rua das Laranjeiras', 'Rio de Janeiro', 'RJ', 'Brasil'),
(4, 'Diego', 'diego@mail.com', 'a'*128, '1997-01-25', 99, 'Rua do Sol', 'Curitiba', 'PR', 'Brasil'),
(5, 'Elena', 'elena@mail.com', 'b'*128, '2001-07-30', 101, 'Rua Central', 'Florianópolis', 'SC', 'Brasil');

-- Tipo de usuário
-- tipo: 0 = competidor, 1 = organizador, 3 = ambos
INSERT INTO usuario_tipo (id_usuario, tipo) VALUES
(1, 0),
(2, 1),
(3, 0),
(4, 0),
(5, 3);

-- Organizador (usuário 2 e 5)
INSERT INTO organizador (id_usuario, cpf) VALUES
(2, '123.456.789-10'),
(5, '234.567.890-11');

-- Patrocinador
INSERT INTO patrocinador (cnpj, nome_fantasia, endereco, telefone) VALUES
('12.345.678/0001-99', 'TechCorp', 'Av. das Inovações, 123', '(11) 99999-8888'),
('98.765.432/0001-11', 'DataBoost', 'Rua dos Dados, 456', '(21) 98888-7777');

-- Competição de predição
INSERT INTO competicao_pred (
    id_competicao, id_org_competicao, flg_oficial,
    dataset_tt, dataset_submissao, dataset_gabarito,
    cnpj_patrocinador, premiacao
) VALUES
(1, 2, 1,
 '/datasets/vendas/train.csv',
 '/datasets/vendas/test.csv',
 '/datasets/vendas/gabarito.csv',
 '12.345.678/0001-99',
 5000.00);

-- Regras da competição de predição
INSERT INTO competicao_regras_pred (id_competicao, id_org_competicao, n_ordem, regra) VALUES
(1, 2, 1, 'Submissão em formato CSV'),
(1, 2, 2, 'Métrica de avaliação: RMSE'),
(1, 2, 3, 'Máximo de 3 submissões por dia');

-- Equipes da competição de predição
INSERT INTO equipe_pred (id, id_competicao, id_org_competicao, nome) VALUES
(1, 1, 2, 'DataWizards'),
(2, 1, 2, 'ModelMasters');

-- Composição de equipes (usuários competidores)
INSERT INTO composicao_equipe_pred (
    id_equipe, id_competicao, id_org_competicao, id_competidor, data_hora_inicio, data_hora_fim
) VALUES
(1, 1, 2, 1, '2025-04-01 10:00:00', NULL),
(1, 1, 2, 3, '2025-04-01 10:05:00', NULL),
(2, 1, 2, 4, '2025-04-01 10:10:00', NULL);

-- Prêmios da competição de predição
INSERT INTO premios_competidor_pred (
    id_competidor, id_competicao, id_org_competicao,
    data_recebimento, tipo, classificacao, valor
) VALUES
(1, 1, 2, '2025-05-02', 1, 1, 3000.00),
(3, 1, 2, '2025-05-02', 2, 2, 1500.00);

-- Competição de simulação
INSERT INTO competicao_simul (
    id_competicao, id_org_competicao, flg_oficial,
    ambiente, cnpj_patrocinador, premiacao
) VALUES
(2, 5, 1,
 '/ambientes/robos/arena_v1.zip',
 '98.765.432/0001-11',
 7000.00);

-- Regras da simulação
INSERT INTO competicao_regras_simul (id_competicao, id_org_competicao, n_ordem, regra) VALUES
(2, 5, 1, 'Ambiente simulado deve ser executado em modo seguro'),
(2, 5, 2, 'Limite de tempo: 10 minutos por episódio');

-- Equipes da simulação
INSERT INTO equipe_simul (id, id_competicao, id_org_competicao, nome) VALUES
(1, 2, 5, 'RoboRacers'),
(2, 2, 5, 'AI Dynamics');

-- Composição de equipes da simulação
INSERT INTO composicao_equipe_simul (
    id_equipe, id_competicao, id_org_competicao, id_competidor, data_hora_inicio, data_hora_fim
) VALUES
(1, 2, 5, 1, '2025-06-01 09:00:00', NULL),
(1, 2, 5, 3, '2025-06-01 09:10:00', NULL),
(2, 2, 5, 4, '2025-06-01 09:20:00', NULL),
(2, 2, 5, 5, '2025-06-01 09:30:00', NULL);

-- Prêmios da simulação
INSERT INTO premios_competidor_simul (
    id_competidor, id_competicao, id_org_competicao, data_recebimento, tipo, classificacao, valor
) VALUES
(5, 2, 5, '2025-07-02', 1, 1, 4000.00),
(4, 2, 5, '2025-07-02', 2, 2, 2000.00);

INSERT INTO submissao_equipe_pred (
    id_competicao, id_org_competicao, id_equipe, data_hora_envio, arq_submissao, score
) VALUES
(1, 2, 1, '2025-04-10 10:00:00', '/submissions/pred/datawizards/sub1.csv', 85.5),
(1, 2, 1, '2025-04-12 14:30:00', '/submissions/pred/datawizards/sub2.csv', 88.2),
(1, 2, 2, '2025-04-11 09:15:00', '/submissions/pred/modelmasters/sub1.csv', 79.3),
(1, 2, 2, '2025-04-13 16:45:00', '/submissions/pred/modelmasters/sub2.csv', 82.7);

INSERT INTO submissao_equipe_simul (
    id_competicao, id_org_competicao, id_equipe, data_hora_envio, arq_submissao, score
) VALUES
(2, 5, 1, '2025-06-05 09:00:00', '/submissions/simul/roboracers/run1.zip', 92.5),
(2, 5, 1, '2025-06-06 11:30:00', '/submissions/simul/roboracers/run2.zip', 95.0),
(2, 5, 2, '2025-06-05 10:15:00', '/submissions/simul/aidynamics/run1.zip', 87.3),
(2, 5, 2, '2025-06-06 13:45:00', '/submissions/simul/aidynamics/run2.zip', 90.1);