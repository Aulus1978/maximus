import sqlite3
import re
import unicodedata
from pathlib import Path
from flask import current_app, g

from .recovered_inventory import BATCH, DETAIL, ITEMS


def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(current_app.config["DATABASE"])
        g.db.row_factory = sqlite3.Row
        g.db.execute("PRAGMA foreign_keys = ON")
    return g.db


def close_db(_error=None):
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_db():
    db = get_db()
    schema = Path(__file__).with_name("schema.sql").read_text(encoding="utf-8")
    db.executescript(schema)
    migrate_db(db)
    if db.execute("SELECT COUNT(*) FROM modules").fetchone()[0] == 0:
        seed = Path(__file__).with_name("seed.sql").read_text(encoding="utf-8")
        db.executescript(seed)
        seed_module_positions(db)
    seed_recovered_inventory(db)
    seed_project_updates(db)
    db.commit()


def _add_column(db, table, definition):
    name = definition.split()[0]
    columns = {row[1] for row in db.execute(f"PRAGMA table_info({table})")}
    if name not in columns:
        db.execute(f"ALTER TABLE {table} ADD COLUMN {definition}")


def migrate_db(db):
    """Incrementally upgrades existing installations without replacing their data."""
    _add_column(db, "tools", "position_id INTEGER REFERENCES module_positions(id)")
    _add_column(db, "tools", "module_function TEXT")
    _add_column(db, "tools", "display_order INTEGER NOT NULL DEFAULT 0")
    _add_column(db, "tools", "validation_status TEXT")
    _add_column(db, "tools", "existence_status TEXT")
    _add_column(db, "tools", "source_path TEXT")
    _add_column(db, "tools", "source_filename TEXT")
    _add_column(db, "tools", "source_note TEXT")
    _add_column(db, "tools", "historical_file_code TEXT")
    _add_column(db, "tools", "future_modernization TEXT")
    _add_column(db, "tools", "recovery_batch TEXT")
    _add_column(db, "gaps", "position_id INTEGER REFERENCES module_positions(id)")
    db.execute("""CREATE TABLE IF NOT EXISTS evidence_sources (
      id INTEGER PRIMARY KEY AUTOINCREMENT, path TEXT UNIQUE NOT NULL,
      filename TEXT NOT NULL, note TEXT)""")
    db.execute("""CREATE TABLE IF NOT EXISTS tool_evidence (
      tool_id INTEGER NOT NULL REFERENCES tools(id) ON DELETE CASCADE,
      evidence_id INTEGER NOT NULL REFERENCES evidence_sources(id) ON DELETE CASCADE,
      note TEXT, PRIMARY KEY(tool_id,evidence_id))""")
    seed_module_positions(db)


def seed_module_positions(db):
    roots = [
        ("1", "Diretrizes", 1, "guidelines", "Define o que orienta as decisões do módulo."),
        ("2", "Planejamento", 2, "planning", "Transforma diretrizes em planos, metas, programas e ações."),
        ("3", "Pacote Operacional", 3, "operational_package", "Executa, registra, acompanha e controla a operação (Management Book)."),
        ("4", "Gestão do Módulo", 4, "module_management", "Avalia resultados e promove correções e retornos ao planejamento e às diretrizes."),
        ("P", "Posição pendente de classificação", 99, "pending", "Preserva itens cuja posição histórica ainda requer validação."),
    ]
    children = {
        "1": [("1.0", "Missão / Visão", 0, "mission_vision", "Explicita a razão de existir e a direção pretendida do módulo."),
              ("1.1", "Estratégia", 1, "strategy", "Definições estratégicas específicas do módulo."),
              ("1.2", "Política", 2, "policy", "Políticas, princípios, critérios e regras de decisão.")],
        "3": [("3.1", "Management Book", 1, "management_book", "Organiza a visão consolidada da operação."),
              ("3.2", "Ferramentas de Gestão", 2, "management_tools", "Reúne as ferramentas que apoiam a execução e a decisão."),
              ("3.3", "Acompanhamentos", 3, "monitoring", "Acompanha a execução e seus resultados."),
              ("3.4", "Registros", 4, "records", "Preserva os registros operacionais do módulo.")],
        "4": [("4.1", "Análises e Avaliações de Resultado", 1, "analysis", "Analisa e avalia os resultados do módulo."),
              ("4.2", "Reuniões de Acompanhamento", 2, "meetings", "Estabelece a cadência de acompanhamento."),
              ("4.3", "Orientações e Feedback", 3, "feedback", "Orienta a execução e devolve feedback aos responsáveis."),
              ("4.4", "Planos de Ação", 4, "action_plans", "Registra e acompanha ações corretivas.")],
    }
    for module_id, in db.execute("SELECT id FROM modules"):
        for code, name, order, kind, function in roots:
            db.execute("""INSERT OR IGNORE INTO module_positions
                (module_id,parent_id,code,name,sort_order,position_type,description,module_function)
                VALUES (?,NULL,?,?,?,?,?,?)""", (module_id, code, name, order, kind, function, function))
        for parent_code, child_rows in children.items():
            parent_id = db.execute("SELECT id FROM module_positions WHERE module_id=? AND code=?", (module_id, parent_code)).fetchone()[0]
            for child in child_rows:
                child_code, child_name, child_order, child_kind, child_function = child
                db.execute("""INSERT OR IGNORE INTO module_positions
                    (module_id,parent_id,code,name,sort_order,position_type,description,module_function)
                    VALUES (?,?,?,?,?,?,?,?)""", (module_id, parent_id, child_code, child_name, child_order, child_kind, child_function, child_function))
        pending = db.execute("SELECT id FROM module_positions WHERE module_id=? AND code='P'", (module_id,)).fetchone()[0]
        db.execute("UPDATE tools SET position_id=? WHERE module_id=? AND position_id IS NULL", (pending, module_id))
    db.execute("""UPDATE module_positions SET
      description='Registros gerados automaticamente pelo sistema, mantidos como fase de checagem do fluxo de dados entre os módulos.',
      module_function='Registros gerados automaticamente pelo sistema, mantidos como fase de checagem do fluxo de dados entre os módulos.'
      WHERE code='3.4' AND module_id=(SELECT id FROM modules WHERE slug='diamond')""")


def seed_project_updates(db):
    updates = (
        ("base-digital", "2026-08-27", "Site", "Base digital Maximus", "Estrutura inicial do acervo metodológico, módulos, ferramentas e indicadores disponibilizada no sistema."),
        ("inventario-recuperado", "2026-08-27", "Produto", "Inventário histórico recuperado", "Carga documental organizada por módulo, posição estrutural e estado de validação."),
        ("anotacoes-pagina", "2026-08-28", "Site", "Anotações por página", "Área de trabalho criada para registrar diretamente no sistema as alterações desejadas no projeto."),
        ("matriz-consultoria-marca", "2026-08-28", "Site", "Navegação e estrutura aprimoradas", "Nova marca, apresentação da consultoria e visual matricial dos módulos incorporados à experiência."),
    )
    db.executemany("""INSERT OR IGNORE INTO project_updates
      (update_key,update_date,category,title,description) VALUES (?,?,?,?,?)""", updates)


def _slug(value):
    ascii_value = unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]+", "-", ascii_value.lower()).strip("-")


def seed_recovered_inventory(db):
    """Loads the documented 2012 inventory once, without touching user records."""
    if not db.execute("SELECT 1 FROM modules LIMIT 1").fetchone():
        return
    # Remove only the original sample content shipped with this prototype.
    demo_codes = tuple(["DIAMOND-001", "DIAMOND-002", "COMBAT-001", "COMBAT-002", "COMBAT-003",
                        "QUANTUM-001", "QUANTUM-002", "ELEMENTUM-001", "REGIA-001", "DYNAMIC-001"])
    placeholders = ",".join("?" for _ in demo_codes)
    demo_ids = [r[0] for r in db.execute(f"SELECT id FROM tools WHERE code IN ({placeholders})", demo_codes)]
    if demo_ids:
        ids = ",".join("?" for _ in demo_ids)
        for table, column in (("tool_history", "tool_id"), ("tool_evidence", "tool_id"),
                              ("files", "tool_id"), ("study_tools", "tool_id"),
                              ("tool_system_features", "tool_id")):
            db.execute(f"DELETE FROM {table} WHERE {column} IN ({ids})", demo_ids)
        db.execute(f"DELETE FROM integrations WHERE source_tool_id IN ({ids}) OR target_tool_id IN ({ids})", demo_ids * 2)
        db.execute(f"DELETE FROM tool_relationships WHERE source_tool_id IN ({ids}) OR target_tool_id IN ({ids})", demo_ids * 2)
        db.execute(f"DELETE FROM tools WHERE id IN ({ids})", demo_ids)
    demo_gaps = ("Ritual de governança", "Inteligência de canais", "Cenários financeiros",
                 "Voz do cliente", "Planejamento sucessório", "Mineração de processos")
    db.execute(f"DELETE FROM gaps WHERE title IN ({','.join('?' for _ in demo_gaps)})", demo_gaps)

    for index, data in enumerate(ITEMS, 1):
        module = db.execute("SELECT id FROM modules WHERE slug=?", (data["module"],)).fetchone()
        position = db.execute("SELECT id FROM module_positions WHERE module_id=? AND code=?",
                              (module[0], data["position"])).fetchone()
        if not position:
            raise RuntimeError(f"Posição inexistente: {data['module']} {data['position']}")
        slug = _slug(data["name"])
        # Repeated names are intentionally distinct by structural position.
        if db.execute("SELECT 1 FROM tools WHERE module_id=? AND slug=?", (module[0], slug)).fetchone():
            slug = f"{slug}-{data['position'].replace('.', '-')}"
        code = f"REC-{data['module'].upper()}-{index:03d}"
        existence_status = "Existe" if data["validation"] == "confirmed" else None
        cursor = db.execute("""INSERT OR IGNORE INTO tools
          (module_id,position_id,code,slug,name,summary,existence,status,version,
           objective,description,original_method,current_version,module_function,inputs,processing,outputs,
           display_order,validation_status,existence_status,source_path,source_filename,source_note,
           historical_file_code,future_modernization,recovery_batch)
          VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
          (module[0], position[0], code, slug, data["name"], DETAIL,
           "Existe" if existence_status else "Não encontrada", "Original", "1.0",
           DETAIL, DETAIL, DETAIL, DETAIL, DETAIL, DETAIL, DETAIL, DETAIL,
           index, data["validation"], existence_status, data["path"], Path(data["path"]).name,
           data["note"], data["historical_code"], DETAIL, BATCH))
        tool = db.execute("SELECT id FROM tools WHERE code=?", (code,)).fetchone()
        if not tool:
            continue
        db.execute("INSERT OR IGNORE INTO evidence_sources(path,filename,note) VALUES (?,?,?)",
                   (data["path"], Path(data["path"]).name, data["note"]))
        evidence = db.execute("SELECT id FROM evidence_sources WHERE path=?", (data["path"],)).fetchone()[0]
        db.execute("INSERT OR IGNORE INTO tool_evidence(tool_id,evidence_id,note) VALUES (?,?,?)",
                   (tool[0], evidence, data["note"]))
    db.execute("INSERT OR IGNORE INTO recovered_inventory_loads(key) VALUES (?)", (BATCH,))


def query(sql, params=(), one=False):
    rows = get_db().execute(sql, params).fetchall()
    return (rows[0] if rows else None) if one else rows
