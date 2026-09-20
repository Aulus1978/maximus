# MAXIMUS

Base digital da metodologia de consultoria Maximus, construída com Flask, SQLite, Jinja, CSS e JavaScript simples.

## Executar localmente

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/flask --app run run --debug
```

Acesse `http://127.0.0.1:5000`. O banco e a primeira carga do inventário histórico são criados automaticamente em `instance/maximus.sqlite` na primeira execução.

## Estrutura

- `maximus/schema.sql`: modelo relacional, incluindo posições estruturais e funcionalidades digitais.
- `maximus/seed.sql`: cadastro-base dos seis módulos.
- `maximus/recovered_inventory.py`: primeira carga documental recuperada (56 itens; 39 confirmados e 17 em validação).
- `maximus/routes.py`: consultas, indicadores, filtros e cadastros.
- `maximus/templates/`: páginas Jinja.
- `maximus/static/`: identidade visual e interação responsiva.

O item “Inventário Recuperado” da navegação apresenta a auditoria da carga por módulo.

Ao iniciar, bancos existentes são migrados incrementalmente: as 11 posições padrão de cada módulo são criadas e ferramentas ainda não classificadas são preservadas em “Posição pendente de classificação”.
