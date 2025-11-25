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

