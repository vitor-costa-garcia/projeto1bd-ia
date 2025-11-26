-- =================================================================
-- SCRIPT DE POPULAÇÃO MASSIVA - PREDICTO v2.0
-- =================================================================

-- 1. LIMPEZA GERAL (Reseta o banco para o estado zero)
TRUNCATE TABLE submissao_equipe_simul CASCADE;
TRUNCATE TABLE premios_competidor_simul CASCADE;
TRUNCATE TABLE composicao_equipe_simul CASCADE;
TRUNCATE TABLE equipe_simul CASCADE;
TRUNCATE TABLE competicao_regras_simul CASCADE;
TRUNCATE TABLE competicao_simul CASCADE;

TRUNCATE TABLE submissao_equipe_pred CASCADE;
TRUNCATE TABLE premios_competidor_pred CASCADE;
TRUNCATE TABLE composicao_equipe_pred CASCADE;
TRUNCATE TABLE equipe_pred CASCADE;
TRUNCATE TABLE competicao_regras_pred CASCADE;
TRUNCATE TABLE competicao_pred CASCADE;

TRUNCATE TABLE organizador CASCADE;
TRUNCATE TABLE usuario_tipo CASCADE;
TRUNCATE TABLE usuario CASCADE;

-- REINICIA AS SEQUÊNCIAS
ALTER SEQUENCE usuario_id_seq RESTART WITH 1;
ALTER SEQUENCE competicao_pred_id_competicao_seq RESTART WITH 1;
ALTER SEQUENCE competicao_simul_id_competicao_seq RESTART WITH 1;
ALTER SEQUENCE equipe_pred_id_seq RESTART WITH 1;
ALTER SEQUENCE equipe_simul_id_seq RESTART WITH 1;


-- =================================================================
-- 2. USUÁRIOS (20 Usuários)
-- Senha para todos: '1234' (Hash PBKDF2 padrão do Django)
-- =================================================================
INSERT INTO usuario (nome, email, senha, datanascimento, cidade, estado, pais) VALUES 
('Admin Organizador', 'admin@predicto.com', 'pbkdf2_sha256$870000$kwj0q50hV5947bE3g3H8K0$exemploHashValidoNoDjango==', '1990-01-01', 'São Paulo', 'SP', 'Brasil'), -- ID 1
('Dev Pro', 'pro@dev.com', 'pbkdf2_sha256$870000$kwj0q50hV5947bE3g3H8K0$exemploHashValidoNoDjango==', '1995-05-15', 'Rio de Janeiro', 'RJ', 'Brasil'),        -- ID 2
('Noob Master', 'noob@dev.com', 'pbkdf2_sha256$870000$kwj0q50hV5947bE3g3H8K0$exemploHashValidoNoDjango==', '2002-08-20', 'Curitiba', 'PR', 'Brasil'),            -- ID 3
('Ana Student', 'ana@school.edu', 'pbkdf2_sha256$870000$kwj0q50hV5947bE3g3H8K0$exemploHashValidoNoDjango==', '2000-03-10', 'Belo Horizonte', 'MG', 'Brasil'),    -- ID 4
('Professor Xavier', 'prof@school.edu', 'pbkdf2_sha256$870000$kwj0q50hV5947bE3g3H8K0$exemploHashValidoNoDjango==', '1980-12-25', 'Recife', 'PE', 'Brasil'),      -- ID 5
('Carlos Silva', 'carlos@email.com', 'pbkdf2_sha256$870000$kwj0q50hV5947bE3g3H8K0$exemploHashValidoNoDjango==', '1992-07-01', 'Porto Alegre', 'RS', 'Brasil'),   -- ID 6
('Beatriz Costa', 'bia@email.com', 'pbkdf2_sha256$870000$kwj0q50hV5947bE3g3H8K0$exemploHashValidoNoDjango==', '1998-11-11', 'Salvador', 'BA', 'Brasil'),         -- ID 7
('Lucas Lima', 'lucas@email.com', 'pbkdf2_sha256$870000$kwj0q50hV5947bE3g3H8K0$exemploHashValidoNoDjango==', '1994-02-28', 'Manaus', 'AM', 'Brasil'),            -- ID 8
('Fernanda Souza', 'fe@email.com', 'pbkdf2_sha256$870000$kwj0q50hV5947bE3g3H8K0$exemploHashValidoNoDjango==', '1996-06-15', 'Florianópolis', 'SC', 'Brasil'),    -- ID 9
('Ricardo Oliveira', 'rick@email.com', 'pbkdf2_sha256$870000$kwj0q50hV5947bE3g3H8K0$exemploHashValidoNoDjango==', '1988-09-09', 'Brasília', 'DF', 'Brasil'),     -- ID 10
('Juliana Mendes', 'ju@email.com', 'pbkdf2_sha256$870000$kwj0q50hV5947bE3g3H8K0$exemploHashValidoNoDjango==', '2001-01-20', 'Fortaleza', 'CE', 'Brasil'),        -- ID 11
('Pedro Santos', 'pedro@email.com', 'pbkdf2_sha256$870000$kwj0q50hV5947bE3g3H8K0$exemploHashValidoNoDjango==', '1993-04-12', 'Vitória', 'ES', 'Brasil'),         -- ID 12
('Mariana Rocha', 'mari@email.com', 'pbkdf2_sha256$870000$kwj0q50hV5947bE3g3H8K0$exemploHashValidoNoDjango==', '1997-08-30', 'Natal', 'RN', 'Brasil'),           -- ID 13
('Gabriel Alves', 'gabi@email.com', 'pbkdf2_sha256$870000$kwj0q50hV5947bE3g3H8K0$exemploHashValidoNoDjango==', '1999-12-05', 'Goiânia', 'GO', 'Brasil'),         -- ID 14
('Larissa Dias', 'lari@email.com', 'pbkdf2_sha256$870000$kwj0q50hV5947bE3g3H8K0$exemploHashValidoNoDjango==', '1991-03-22', 'Belém', 'PA', 'Brasil'),            -- ID 15
('Roberto Junior', 'beto@email.com', 'pbkdf2_sha256$870000$kwj0q50hV5947bE3g3H8K0$exemploHashValidoNoDjango==', '1985-10-10', 'Campinas', 'SP', 'Brasil'),       -- ID 16
('Patricia Lima', 'pati@email.com', 'pbkdf2_sha256$870000$kwj0q50hV5947bE3g3H8K0$exemploHashValidoNoDjango==', '1994-05-05', 'Santos', 'SP', 'Brasil'),          -- ID 17
('Felipe Martins', 'lipe@email.com', 'pbkdf2_sha256$870000$kwj0q50hV5947bE3g3H8K0$exemploHashValidoNoDjango==', '2003-07-14', 'Niterói', 'RJ', 'Brasil'),        -- ID 18
('Camila Nogueira', 'mila@email.com', 'pbkdf2_sha256$870000$kwj0q50hV5947bE3g3H8K0$exemploHashValidoNoDjango==', '1996-02-01', 'Osasco', 'SP', 'Brasil'),        -- ID 19
('Thiago Barbosa', 'thi@email.com', 'pbkdf2_sha256$870000$kwj0q50hV5947bE3g3H8K0$exemploHashValidoNoDjango==', '1990-11-18', 'Londrina', 'PR', 'Brasil');       -- ID 20

-- =================================================================
-- 3. ORGANIZADORES
-- =================================================================
INSERT INTO organizador (id_usuario, cpf) VALUES (1, '111.111.111-11');
INSERT INTO organizador (id_usuario, cpf) VALUES (5, '222.222.222-22');
INSERT INTO organizador (id_usuario, cpf) VALUES (10, '333.333.333-33');

-- =================================================================
-- 4. COMPETIÇÕES PREDIÇÃO
-- =================================================================

-- 4.1. PREDIÇÃO OFICIAL (ENCERRADA - Vendas Natal)
-- ID: 1 | Org: 1
INSERT INTO competicao_pred (id_org_competicao, titulo, descricao, dificuldade, flg_oficial, data_inicio, data_fim, metrica_desempenho, premiacao, dataset_tt, dataset_submissao, dataset_gabarito, flg_deletada, flg_premiada)
VALUES (1, 'Previsão de Vendas Natal', 'Competição encerrada e premiada.', 'AVANCADO', 1, NOW() - INTERVAL '60 days', NOW() - INTERVAL '10 days', 'RMSE', 5000.00, 'datasets/vendas_tt.csv', 'datasets/vendas_sub.csv', 'datasets/vendas_gab.csv', false, true);

-- 4.2. PREDIÇÃO AMADORA (EM ANDAMENTO - Titanic)
-- ID: 2 | Org: 1
INSERT INTO competicao_pred (id_org_competicao, titulo, descricao, dificuldade, flg_oficial, data_inicio, data_fim, metrica_desempenho, premiacao, dataset_tt, dataset_submissao, dataset_gabarito, flg_deletada, flg_premiada)
VALUES (1, 'Titanic: Quem sobrevive?', 'Desafio clássico em andamento.', 'INICIANTE', 0, NOW() - INTERVAL '10 days', NOW() + INTERVAL '20 days', 'ACURACIA', NULL, 'datasets/titanic_tt.csv', 'datasets/titanic_sub.csv', 'datasets/titanic_gab.csv', false, false);

-- 4.3. PREDIÇÃO OFICIAL (FUTURA - Fraude)
-- ID: 3 | Org: 5
INSERT INTO competicao_pred (id_org_competicao, titulo, descricao, dificuldade, flg_oficial, data_inicio, data_fim, metrica_desempenho, premiacao, dataset_tt, dataset_submissao, dataset_gabarito, flg_deletada, flg_premiada)
VALUES (5, 'Detecção de Fraude Bancária', 'Começa em breve. Prepare seus modelos!', 'INTERMEDIARIO', 1, NOW() + INTERVAL '5 days', NOW() + INTERVAL '35 days', 'F1', 10000.00, 'datasets/fraude_tt.csv', 'datasets/fraude_sub.csv', 'datasets/fraude_gab.csv', false, false);

-- 4.4. PREDIÇÃO OFICIAL (ENCERRADA - Preço Casas)
-- ID: 4 | Org: 10
INSERT INTO competicao_pred (id_org_competicao, titulo, descricao, dificuldade, flg_oficial, data_inicio, data_fim, metrica_desempenho, premiacao, dataset_tt, dataset_submissao, dataset_gabarito, flg_deletada, flg_premiada)
VALUES (10, 'Previsão Preço Imóveis', 'Competição finalizada. Grande volume de dados.', 'INTERMEDIARIO', 1, NOW() - INTERVAL '40 days', NOW() - INTERVAL '5 days', 'MAE', 3000.00, 'datasets/casas_tt.csv', 'datasets/casas_sub.csv', 'datasets/casas_gab.csv', false, true);


-- =================================================================
-- 5. COMPETIÇÕES SIMULAÇÃO
-- =================================================================

-- 5.1. SIMULAÇÃO OFICIAL (ENCERRADA - Carro Autônomo)
-- ID: 1 | Org: 1
INSERT INTO competicao_simul (id_org_competicao, titulo, descricao, dificuldade, flg_oficial, data_inicio, data_fim, metrica_desempenho, premiacao, ambiente, flg_deletada, flg_premiada)
VALUES (1, 'Carro Autônomo 2D', 'Construa um agente que dirige sozinho.', 'AVANCADO', 1, NOW() - INTERVAL '50 days', NOW() - INTERVAL '2 days', 'PONTUACAO_TOTAL', 2500.00, 'ambientes/carro_2d.py', false, true);

-- 5.2. SIMULAÇÃO AMADORA (EM ANDAMENTO - Snake)
-- ID: 2 | Org: 5
INSERT INTO competicao_simul (id_org_competicao, titulo, descricao, dificuldade, flg_oficial, data_inicio, data_fim, metrica_desempenho, premiacao, ambiente, flg_deletada, flg_premiada)
VALUES (5, 'Snake Game AI', 'Quem faz a cobra crescer mais?', 'INICIANTE', 0, NOW() - INTERVAL '5 days', NOW() + INTERVAL '25 days', 'SOBREVIVENCIA', NULL, 'ambientes/snake.py', false, false);

-- 5.3. SIMULAÇÃO OFICIAL (EM ANDAMENTO - Drone)
-- ID: 3 | Org: 1
INSERT INTO competicao_simul (id_org_competicao, titulo, descricao, dificuldade, flg_oficial, data_inicio, data_fim, metrica_desempenho, premiacao, ambiente, flg_deletada, flg_premiada)
VALUES (1, 'Drone Racing League', 'Corrida de drones em ambiente 3D simulado.', 'AVANCADO', 1, NOW() - INTERVAL '20 days', NOW() + INTERVAL '10 days', 'TEMPO_CONCLUSAO', 15000.00, 'ambientes/drone.py', false, false);

-- 5.4. SIMULAÇÃO AMADORA (FUTURA - Labirinto)
-- ID: 4 | Org: 10
INSERT INTO competicao_simul (id_org_competicao, titulo, descricao, dificuldade, flg_oficial, data_inicio, data_fim, metrica_desempenho, premiacao, ambiente, flg_deletada, flg_premiada)
VALUES (10, 'Labirinto Infinito', 'Escape do labirinto gerado proceduralmente.', 'INTERMEDIARIO', 0, NOW() + INTERVAL '10 days', NOW() + INTERVAL '40 days', 'PASSOS_EXECUTADOS', NULL, 'ambientes/maze.py', false, false);


-- =================================================================
-- 6. EQUIPES E MEMBROS (PREDIÇÃO)
-- =================================================================

-- >> Competição Pred 1 (Vendas Natal - Encerrada)
-- Org: 1
INSERT INTO equipe_pred (id_competicao, id_org_competicao, nome) VALUES (1, 1, 'Alpha Team'); -- Eq 1
INSERT INTO equipe_pred (id_competicao, id_org_competicao, nome) VALUES (1, 1, 'Beta Analytics'); -- Eq 2
INSERT INTO equipe_pred (id_competicao, id_org_competicao, nome) VALUES (1, 1, 'Gamma Ray'); -- Eq 3
INSERT INTO equipe_pred (id_competicao, id_org_competicao, nome) VALUES (1, 1, 'Delta Force'); -- Eq 4

-- Membros Comp 1
INSERT INTO composicao_equipe_pred (id_equipe, id_competicao, id_org_competicao, id_competidor, data_hora_inicio) VALUES (1, 1, 1, 2, NOW() - INTERVAL '59 days'); -- Dev Pro
INSERT INTO composicao_equipe_pred (id_equipe, id_competicao, id_org_competicao, id_competidor, data_hora_inicio) VALUES (1, 1, 1, 4, NOW() - INTERVAL '59 days'); -- Ana
INSERT INTO composicao_equipe_pred (id_equipe, id_competicao, id_org_competicao, id_competidor, data_hora_inicio) VALUES (2, 1, 1, 6, NOW() - INTERVAL '58 days'); -- Carlos
INSERT INTO composicao_equipe_pred (id_equipe, id_competicao, id_org_competicao, id_competidor, data_hora_inicio) VALUES (3, 1, 1, 7, NOW() - INTERVAL '55 days'); -- Bia
INSERT INTO composicao_equipe_pred (id_equipe, id_competicao, id_org_competicao, id_competidor, data_hora_inicio) VALUES (3, 1, 1, 8, NOW() - INTERVAL '55 days'); -- Lucas
INSERT INTO composicao_equipe_pred (id_equipe, id_competicao, id_org_competicao, id_competidor, data_hora_inicio) VALUES (4, 1, 1, 3, NOW() - INTERVAL '50 days'); -- Noob

-- >> Competição Pred 2 (Titanic - Em Andamento)
-- Org: 1
INSERT INTO equipe_pred (id_competicao, id_org_competicao, nome) VALUES (2, 1, 'Iceberg'); -- Eq 5
INSERT INTO equipe_pred (id_competicao, id_org_competicao, nome) VALUES (2, 1, 'Titanic Survivors'); -- Eq 6

-- Membros Comp 2
INSERT INTO composicao_equipe_pred (id_equipe, id_competicao, id_org_competicao, id_competidor, data_hora_inicio) VALUES (5, 2, 1, 2, NOW() - INTERVAL '9 days'); -- Dev Pro
INSERT INTO composicao_equipe_pred (id_equipe, id_competicao, id_org_competicao, id_competidor, data_hora_inicio) VALUES (6, 2, 1, 9, NOW() - INTERVAL '8 days'); -- Fernanda

-- >> Competição Pred 4 (Imóveis - Encerrada)
-- Org: 10
INSERT INTO equipe_pred (id_competicao, id_org_competicao, nome) VALUES (4, 10, 'Real Estate AI'); -- Eq 7
INSERT INTO equipe_pred (id_competicao, id_org_competicao, nome) VALUES (4, 10, 'House Hunters'); -- Eq 8

-- Membros Comp 4
INSERT INTO composicao_equipe_pred (id_equipe, id_competicao, id_org_competicao, id_competidor, data_hora_inicio) VALUES (7, 4, 10, 2, NOW() - INTERVAL '39 days'); -- Dev Pro (Ganhando tudo)
INSERT INTO composicao_equipe_pred (id_equipe, id_competicao, id_org_competicao, id_competidor, data_hora_inicio) VALUES (8, 4, 10, 11, NOW() - INTERVAL '38 days'); -- Juliana


-- =================================================================
-- 7. EQUIPES E MEMBROS (SIMULAÇÃO)
-- =================================================================

-- >> Competição Simul 1 (Carro - Encerrada)
-- Org: 1
INSERT INTO equipe_simul (id_competicao, id_org_competicao, nome) VALUES (1, 1, 'Fast Cars'); -- Eq 1
INSERT INTO equipe_simul (id_competicao, id_org_competicao, nome) VALUES (1, 1, 'Slow & Steady'); -- Eq 2
INSERT INTO equipe_simul (id_competicao, id_org_competicao, nome) VALUES (1, 1, 'Crash Test Dummies'); -- Eq 3

-- Membros Comp 1
INSERT INTO composicao_equipe_simul (id_equipe, id_competicao, id_org_competicao, id_competidor, data_hora_inicio) VALUES (1, 1, 1, 6, NOW() - INTERVAL '49 days'); -- Carlos
INSERT INTO composicao_equipe_simul (id_equipe, id_competicao, id_org_competicao, id_competidor, data_hora_inicio) VALUES (1, 1, 1, 12, NOW() - INTERVAL '49 days'); -- Pedro
INSERT INTO composicao_equipe_simul (id_equipe, id_competicao, id_org_competicao, id_competidor, data_hora_inicio) VALUES (2, 1, 1, 3, NOW() - INTERVAL '48 days'); -- Noob
INSERT INTO composicao_equipe_simul (id_equipe, id_competicao, id_org_competicao, id_competidor, data_hora_inicio) VALUES (3, 1, 1, 13, NOW() - INTERVAL '45 days'); -- Mariana

-- >> Competição Simul 3 (Drone - Em Andamento)
-- Org: 1
INSERT INTO equipe_simul (id_competicao, id_org_competicao, nome) VALUES (3, 1, 'Sky High'); -- Eq 4
INSERT INTO composicao_equipe_simul (id_equipe, id_competicao, id_org_competicao, id_competidor, data_hora_inicio) VALUES (4, 3, 1, 2, NOW() - INTERVAL '19 days'); -- Dev Pro


-- =================================================================
-- 8. SUBMISSÕES (Histórico)
-- =================================================================

-- Pred 1 (Natal) - RMSE (Menor é melhor)
-- Eq 1 (Vencedora)
INSERT INTO submissao_equipe_pred (id_equipe, id_competicao, id_org_competicao, data_hora_envio, arq_submissao, score) VALUES (1, 1, 1, NOW() - INTERVAL '40 days', 'sub.csv', 500.0);
INSERT INTO submissao_equipe_pred (id_equipe, id_competicao, id_org_competicao, data_hora_envio, arq_submissao, score) VALUES (1, 1, 1, NOW() - INTERVAL '20 days', 'sub.csv', 200.0);
INSERT INTO submissao_equipe_pred (id_equipe, id_competicao, id_org_competicao, data_hora_envio, arq_submissao, score) VALUES (1, 1, 1, NOW() - INTERVAL '12 days', 'sub.csv', 50.5);

-- Eq 2 (2º)
INSERT INTO submissao_equipe_pred (id_equipe, id_competicao, id_org_competicao, data_hora_envio, arq_submissao, score) VALUES (2, 1, 1, NOW() - INTERVAL '15 days', 'sub.csv', 80.0);

-- Eq 3 (3º)
INSERT INTO submissao_equipe_pred (id_equipe, id_competicao, id_org_competicao, data_hora_envio, arq_submissao, score) VALUES (3, 1, 1, NOW() - INTERVAL '18 days', 'sub.csv', 150.0);

-- Eq 4 (4º)
INSERT INTO submissao_equipe_pred (id_equipe, id_competicao, id_org_competicao, data_hora_envio, arq_submissao, score) VALUES (4, 1, 1, NOW() - INTERVAL '11 days', 'sub.csv', 300.0);


-- Simul 1 (Carro) - Pontos (Maior é melhor)
-- Eq 1 (Vencedora)
INSERT INTO submissao_equipe_simul (id_equipe, id_competicao, id_org_competicao, data_hora_envio, arq_submissao, score) VALUES (1, 1, 1, NOW() - INTERVAL '40 days', 'env.py', 1000.0);
INSERT INTO submissao_equipe_simul (id_equipe, id_competicao, id_org_competicao, data_hora_envio, arq_submissao, score) VALUES (1, 1, 1, NOW() - INTERVAL '10 days', 'env.py', 5000.0);

-- Eq 2
INSERT INTO submissao_equipe_simul (id_equipe, id_competicao, id_org_competicao, data_hora_envio, arq_submissao, score) VALUES (2, 1, 1, NOW() - INTERVAL '12 days', 'env.py', 2000.0);

-- Eq 3
INSERT INTO submissao_equipe_simul (id_equipe, id_competicao, id_org_competicao, data_hora_envio, arq_submissao, score) VALUES (3, 1, 1, NOW() - INTERVAL '5 days', 'env.py', 500.0);


-- Pred 4 (Imoveis) - MAE (Menor é melhor)
-- Eq 7 (Vencedora)
INSERT INTO submissao_equipe_pred (id_equipe, id_competicao, id_org_competicao, data_hora_envio, arq_submissao, score) VALUES (7, 4, 10, NOW() - INTERVAL '10 days', 'sub.csv', 1200.0);
-- Eq 8
INSERT INTO submissao_equipe_pred (id_equipe, id_competicao, id_org_competicao, data_hora_envio, arq_submissao, score) VALUES (8, 4, 10, NOW() - INTERVAL '10 days', 'sub.csv', 5000.0);


-- =================================================================
-- 9. PRÊMIOS (Inserção Manual dos Resultados das Competições Encerradas)
-- =================================================================

-- Pred 1 (Natal) - Total 5000.00
-- 1º: Eq 1 (Carlos ID 2, Ana ID 4) -> Ouro + 2500 cada
INSERT INTO premios_competidor_pred (id_competidor, id_competicao, id_org_competicao, data_recebimento, tipo, classificacao, valor) VALUES (2, 1, 1, NOW(), 0, 1, NULL);
INSERT INTO premios_competidor_pred (id_competidor, id_competicao, id_org_competicao, data_recebimento, tipo, classificacao, valor) VALUES (2, 1, 1, NOW(), 3, 1, 2500.00);
INSERT INTO premios_competidor_pred (id_competidor, id_competicao, id_org_competicao, data_recebimento, tipo, classificacao, valor) VALUES (4, 1, 1, NOW(), 0, 1, NULL);
INSERT INTO premios_competidor_pred (id_competidor, id_competicao, id_org_competicao, data_recebimento, tipo, classificacao, valor) VALUES (4, 1, 1, NOW(), 3, 1, 2500.00);

-- 2º: Eq 2 (Carlos ID 6) -> Prata
INSERT INTO premios_competidor_pred (id_competidor, id_competicao, id_org_competicao, data_recebimento, tipo, classificacao, valor) VALUES (6, 1, 1, NOW(), 1, 2, NULL);

-- 3º: Eq 3 (Bia ID 7, Lucas ID 8) -> Bronze
INSERT INTO premios_competidor_pred (id_competidor, id_competicao, id_org_competicao, data_recebimento, tipo, classificacao, valor) VALUES (7, 1, 1, NOW(), 2, 3, NULL);
INSERT INTO premios_competidor_pred (id_competidor, id_competicao, id_org_competicao, data_recebimento, tipo, classificacao, valor) VALUES (8, 1, 1, NOW(), 2, 3, NULL);


-- Simul 1 (Carro) - Total 2500.00
-- 1º: Eq 1 (Carlos ID 6, Pedro ID 12) -> Ouro + 1250 cada
INSERT INTO premios_competidor_simul (id_competidor, id_competicao, id_org_competicao, data_recebimento, tipo, classificacao, valor) VALUES (6, 1, 1, NOW(), 0, 1, NULL);
INSERT INTO premios_competidor_simul (id_competidor, id_competicao, id_org_competicao, data_recebimento, tipo, classificacao, valor) VALUES (6, 1, 1, NOW(), 3, 1, 1250.00);
INSERT INTO premios_competidor_simul (id_competidor, id_competicao, id_org_competicao, data_recebimento, tipo, classificacao, valor) VALUES (12, 1, 1, NOW(), 0, 1, NULL);
INSERT INTO premios_competidor_simul (id_competidor, id_competicao, id_org_competicao, data_recebimento, tipo, classificacao, valor) VALUES (12, 1, 1, NOW(), 3, 1, 1250.00);

-- 2º: Eq 2 (Noob ID 3) -> Prata
INSERT INTO premios_competidor_simul (id_competidor, id_competicao, id_org_competicao, data_recebimento, tipo, classificacao, valor) VALUES (3, 1, 1, NOW(), 1, 2, NULL);

-- 3º: Eq 3 (Mariana ID 13) -> Bronze
INSERT INTO premios_competidor_simul (id_competidor, id_competicao, id_org_competicao, data_recebimento, tipo, classificacao, valor) VALUES (13, 1, 1, NOW(), 2, 3, NULL);


-- Pred 4 (Imóveis) - Total 3000.00
-- 1º: Eq 7 (Dev Pro ID 2) -> Ouro + 3000
INSERT INTO premios_competidor_pred (id_competidor, id_competicao, id_org_competicao, data_recebimento, tipo, classificacao, valor) VALUES (2, 4, 10, NOW(), 0, 1, NULL);
INSERT INTO premios_competidor_pred (id_competidor, id_competicao, id_org_competicao, data_recebimento, tipo, classificacao, valor) VALUES (2, 4, 10, NOW(), 3, 1, 3000.00);

-- 2º: Eq 8 (Juliana ID 11) -> Prata
INSERT INTO premios_competidor_pred (id_competidor, id_competicao, id_org_competicao, data_recebimento, tipo, classificacao, valor) VALUES (11, 4, 10, NOW(), 1, 2, NULL);