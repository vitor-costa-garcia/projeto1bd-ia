/* ========================================================================== */
/* 1. RELATÓRIOS DE COMPETIÇÃO (PREDIÇÃO)                    */
/* ========================================================================== */

-- 1.1. Total de Submissões (Volume de atividade)
SELECT COUNT(*) 
FROM submissao_equipe_pred 
WHERE id_competicao = %s;

-- 1.2. Média de Score (Desempenho médio geral)
SELECT AVG(score) 
FROM submissao_equipe_pred 
WHERE id_competicao = %s;

-- 1.3. Melhor Score (Recorde atual)
-- Nota: Para Predição (RMSE/Erro), usamos MIN (quanto menor, melhor).
SELECT MIN(score) 
FROM submissao_equipe_pred 
WHERE id_competicao = %s;

-- 1.4. Gráfico de Linha: Evolução Temporal das Submissões
SELECT 
    TO_CHAR(data_hora_envio, 'YYYY-MM-DD') AS dia, 
    COUNT(*) AS total_envios
FROM submissao_equipe_pred 
WHERE id_competicao = %s 
GROUP BY dia 
ORDER BY dia ASC;

-- 1.5. Gráfico de Barras: Top 10 Equipes (Melhor Performance)
-- Agrupa por equipe e pega o MELHOR score (MIN) de cada uma.
SELECT 
    e.nome, 
    MIN(s.score) AS best_score
FROM submissao_equipe_pred s
JOIN equipe_pred e ON s.id_equipe = e.id
WHERE s.id_competicao = %s
GROUP BY e.nome
ORDER BY best_score ASC
LIMIT 10;


/* ========================================================================== */
/* 2. RELATÓRIOS DE COMPETIÇÃO (SIMULAÇÃO)                   */
/* ========================================================================== */

-- 2.1. Total de Submissões
SELECT COUNT(*) 
FROM submissao_equipe_simul 
WHERE id_competicao = %s;

-- 2.2. Média de Score
SELECT AVG(score) 
FROM submissao_equipe_simul 
WHERE id_competicao = %s;

-- 2.3. Melhor Score (Recorde atual)
-- Nota: Para Simulação (Pontos), geralmente usamos MAX (quanto maior, melhor).
SELECT MAX(score) 
FROM submissao_equipe_simul 
WHERE id_competicao = %s;

-- 2.4. Gráfico de Linha: Evolução Temporal
SELECT 
    TO_CHAR(data_hora_envio, 'YYYY-MM-DD') AS dia, 
    COUNT(*) AS total_envios
FROM submissao_equipe_simul 
WHERE id_competicao = %s 
GROUP BY dia 
ORDER BY dia ASC;

-- 2.5. Gráfico de Barras: Top 10 Equipes
-- Agrupa por equipe e pega o MELHOR score (MAX) de cada uma.
SELECT 
    e.nome, 
    MAX(s.score) AS best_score
FROM submissao_equipe_simul s
JOIN equipe_simul e ON s.id_equipe = e.id
WHERE s.id_competicao = %s
GROUP BY e.nome
ORDER BY best_score DESC
LIMIT 10;


/* ========================================================================== */
/* 3. ESTATÍSTICAS DO USUÁRIO                          */
/* ========================================================================== */

-- 3.1. KPI: Total de Competições Participadas
-- Une a participação em equipes de predição e simulação.
SELECT COUNT(*) 
FROM (
    SELECT id_competicao FROM composicao_equipe_pred WHERE id_competidor = %s
    UNION ALL
    SELECT id_competicao FROM composicao_equipe_simul WHERE id_competidor = %s
) AS total_comps;

-- 3.2. KPI: Total de Submissões Realizadas (Pela equipe do usuário)
SELECT COUNT(*) 
FROM (
    SELECT s.id_equipe 
    FROM submissao_equipe_pred s
    JOIN composicao_equipe_pred c ON s.id_equipe = c.id_equipe
    WHERE c.id_competidor = %s
    
    UNION ALL
    
    SELECT s.id_equipe 
    FROM submissao_equipe_simul s
    JOIN composicao_equipe_simul c ON s.id_equipe = c.id_equipe
    WHERE c.id_competidor = %s
) AS total_subs;

-- 3.3. KPI: Resumo de Prêmios (Medalhas e Dinheiro Acumulado)
-- Tipos: 0=Ouro, 1=Prata, 2=Bronze.
SELECT 
    SUM(CASE WHEN tipo = 0 THEN 1 ELSE 0 END) AS ouro,
    SUM(CASE WHEN tipo = 1 THEN 1 ELSE 0 END) AS prata,
    SUM(CASE WHEN tipo = 2 THEN 1 ELSE 0 END) AS bronze,
    SUM(COALESCE(valor, 0)) AS total_dinheiro
FROM (
    SELECT tipo, valor FROM premios_competidor_pred WHERE id_competidor = %s
    UNION ALL
    SELECT tipo, valor FROM premios_competidor_simul WHERE id_competidor = %s
) AS premios;

-- 3.4. Gráfico de Linha: Histórico de Atividade (Submissões por Dia)
-- Limita aos últimos 30 dias de atividade para melhor visualização.
SELECT 
    TO_CHAR(data_envio, 'YYYY-MM-DD') AS dia, 
    COUNT(*) AS qtd_envios
FROM (
    SELECT s.data_hora_envio AS data_envio 
    FROM submissao_equipe_pred s
    JOIN composicao_equipe_pred c ON s.id_equipe = c.id_equipe
    WHERE c.id_competidor = %s
    
    UNION ALL
    
    SELECT s.data_hora_envio AS data_envio 
    FROM submissao_equipe_simul s
    JOIN composicao_equipe_simul c ON s.id_equipe = c.id_equipe
    WHERE c.id_competidor = %s
) AS timeline
GROUP BY dia
ORDER BY dia ASC
LIMIT 30;

-- 3.5. Gráfico de Pizza: Perfil de Participação (Predição vs. Simulação)
SELECT 'Predição' AS tipo, COUNT(*) AS qtd
FROM composicao_equipe_pred 
WHERE id_competidor = %s

UNION ALL

SELECT 'Simulação' AS tipo, COUNT(*) AS qtd
FROM composicao_equipe_simul 
WHERE id_competidor = %s;