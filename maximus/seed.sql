INSERT INTO modules (slug,name,subtitle,description,color,sort_order) VALUES
('diamond','Diamond','Gestão Executiva','Direciona estratégia, governança, metas e tomada de decisão executiva.','#26324a',1),
('combat','Combat','Gestão Comercial','Estrutura a inteligência comercial, a carteira e a execução de vendas.','#9a3e35',2),
('quantum','Quantum','Gestão Financeira','Transforma dados financeiros em previsibilidade, controle e decisão.','#24665d',3),
('elementum','Elementum','Gestão de Produtos','Organiza portfólio, proposta de valor e ciclo de vida dos produtos.','#9a7132',4),
('regia','Régia','Gestão de Pessoas','Alinha pessoas, competências, cultura e desempenho.','#70527d',5),
('dynamic','Dynamic','Gestão de Processos','Mapeia, padroniza e melhora os processos organizacionais.','#34647d',6);
INSERT INTO categories (name) VALUES ('Diagnóstico'),('Planejamento'),('Controle'),('Análise'),('Execução');
INSERT INTO studies (area,theme,slug,title,body,references_text,authors) VALUES
('Economia','Macroeconomia','inflacao-emissao-moeda','Por que imprimir dinheiro pode gerar inflação?','Um estudo sobre oferta monetária, capacidade produtiva, expectativas e velocidade da moeda. A relação não é automática: depende do contexto econômico e institucional.','Banco Central; manuais de macroeconomia','Equipe Maximus'),
('Administração','Estratégia','execucao-estrategia','Da estratégia à execução','Investiga como objetivos, indicadores, iniciativas e rituais de gestão transformam intenção estratégica em ação coordenada.','Kaplan e Norton; Mintzberg','Equipe Maximus');
INSERT INTO study_modules VALUES (1,3),(2,1);
