--Nº USUARIOS POR TIPO
SELECT
    COUNT(id_usuario),
    tipo
FROM
    usuario_tipo
GROUP BY tipo
;

--Nº EQUIPES POR COMPETICAO
SELECT
    COUNT(id) as n_equipes,
    id_competicao
FROM (
	SELECT * FROM equipe_pred
	UNION ALL
	SELECT * FROM equipe_simul
) AS equipes
GROUP BY id_competicao
;

--Nº COMPETIDORES ATIVOS POR COMPETICAO
SELECT
    COUNT(id_competidor) AS qtd_competidores_ativos,
    id_competicao
FROM (
    SELECT * FROM composicao_equipe_pred
	UNION ALL
	SELECT * FROM composicao_equipe_simul
)
WHERE
    data_hora_fim IS NULL
GROUP BY id_competicao
;

--Nº COMPETIDORES HISTÓRICO POR COMPETICAO
SELECT
    COUNT(DISTINCT id_competidor) AS qtd_competidores_ativos,
    id_competicao
FROM (
	SELECT * FROM composicao_equipe_pred
	UNION ALL
	SELECT * FROM composicao_equipe_simul
)
GROUP BY id_competicao
;

--RANKING GLOBAL COMPETIDORES
SELECT
    id_competidor,
    SUM((tipo + 1) * 100) AS pontuacao
FROM (
    SELECT id_competidor, tipo FROM premios_competidor_pred
    UNION ALL
    SELECT id_competidor, tipo FROM premios_competidor_simul
) AS premios
GROUP BY id_competidor
ORDER BY pontuacao DESC
;

--COMPETICOES CRIADAS POR ORGANIZADOR
SELECT
    id_org_competicao AS id_organizador,
    COUNT(id_competicao) AS n_competicoes
FROM (
    SELECT id_org_competicao, id_competicao FROM competicao_pred
    UNION ALL
    SELECT id_org_competicao, id_competicao FROM competicao_simul
) as competicoes
GROUP BY id_org_competicao
ORDER BY n_competicoes DESC
;

--RANKING EQUIPES POR COMPETICAO
SELECT
    id_competicao,
    id_org_competicao,
    id_equipe,
    MAX(score)
FROM (
    SELECT * FROM submissao_equipe_pred
    UNION ALL 
    SELECT * FROM submissao_equipe_simul
)
GROUP BY id_competicao, id_org_competicao, id_equipe
ORDER BY score DESC
;

--COMPETICOES PATROCINADAS POR PATROCINADOR
SELECT
    COUNT(id_competicao) as n_competicoes,
    cnpj_patrocinador
FROM (
    SELECT id_competicao, cnpj_patrocinador FROM competicao_pred WHERE flg_oficial = 1
    UNION ALL
    SELECT id_competicao, cnpj_patrocinador FROM competicao_simul WHERE flg_oficial = 1
)
GROUP BY cnpj_patrocinador
ORDER BY n_competicoes DESC
;

--NUMERO SUBMISSOES POR EQUIPE
SELECT
    id_competicao,
    id_org_competicao,
    id_equipe,
    COUNT(data_hora_envio) as n_submissoes
FROM (
    SELECT * FROM submissao_equipe_pred
    UNION ALL 
    SELECT * FROM submissao_equipe_simul
)
GROUP BY id_competicao, id_org_competicao, id_equipe
ORDER BY id_competicao, n_submissoes DESC
;

--PROPORCAO TIPO COMPETICOES
SELECT
    (SELECT COUNT(*) FROM competicao_pred WHERE flg_oficial = 1)*1.0/total_comp AS pct_pred_ofc,
    (SELECT COUNT(*) FROM competicao_pred WHERE flg_oficial = 0)*1.0/total_comp AS pct_pred,
    (SELECT COUNT(*) FROM competicao_simul WHERE flg_oficial = 1)*1.0/total_comp AS pct_simul_ofc,
    (SELECT COUNT(*) FROM competicao_simul WHERE flg_oficial = 0)*1.0/total_comp AS pct_simul
FROM (
    SELECT
	    COUNT(*) as total_comp
	FROM (
	    SELECT id_competicao FROM competicao_pred
		UNION ALL
		SELECT id_competicao FROM competicao_simul
    )
)
;