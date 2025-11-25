-- Queries para PRED espelhadas para SIMUL !

-- Total de Submissões
SELECT COUNT(*) 
FROM submissao_equipe_pred 
WHERE id_competicao = %s;

-- Média de Score (Desempenho Médio Geral)
SELECT AVG(score) 
FROM submissao_equipe_pred 
WHERE id_competicao = %s;

-- Melhor Score (Recorde da Competição - Menor Erro RMSE)
SELECT MIN(score) 
FROM submissao_equipe_pred 
WHERE id_competicao = %s;

-- Gráfico de Linha: Evolução das Submissões
SELECT 
    TO_CHAR(data_hora_envio, 'YYYY-MM-DD') as dia, 
    COUNT(*) as total_envios
FROM submissao_equipe_pred 
WHERE id_competicao = %s 
GROUP BY dia 
ORDER BY dia ASC;

-- Gráfico de Barras: Ranking das Melhores Equipes
SELECT 
    e.nome, 
    MIN(s.score) as best_score
FROM submissao_equipe_pred s
JOIN equipe_pred e ON s.id_equipe = e.id
WHERE s.id_competicao = %s
GROUP BY e.nome
ORDER BY best_score ASC
LIMIT 10;
-----------------------------------------------

-- Total de Competições Participadas
SELECT COUNT(*) 
FROM (
    SELECT id_competicao FROM composicao_equipe_pred WHERE id_competidor = %s
    UNION ALL
    SELECT id_competicao FROM composicao_equipe_simul WHERE id_competidor = %s
) AS total_comps;

-- Total de Submissões Feitas
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

-- Resumo de Prêmios (Medalhas e Dinheiro)

SELECT 
    SUM(CASE WHEN tipo = 0 THEN 1 ELSE 0 END) as ouro,
    SUM(CASE WHEN tipo = 1 THEN 1 ELSE 0 END) as prata,
    SUM(CASE WHEN tipo = 2 THEN 1 ELSE 0 END) as bronze,
    SUM(COALESCE(valor, 0)) as total_dinheiro
FROM (
    SELECT tipo, valor FROM premios_competidor_pred WHERE id_competidor = %s
    UNION ALL
    SELECT tipo, valor FROM premios_competidor_simul WHERE id_competidor = %s
) AS premios;

-- Gráfico de Linha: Histórico de Atividade (Submissões por Dia

SELECT 
    TO_CHAR(data_envio, 'YYYY-MM-DD') as dia, 
    COUNT(*) as qtd_envios
FROM (
    SELECT s.data_hora_envio as data_envio 
    FROM submissao_equipe_pred s
    JOIN composicao_equipe_pred c ON s.id_equipe = c.id_equipe
    WHERE c.id_competidor = %s
    
    UNION ALL
    
    SELECT s.data_hora_envio as data_envio 
    FROM submissao_equipe_simul s
    JOIN composicao_equipe_simul c ON s.id_equipe = c.id_equipe
    WHERE c.id_competidor = %s
) AS timeline
GROUP BY dia
ORDER BY dia ASC
LIMIT 30;

-- Gráfico de Pizza: Perfil de Participação (Predição vs. Simulação)
SELECT 'Predição' as tipo, COUNT(*) as qtd
FROM composicao_equipe_pred 
WHERE id_competidor = %s

UNION ALL

SELECT 'Simulação' as tipo, COUNT(*) as qtd
FROM composicao_equipe_simul 
WHERE id_competidor = %s;
