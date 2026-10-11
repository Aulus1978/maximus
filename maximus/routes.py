from pathlib import Path
from uuid import uuid4

from flask import Blueprint, abort, current_app, flash, redirect, render_template, request, send_from_directory, url_for
from werkzeug.utils import secure_filename
from .db import get_db, query

bp = Blueprint("main", __name__)


def modules():
    return query("SELECT * FROM modules ORDER BY sort_order")


def totals(where="", params=()):
    clause = f" WHERE {where}" if where else ""
    row = query(f"""SELECT COUNT(*) identified,
      SUM(existence_status='Existe') existing, SUM(existence='A reconstruir' AND recovery_batch IS NULL) rebuild,
      SUM(validation_status='confirmed') confirmed, SUM(validation_status='under_review') under_review,
      SUM(status IN ('Digitalizada','Operacional')) digitized, SUM(status='Operacional') operational
      FROM tools{clause}""", params, one=True)
    return {key: (row[key] or 0) for key in row.keys()}


def progress(stats):
    identified, existing = stats["identified"], stats["existing"]
    return {
        "recovery": round(existing / identified * 100) if identified else 0,
        "digitalization": round(stats["digitized"] / existing * 100) if existing else 0,
        "operational": round(stats["operational"] / existing * 100) if existing else 0,
    }


@bp.app_context_processor
def inject_navigation():
    note = query("SELECT content, updated_at FROM page_notes WHERE page_key=?", (request.path,), one=True)
    return {"nav_modules": modules(), "page_note": note}


@bp.post("/anotacoes")
def save_page_note():
    page_key = request.form.get("page_key", "")
    return_to = request.form.get("return_to", "")
    if not page_key.startswith("/") or page_key.startswith("//"):
        abort(400)
    content = request.form.get("content", "").strip()
    db = get_db()
    db.execute("""INSERT INTO page_notes (page_key, content) VALUES (?, ?)
      ON CONFLICT(page_key) DO UPDATE SET content=excluded.content, updated_at=CURRENT_TIMESTAMP""",
      (page_key, content))
    db.commit()
    flash("Anotação da página salva.", "success")
    target = return_to if return_to.startswith("/") and not return_to.startswith("//") else page_key
    return redirect(target + ("&" if "?" in target else "?") + "anotacao=salva#anotacoes-da-pagina")


@bp.get("/")
def home():
    stats = totals()
    module_rows = query("""SELECT m.*, COUNT(t.id) identified, COALESCE(SUM(t.existence_status='Existe'),0) existing,
      COALESCE(SUM(t.status IN ('Digitalizada','Operacional')),0) digitized,
      COALESCE(SUM(t.status='Operacional'),0) operational,
      (SELECT COUNT(*) FROM gaps g WHERE g.module_id=m.id) gaps
      FROM modules m LEFT JOIN tools t ON t.module_id=m.id GROUP BY m.id ORDER BY m.sort_order""")
    return render_template("home.html", stats=stats, progress=progress(stats), module_rows=module_rows,
                           gap_count=query("SELECT COUNT(*) n FROM gaps", one=True)["n"],
                           project_updates=query("SELECT * FROM project_updates ORDER BY update_date DESC,id DESC LIMIT 8"))


@bp.get("/consultoria")
def consulting():
    return render_template("consulting.html", modules=modules())


@bp.get("/metodologia")
def methodology():
    return render_template("methodology.html", modules=modules())


KNOWLEDGE_AREAS = (
    {"slug": "administracao", "name": "Administração", "description": "Fundamentos, organizações, decisões e práticas de gestão.", "status": "Em organização", "color": "#69b7ff"},
    {"slug": "economia", "name": "Economia", "description": "Conceitos econômicos, cenários, mercados e análise aplicada.", "status": "Material existente", "color": "#ffd27a"},
    {"slug": "pmo", "name": "Gestão de Projetos e PMO", "description": "Governança, portfólio, entrega, valor, maturidade e IA.", "status": "Jornada disponível", "color": "#7ee0c3"},
    {"slug": "six-sigma", "name": "Qualidade e Six Sigma", "description": "Melhoria contínua, métodos estatísticos e formação Belt.", "status": "Próxima jornada", "color": "#9fe3b1"},
    {"slug": "estrategia", "name": "Estratégia", "description": "Escolhas, posicionamento, execução e geração de valor.", "status": "Em organização", "color": "#b8a5ff"},
    {"slug": "financas", "name": "Finanças", "description": "Decisões financeiras, desempenho e sustentabilidade.", "status": "Em organização", "color": "#ffad7a"},
    {"slug": "operacoes", "name": "Operações", "description": "Processos, capacidade, produtividade e excelência operacional.", "status": "Em organização", "color": "#72d5e8"},
)

PMO_JOURNEY = (
    {"number": 1, "group": "Fundamentos", "title": "O que é um PMO?", "summary": "Visibilidade, governança e valor como fundamentos do escritório de projetos."},
    {"number": 2, "group": "Fundamentos", "title": "Tipos de PMO e alcance", "summary": "Supporting, Controlling, Directive, EPMO e outros modelos organizacionais."},
    {"number": 3, "group": "Fundamentos", "title": "Quem decide o quê?", "summary": "Governança, direitos de decisão, guardrails e escalonamento."},
    {"number": 4, "group": "Fundamentos", "title": "Projeto ≠ Programa ≠ Portfólio", "summary": "As diferentes unidades do sistema de entrega e seus objetivos."},
    {"number": 5, "group": "Operação", "title": "Stage-Gates sem virar burocracia", "summary": "Governança proporcional ao risco durante o ciclo de execução."},
    {"number": 6, "group": "Operação", "title": "Do semáforo à realização de valor", "summary": "Métricas equilibradas, benefícios, KPI, KRI e OKR."},
    {"number": 7, "group": "Operação", "title": "Tradicional, Agile e Hybrid", "summary": "Escolha consciente do modelo de entrega conforme o contexto."},
    {"number": 8, "group": "Operação", "title": "Capacidade, riscos e dependências", "summary": "Orquestração integrada da demanda, dos recursos e das restrições."},
    {"number": 9, "group": "Evolução", "title": "Maturidade de PMO", "summary": "Evolução progressiva das capacidades e da entrega de valor."},
    {"number": 10, "group": "Evolução", "title": "PMO moderno, EPMO e xMO", "summary": "O PMO como capacidade empresarial de execução da estratégia."},
    {"number": 11, "group": "Evolução", "title": "IA no PMO", "summary": "Automação, analytics aumentado e copilotos de governança."},
    {"number": 12, "group": "Evolução", "title": "Implantação em 100 dias", "summary": "Diagnosticar, desenhar, entregar quick wins e escalar."},
)


@bp.get("/conhecimento")
def knowledge_index():
    study_count = query("SELECT COUNT(*) n FROM studies", one=True)["n"]
    return render_template("knowledge.html", knowledge_areas=KNOWLEDGE_AREAS,
                           study_count=study_count, pmo_modules=len(PMO_JOURNEY))


@bp.get("/conhecimento/pmo")
def knowledge_pmo():
    return render_template("knowledge_pmo.html", journey=PMO_JOURNEY)


@bp.get("/modulos/<slug>")
def module_detail(slug):
    module = query("SELECT * FROM modules WHERE slug=?", (slug,), one=True)
    if not module: abort(404)
    args, conditions = [module["id"]], ["t.module_id=?"]
    for field in ("validation_status", "status"):
        if request.args.get(field):
            conditions.append(f"t.{field}=?"); args.append(request.args[field])
    if request.args.get("category"):
        conditions.append("c.name=?"); args.append(request.args["category"])
    if request.args.get("q"):
        conditions.append("(t.name LIKE ? OR t.code LIKE ? OR t.summary LIKE ?)")
        term = f"%{request.args['q']}%"; args.extend([term,term,term])
    tools = query(f"""SELECT t.*, c.name category, p.name position_name, p.code position_code,
      pp.name parent_position_name, COUNT(f.id) file_count FROM tools t
      LEFT JOIN categories c ON c.id=t.category_id LEFT JOIN files f ON f.tool_id=t.id
      LEFT JOIN module_positions p ON p.id=t.position_id LEFT JOIN module_positions pp ON pp.id=p.parent_id
      WHERE {' AND '.join(conditions)} GROUP BY t.id ORDER BY t.code""", args)
    stats = totals("module_id=?", (module["id"],))
    gaps = query("""SELECT g.*, t.name generated_tool, p.name position_name FROM gaps g
      LEFT JOIN tools t ON t.id=g.generated_tool_id LEFT JOIN module_positions p ON p.id=g.position_id
      WHERE g.module_id=? ORDER BY CASE g.priority WHEN 'Alta' THEN 1 WHEN 'Média' THEN 2 ELSE 3 END""", (module["id"],))
    positions = query("""SELECT p.*,
      (SELECT COUNT(*) FROM tools t WHERE t.position_id=p.id OR t.position_id IN (SELECT id FROM module_positions WHERE parent_id=p.id)) tool_count,
      (SELECT COUNT(*) FROM gaps g WHERE (g.position_id=p.id OR g.position_id IN (SELECT id FROM module_positions WHERE parent_id=p.id)) AND g.situation!='Resolvido') gap_count,
      COALESCE((SELECT COUNT(*) FROM tools t WHERE (t.position_id=p.id OR t.position_id IN (SELECT id FROM module_positions WHERE parent_id=p.id)) AND t.existence_status='Existe'),0) existing,
      COALESCE((SELECT COUNT(*) FROM tools t WHERE (t.position_id=p.id OR t.position_id IN (SELECT id FROM module_positions WHERE parent_id=p.id)) AND t.status IN ('Digitalizada','Operacional')),0) digitized,
      COALESCE((SELECT COUNT(*) FROM tools t WHERE (t.position_id=p.id OR t.position_id IN (SELECT id FROM module_positions WHERE parent_id=p.id)) AND t.status='Operacional'),0) operational
      FROM module_positions p WHERE p.module_id=? ORDER BY p.parent_id IS NOT NULL,p.sort_order""", (module["id"],))
    position_tools = query("""SELECT t.*,p.id position_key FROM tools t JOIN module_positions p ON p.id=t.position_id
      WHERE t.module_id=? ORDER BY t.display_order,t.id""", (module["id"],))
    tools_by_position = {}
    for tool in position_tools:
        tools_by_position.setdefault(tool["position_key"], []).append(tool)
    children_by_position = {}
    roots = []
    for position in positions:
        if position["parent_id"]:
            children_by_position.setdefault(position["parent_id"], []).append(position)
        else:
            roots.append(position)
    comparison_modules = modules()
    comparison_positions = query("""SELECT p.*,
      (SELECT COUNT(*) FROM tools t WHERE t.position_id=p.id OR t.position_id IN
        (SELECT id FROM module_positions WHERE parent_id=p.id)) tool_count
      FROM module_positions p ORDER BY p.module_id,p.parent_id IS NOT NULL,p.sort_order""")
    comparison_roots = {}
    comparison_children = {}
    for position in comparison_positions:
        if position["parent_id"]:
            comparison_children.setdefault(position["parent_id"], []).append(position)
        else:
            comparison_roots.setdefault(position["module_id"], []).append(position)
    comparison_tools = query("""SELECT t.*,p.id position_key,m.slug module_slug
      FROM tools t JOIN module_positions p ON p.id=t.position_id
      JOIN modules m ON m.id=t.module_id ORDER BY t.display_order,t.id""")
    comparison_tools_by_position = {}
    for tool in comparison_tools:
        comparison_tools_by_position.setdefault(tool["position_key"], []).append(tool)
    return render_template("module.html", module=module, tools=tools, gaps=gaps, stats=stats,
                           progress=progress(stats), categories=query("SELECT * FROM categories ORDER BY name"),
                           position_roots=roots, position_children=children_by_position,
                           tools_by_position=tools_by_position, comparison_modules=comparison_modules,
                           comparison_roots=comparison_roots, comparison_children=comparison_children,
                           comparison_tools_by_position=comparison_tools_by_position)


@bp.route("/ferramentas/nova", methods=("GET","POST"))
def tool_new():
    if request.method == "POST":
        data = request.form
        required = ("module_id","position_id","code","name","slug","summary","existence","status","validation_status")
        if not all(data.get(k) for k in required):
            flash("Preencha os campos obrigatórios.", "error")
        elif not query("SELECT id FROM module_positions WHERE id=? AND module_id=?", (data["position_id"], data["module_id"]), one=True):
            flash("A posição escolhida não pertence ao módulo selecionado.", "error")
        else:
            try:
                values = dict(data)
                values["existence_status"] = "Existe" if data["validation_status"] == "confirmed" else None
                if data.get("source_path") and not data.get("source_filename"):
                    values["source_filename"] = data["source_path"].rsplit("/", 1)[-1]
                db=get_db(); cursor=db.execute("""INSERT INTO tools
                  (module_id,category_id,position_id,code,slug,name,summary,existence,status,version,objective,description,original_method,current_version,module_function,inputs,processing,outputs,display_order,system_path,validation_status,existence_status,source_path,source_filename,source_note,historical_file_code,future_modernization)
                  VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""", tuple(values.get(k) or None for k in
                  ("module_id","category_id","position_id","code","slug","name","summary","existence","status","version","objective","description","original_method","current_version","module_function","inputs","processing","outputs","display_order","system_path","validation_status","existence_status","source_path","source_filename","source_note","historical_file_code","future_modernization")))
                if values.get("source_path"):
                    db.execute("INSERT OR IGNORE INTO evidence_sources(path,filename,note) VALUES (?,?,?)",
                               (values["source_path"], values["source_filename"], values.get("source_note")))
                    evidence_id = db.execute("SELECT id FROM evidence_sources WHERE path=?", (values["source_path"],)).fetchone()[0]
                    db.execute("INSERT OR IGNORE INTO tool_evidence(tool_id,evidence_id,note) VALUES (?,?,?)",
                               (cursor.lastrowid, evidence_id, values.get("source_note")))
                db.commit(); flash("Ferramenta cadastrada.", "success")
                return redirect(url_for("main.tool_detail", module_slug=data["module_slug"], tool_slug=data["slug"]))
            except Exception:
                flash("Código ou identificador já cadastrado.", "error")
    return render_template("tool_form.html", modules=modules(), categories=query("SELECT * FROM categories ORDER BY name"),
      positions=query("""SELECT p.*,m.name module_name FROM module_positions p JOIN modules m ON m.id=p.module_id
        ORDER BY m.sort_order,p.code"""))


@bp.get("/modulos/<module_slug>/ferramentas/<tool_slug>")
def tool_detail(module_slug, tool_slug):
    tool = query("""SELECT t.*,m.name module_name,m.slug module_slug,m.color,c.name category,
      p.name position_name,p.code position_code,pp.name parent_position_name FROM tools t
      JOIN modules m ON m.id=t.module_id LEFT JOIN categories c ON c.id=t.category_id
      LEFT JOIN module_positions p ON p.id=t.position_id LEFT JOIN module_positions pp ON pp.id=p.parent_id
      WHERE m.slug=? AND t.slug=?""", (module_slug,tool_slug), one=True)
    if not tool: abort(404)
    return render_template("tool.html", tool=tool,
      files=query("SELECT * FROM files WHERE tool_id=? ORDER BY file_date DESC",(tool["id"],)),
      evidence=query("""SELECT e.*,te.note relationship_note FROM evidence_sources e
        JOIN tool_evidence te ON te.evidence_id=e.id WHERE te.tool_id=? ORDER BY e.filename""", (tool["id"],)),
      integrations=query("""SELECT i.*,t.name target_tool,t.slug target_slug,m.slug target_module FROM integrations i
        LEFT JOIN tools t ON t.id=i.target_tool_id LEFT JOIN modules m ON m.id=t.module_id WHERE i.source_tool_id=?""",(tool["id"],)),
      fed_by=query("""SELECT i.*,t.name source_tool,t.slug source_slug,m.slug source_module FROM integrations i
        JOIN tools t ON t.id=i.source_tool_id JOIN modules m ON m.id=t.module_id WHERE i.target_tool_id=?""",(tool["id"],)),
      system_features=query("""SELECT sf.*,tsf.relationship_note FROM system_features sf JOIN tool_system_features tsf
        ON tsf.system_feature_id=sf.id WHERE tsf.tool_id=? ORDER BY sf.name""",(tool["id"],)),
      history=query("SELECT * FROM tool_history WHERE tool_id=? ORDER BY event_date",(tool["id"],)))


@bp.get("/inventario-recuperado")
def recovered_inventory():
    rows = query("""SELECT m.*,
      COALESCE(SUM(t.validation_status='confirmed'),0) confirmed,
      COALESCE(SUM(t.validation_status='under_review'),0) under_review,
      COALESCE(SUM(t.status='Digitalizada' AND t.recovery_batch IS NOT NULL),0) digitized,
      COALESCE(SUM(t.status='Operacional' AND t.recovery_batch IS NOT NULL),0) operational
      FROM modules m LEFT JOIN tools t ON t.module_id=m.id AND t.recovery_batch IS NOT NULL
      GROUP BY m.id ORDER BY m.sort_order""")
    pending = {}
    for module in rows:
        pending[module["id"]] = query("""SELECT COUNT(*) n FROM module_positions p
          WHERE p.module_id=? AND p.position_type!='pending'
          AND NOT EXISTS (SELECT 1 FROM tools t WHERE t.position_id=p.id AND t.recovery_batch IS NOT NULL)
          AND NOT EXISTS (SELECT 1 FROM module_positions c JOIN tools t ON t.position_id=c.id
                          WHERE c.parent_id=p.id AND t.recovery_batch IS NOT NULL)""", (module["id"],), one=True)["n"]
    totals_row = query("""SELECT COUNT(*) total,
      COALESCE(SUM(validation_status='confirmed'),0) confirmed,
      COALESCE(SUM(validation_status='under_review'),0) under_review,
      COALESCE(SUM(status='Digitalizada'),0) digitized,
      COALESCE(SUM(status='Operacional'),0) operational
      FROM tools WHERE recovery_batch IS NOT NULL""", one=True)
    return render_template("recovered_inventory.html", module_rows=rows, pending=pending, totals=totals_row)


@bp.route("/gaps/novo", methods=("GET","POST"))
def gap_new():
    if request.method == "POST":
        d=request.form
        valid_position = not d.get("position_id") or query(
            "SELECT id FROM module_positions WHERE id=? AND module_id=?", (d["position_id"], d["module_id"]), one=True)
        if all(d.get(x) for x in ("module_id","title","description","reason","priority","situation")) and valid_position:
            db=get_db(); db.execute("INSERT INTO gaps (module_id,position_id,generated_tool_id,title,description,reason,priority,situation,future_tools) VALUES (?,?,?,?,?,?,?,?,?)",
              tuple(d.get(k) or None for k in ("module_id","position_id","generated_tool_id","title","description","reason","priority","situation","future_tools"))); db.commit()
            slug=query("SELECT slug FROM modules WHERE id=?",(d["module_id"],),one=True)["slug"]
            flash("Gap cadastrado.","success"); return redirect(url_for("main.module_detail",slug=slug)+"#gaps")
        flash("Preencha os campos obrigatórios e escolha uma posição do mesmo módulo.","error")
    return render_template("gap_form.html",modules=modules(),tools=query("SELECT id,code,name FROM tools ORDER BY code"),
      positions=query("""SELECT p.*,m.name module_name FROM module_positions p JOIN modules m ON m.id=p.module_id
        ORDER BY m.sort_order,p.code"""))


@bp.get("/acervo")
def archive():
    conditions, args = [], []
    mapping={"module":"f.module_id","tool":"f.tool_id","type":"f.file_type","status":"f.status"}
    for key,col in mapping.items():
        if request.args.get(key): conditions.append(f"{col}=?"); args.append(request.args[key])
    if request.args.get("period"):
        conditions.append("substr(f.file_date,1,4)=?"); args.append(request.args["period"])
    where="WHERE "+" AND ".join(conditions) if conditions else ""
    files=query(f"""SELECT f.*,m.name module_name,t.name tool_name,g.title gap_title,s.title study_title FROM files f
      LEFT JOIN modules m ON m.id=f.module_id LEFT JOIN tools t ON t.id=f.tool_id
      LEFT JOIN gaps g ON g.id=f.gap_id LEFT JOIN studies s ON s.id=f.study_id {where} ORDER BY f.file_date DESC""",args)
    return render_template("archive.html",files=files,modules=modules(),tools=query("SELECT id,name FROM tools ORDER BY name"))


@bp.get("/biblioteca")
def library():
    studies=query("""SELECT s.*,GROUP_CONCAT(DISTINCT m.name) module_names,GROUP_CONCAT(DISTINCT t.name) tool_names
      FROM studies s LEFT JOIN study_modules sm ON sm.study_id=s.id LEFT JOIN modules m ON m.id=sm.module_id
      LEFT JOIN study_tools st ON st.study_id=s.id LEFT JOIN tools t ON t.id=st.tool_id GROUP BY s.id ORDER BY s.area,s.theme,s.title""")
    return render_template("library.html",studies=studies)


@bp.get("/biblioteca/macroeconomia-presidencial")
def presidential_macroeconomics():
    return render_template("studies/macroeconomia_presidencial/index.html")


@bp.route("/biblioteca/guias-rapidos", methods=("GET", "POST"))
def quick_guides():
    if request.method == "POST":
        uploaded = request.files.get("pdf")
        title = request.form.get("title", "").strip()
        description = request.form.get("description", "").strip()
        original_name = secure_filename(uploaded.filename or "") if uploaded else ""
        if not title or not uploaded or not original_name:
            flash("Informe o título e selecione um arquivo PDF.", "error")
        elif Path(original_name).suffix.lower() != ".pdf":
            flash("Somente arquivos PDF são aceitos em Guias Rápidos.", "error")
        else:
            header = uploaded.stream.read(5)
            uploaded.stream.seek(0)
            if header != b"%PDF-":
                flash("O arquivo selecionado não possui um PDF válido.", "error")
            else:
                stored_name = f"{uuid4().hex}.pdf"
                destination = Path(current_app.config["QUICK_GUIDES_UPLOAD_FOLDER"]) / stored_name
                uploaded.save(destination)
                db = get_db()
                db.execute("""INSERT INTO quick_guides
                  (title,description,original_filename,stored_filename,file_size)
                  VALUES (?,?,?,?,?)""", (title, description or None, original_name, stored_name, destination.stat().st_size))
                db.commit()
                flash("Guia rápido publicado.", "success")
                return redirect(url_for("main.quick_guides"))
    guides = query("SELECT * FROM quick_guides ORDER BY created_at DESC, id DESC")
    return render_template("quick_guides.html", guides=guides)


@bp.get("/biblioteca/guias-rapidos/<int:guide_id>/pdf")
def quick_guide_pdf(guide_id):
    guide = query("SELECT * FROM quick_guides WHERE id=?", (guide_id,), one=True)
    if not guide:
        abort(404)
    return send_from_directory(
        current_app.config["QUICK_GUIDES_UPLOAD_FOLDER"],
        guide["stored_filename"],
        mimetype="application/pdf",
        as_attachment=request.args.get("download") == "1",
        download_name=guide["original_filename"],
    )


@bp.get("/biblioteca/<slug>")
def study_detail(slug):
    study=query("SELECT * FROM studies WHERE slug=?",(slug,),one=True)
    if not study: abort(404)
    return render_template("study.html",study=study,
      related_modules=query("SELECT m.* FROM modules m JOIN study_modules sm ON sm.module_id=m.id WHERE sm.study_id=?",(study["id"],)),
      related_tools=query("SELECT t.*,m.slug module_slug FROM tools t JOIN modules m ON m.id=t.module_id JOIN study_tools st ON st.tool_id=t.id WHERE st.study_id=?",(study["id"],)))


@bp.get("/sistema")
def system_index():
    module_rows=modules(); operational=query("""SELECT t.*,m.name module_name,m.slug module_slug,m.color FROM tools t JOIN modules m ON m.id=t.module_id
      WHERE t.status='Operacional' AND t.system_path IS NOT NULL ORDER BY m.sort_order,t.name""")
    return render_template("system.html",modules=module_rows,operational=operational)
