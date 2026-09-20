"""Primeira carga documental recuperada do acervo histórico Maximus.

Os textos funcionais permanecem deliberadamente sem interpretação: esta carga
registra somente posição, estado de validação e evidência documental.
"""

DETAIL = "A detalhar"
BATCH = "historical-recovery-2012-v1"


def item(module, position, name, validation, path, note=None, historical_code=None):
    return {
        "module": module, "position": position, "name": name,
        "validation": validation, "path": path, "note": note,
        "historical_code": historical_code,
    }


ITEMS = [
    # Diamond — 3 confirmadas, 1 em validação
    item("diamond", "1.2", "Modelo de Negócio - Sistema Conceitual - Fluxo do Sistema - Processo", "confirmed", "arvore_produtos/Gestão Executiva - Diamond/Sistema Conceitual Gestão Executiva.pptx"),
    item("diamond", "3.2", "Indicadores-Chave (KPI)", "confirmed", "arvore_produtos/Gestão Executiva - Diamond/Pacote Operacional/Modelo_Indicadores_formatar.xlsx"),
    item("diamond", "3.4", "Registro de Indicadores: Integração com relatórios dos módulos", "confirmed", "arvore_produtos/Gestão Executiva - Diamond/Pacote Operacional/Modelo_Indicadores_formatar.xlsx"),
    item("diamond", "4", "Planos de Ação", "under_review", "arvore_produtos/Gestão Executiva - Diamond/Sistema Conceitual Gestão Executiva.pptx"),

    # Combat — 17 confirmadas, 8 em validação
    item("combat", "1.0", "Missão Visão Comercial", "under_review", "arvore_produtos/Gestão Comercial - Combat/Sistema Conceitual Combat1.pptx"),
    item("combat", "1.1", "Estratégia Comercial", "confirmed", "arvore_produtos/Gestão Comercial - Combat/Sistema Conceitual Combat (2).pptx"),
    item("combat", "1.1", "Potencial de Mercado", "under_review", "arvore_produtos/Gestão Comercial - Combat/Planejamento/Sistema Conceitual Comercial.pptx"),
    item("combat", "1.1", "Carteira de Clientes", "confirmed", "arvore_produtos/Gestão Comercial - Combat/Conteúdo para Estrutura/Modelo Gestão da Carteira de Clientes de Vendedores.xls"),
    item("combat", "1.2", "Modelo de Negócio - Sistema Conceitual - Fluxo do Sistema - Processo", "confirmed", "arvore_produtos/Gestão Comercial - Combat/Planejamento/Sistema Conceitual Comercial.pptx"),
    item("combat", "2", "Planejamento Comercial Anual", "under_review", "arvore_produtos/Gestão Comercial - Combat/Sistema Conceitual Combat (2).pptx"),
    item("combat", "2", "Mensal", "confirmed", "arvore_produtos/Gestão Comercial - Combat/Conteúdo para Estrutura/Comissões/Controle Mensal de Comissões e Ajuda de Custo.xlsx"),
    item("combat", "3.2", "Relatorio Mensal de Orçamentos", "confirmed", "arvore_produtos/Gestão Comercial - Combat/Pacote Operacional/C-3.1_Relatório Mensal de Orçamentos.xlsx", historical_code="C-3.1"),
    item("combat", "3.2", "Relatório de Vendas Diário - Mensal", "confirmed", "arvore_produtos/Gestão Comercial - Combat/Pacote Operacional/C-3.2_Relatório de Vendas Diário - Mensal.xlsx", historical_code="C-3.2"),
    item("combat", "3.2", "Relatorio Mensal de Faturamento", "under_review", "arvore_produtos/Gestão Comercial - Combat/Sistema Conceitual Combat (2).pptx"),
    item("combat", "3.2", "Relatório Mensal da Carteira de Clientes", "confirmed", "arvore_produtos/Gestão Comercial - Combat/Pacote Operacional/C-3.4_Relatório Mensal da Carteira de Clientes.xlsx", historical_code="C-3.4"),
    item("combat", "3.3", "Acompanhamento de Vendas", "under_review", "arvore_produtos/Gestão Comercial - Combat/Planejamento/Sistema Conceitual Comercial.pptx"),
    item("combat", "3.3", "Carteira de Orçamentos", "confirmed", "arvore_produtos/Gestão Comercial - Combat/Conteúdo para Estrutura/Carteira de Orçamentos.xls"),
    item("combat", "3.3", "Relatório de Vendas Diário - Mensal", "confirmed", "arvore_produtos/Gestão Comercial - Combat/Pacote Operacional/C-3.2_Relatório de Vendas Diário - Mensal.xlsx", historical_code="C-3.2"),
    item("combat", "3.3", "Acompanhamento Diário de Faturamento", "under_review", "arvore_produtos/Gestão Comercial - Combat/Sistema Conceitual Combat2013.03.25.pptx", "Evidência complementar posterior a 2012; a posição estrutural provém da Estrutura dos Módulos de 02/11/2012."),
    item("combat", "3.3", "Carteira de Clientes", "confirmed", "arvore_produtos/Gestão Comercial - Combat/Conteúdo para Estrutura/Modelo Gestão da Carteira de Clientes de Vendedores.xls"),
    item("combat", "3.3", "Planejamento Mensal de Visitas/Atendimento", "confirmed", "arvore_produtos/Gestão Comercial - Combat/Conteúdo para Estrutura/Planilha Registro Visitas e Preparação de PMV.xls"),
    item("combat", "3.3", "Programação Semanal de Visitas/Atendimento", "confirmed", "arvore_produtos/Gestão Comercial - Combat/Conteúdo para Estrutura/Quadro de Gestão de Rotas de Visitação.xls"),
    item("combat", "3.3", "Acompanhamento Semanal de Visitas/Atendimento", "confirmed", "arvore_produtos/Gestão Comercial - Combat/Conteúdo para Estrutura/Planilha Registro Visitas e Preparação de PMV.xls"),
    item("combat", "3.3", "Clientes Não Fidelizados", "confirmed", "arvore_produtos/Gestão Comercial - Combat/Pacote Operacional/C-3.12_Clientes Não Fidelizados.xlsx", historical_code="C-3.12"),
    item("combat", "3.3", "Clientes Inativos 12 últimos meses", "confirmed", "arvore_produtos/Gestão Comercial - Combat/Pacote Operacional/C-3.15_Clientes Inativos por grife_grupo_família_produtos.xlsx", historical_code="C-3.15"),
    item("combat", "3.3", "Clientes Visitados / Trafego", "confirmed", "arvore_produtos/Gestão Comercial - Combat/Conteúdo para Estrutura/Planilha Registro Visitas e Preparação de PMV.xls"),
    item("combat", "3.3", "Clientes Ativos por grife, família, grupo - produto", "confirmed", "arvore_produtos/Gestão Comercial - Combat/Pacote Operacional/C-3.15_Clientes Inativos por grife_grupo_família_produtos.xlsx", historical_code="C-3.15"),
    item("combat", "3.4", "Registro de Vendas - Linha de Venda", "under_review", "arvore_produtos/Gestão Comercial - Combat/Sistema Conceitual Combat2013.03.25.pptx", "Evidência complementar posterior a 2012; a posição estrutural provém da Estrutura dos Módulos de 02/11/2012."),
    item("combat", "4", "Reuniões de Acompanhamento", "under_review", "arvore_produtos/Gestão Comercial - Combat/Planejamento/Sistema Conceitual Comercial.pptx"),

    # Quantum — 5 confirmadas, 2 em validação
    item("quantum", "1.2", "Modelo de Negócio - Sistema Conceitual - Fluxo do Sistema - Processo", "confirmed", "arvore_produtos/Gestão Financeira/Fluxo de Caixa.cab", "Correspondência forte na primeira varredura; função e escopo aguardam revisão qualitativa."),
    item("quantum", "3.2", "Pacote Econômico", "under_review", "arvore_produtos/Gestão Financeira/Exemplo Orámento matricial.pptx"),
    item("quantum", "3.2", "DRE", "confirmed", "arvore_produtos/Gestão Financeira/DRE_Modelo Florêncio.xls"),
    item("quantum", "3.2", "DRE produto", "confirmed", "arvore_produtos/Gestão Financeira/DRE_Modelo Florêncio.xls"),
    item("quantum", "3.2", "Fluxo de Caixa", "confirmed", "arvore_produtos/Gestão Financeira/Fluxo de Caixa.cab"),
    item("quantum", "3.3", "Plano de Contas", "under_review", "arvore_produtos/Gestão Financeira/Exemplo Orámento matricial.pptx"),
    item("quantum", "4", "Planos de Ação", "confirmed", "arvore_produtos/Gestão Financeira/Exemplo Orámento matricial.pptx", "Correspondência da primeira varredura; manter para revisão qualitativa porque o nome da evidência não corresponde diretamente ao componente."),

    # Elementum — 3 confirmadas, 1 em validação
    item("elementum", "2", "Ciclo de Vida", "confirmed", "arvore_produtos/Gestão de Produtos/Modelo de Ciclo Comercial para Produtos.pptx"),
    item("elementum", "3.2", "Resultado Econômico de Produtos", "confirmed", "arvore_produtos/Gestão de Produtos/Modelo Resultado Economico Produtos_formatar.xlsx"),
    item("elementum", "3.3", "Desenvolvimento de Produto", "confirmed", "arvore_produtos/Gestão de Produtos/Fases da Gestão de Grife_2010.01.19.xlsx", "Documento histórico de 2010 usado apenas como evidência; a estrutura de referência permanece a de 02/11/2012."),
    item("elementum", "3.3", "Lançamento de Produto", "under_review", "arvore_produtos/Gestão de Produtos/Modelo de Ciclo Comercial para Produtos.pptx"),

    # Régia — 8 confirmadas, 5 em validação
    item("regia", "1.1", "Desenvolvimento de Pessoas", "confirmed", "arvore_produtos/RH - Pessoal - Vitoria Regia/Sistema de Desenvolvimento de Pessoas.docx"),
    item("regia", "1.1", "Estrutura de Cargos e Salários", "under_review", "arvore_produtos/RH - Pessoal - Vitoria Regia/Perfis e Atribuições/Supervisor Comercial.docx"),
    item("regia", "1.2", "Políticas de Desenvolvimento de Pessoas", "under_review", "arvore_produtos/RH - Pessoal - Vitoria Regia/Sistema de Desenvolvimento de Pessoas.docx"),
    item("regia", "3.2", "Avaliações Desempenho Realizadas", "under_review", "arvore_produtos/RH - Pessoal - Vitoria Regia/Ficha Acompanhamento Promoções e Avaliações de Desempenho.xls"),
    item("regia", "3.3", "Estrutura de Pessoas", "under_review", "arvore_produtos/RH - Pessoal - Vitoria Regia/Sistema de Desenvolvimento de Pessoas.docx"),
    item("regia", "3.3", "Esteira de Cargos e Salários", "confirmed", "arvore_produtos/RH - Pessoal - Vitoria Regia/Sistema de Desenvolvimento de Pessoas.docx"),
    item("regia", "3.3", "Perfis dos Cargos", "confirmed", "arvore_produtos/RH - Pessoal - Vitoria Regia/Perfis e Atribuições/Analista comercial - vaga.doc"),
    item("regia", "3.3", "Responsabilidades, Funções e Atribuições dos Cargos", "confirmed", "arvore_produtos/RH - Pessoal - Vitoria Regia/Perfis e Atribuições/Analista comercial - vaga.doc"),
    item("regia", "3.3", "Avaliações de Desempenho", "confirmed", "arvore_produtos/RH - Pessoal - Vitoria Regia/Ficha Acompanhamento Promoções e Avaliações de Desempenho.xls"),
    item("regia", "3.3", "Programas de Integração", "under_review", "arvore_produtos/RH - Pessoal - Vitoria Regia/Sistema de Desenvolvimento de Pessoas.docx"),
    item("regia", "3.3", "Programa de Treinamentos", "confirmed", "arvore_produtos/RH - Pessoal - Vitoria Regia/Avaliação do Treinamento.xlsx"),
    item("regia", "3.3", "Recrutamento e Seleção de Talentos", "confirmed", "arvore_produtos/RH - Pessoal - Vitoria Regia/Recrutamento e Seleção/Check list contratação equipe.xls"),
    item("regia", "4", "Reuniões de Acompanhamento", "confirmed", "arvore_produtos/RH - Pessoal - Vitoria Regia/Perfis e Atribuições2/Diretor Comercial - Perfis e Atribuições.docx", "Correspondência localizada no conteúdo; revisão qualitativa obrigatória porque o arquivo não possui o nome explícito da ferramenta."),

    # Dynamic — 3 confirmadas
    item("dynamic", "1.2", "Modelo de Negócio - Sistema Conceitual - Fluxo do Sistema - Processo", "confirmed", "arvore_produtos/Processos/Fluxos/Fluxo Sistema conceitual CRM.ppt"),
    item("dynamic", "3.2", "Implantação dos processos", "confirmed", "arvore_produtos/Processos/Exemplo para procedimento de operação de ferramenta.doc"),
    item("dynamic", "3.3", "Acompanhamento dos Processos", "confirmed", "arvore_produtos/Processos/Exemplo para procedimento de operação de ferramenta.doc"),
]
