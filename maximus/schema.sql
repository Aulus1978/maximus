CREATE TABLE IF NOT EXISTS modules (
  id INTEGER PRIMARY KEY AUTOINCREMENT, slug TEXT UNIQUE NOT NULL, name TEXT UNIQUE NOT NULL,
  subtitle TEXT NOT NULL, description TEXT NOT NULL, color TEXT NOT NULL, sort_order INTEGER NOT NULL DEFAULT 0
);
CREATE TABLE IF NOT EXISTS categories (
  id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT UNIQUE NOT NULL, kind TEXT NOT NULL DEFAULT 'tool'
);
CREATE TABLE IF NOT EXISTS module_positions (
  id INTEGER PRIMARY KEY AUTOINCREMENT, module_id INTEGER NOT NULL REFERENCES modules(id),
  parent_id INTEGER REFERENCES module_positions(id), code TEXT NOT NULL, name TEXT NOT NULL,
  sort_order INTEGER NOT NULL DEFAULT 0, position_type TEXT NOT NULL,
  description TEXT, module_function TEXT, UNIQUE(module_id, code)
);
CREATE TABLE IF NOT EXISTS tools (
  id INTEGER PRIMARY KEY AUTOINCREMENT, module_id INTEGER NOT NULL REFERENCES modules(id),
  category_id INTEGER REFERENCES categories(id), position_id INTEGER REFERENCES module_positions(id), code TEXT UNIQUE NOT NULL, slug TEXT NOT NULL,
  name TEXT NOT NULL, summary TEXT NOT NULL, existence TEXT NOT NULL CHECK(existence IN ('Existe','Não encontrada','A reconstruir')),
  status TEXT NOT NULL CHECK(status IN ('Original','Digitalizada','Operacional')), version TEXT DEFAULT '1.0',
  objective TEXT, description TEXT, original_method TEXT, current_version TEXT, module_function TEXT, inputs TEXT, processing TEXT, outputs TEXT,
  display_order INTEGER NOT NULL DEFAULT 0,
  system_path TEXT, created_at TEXT DEFAULT CURRENT_TIMESTAMP, UNIQUE(module_id, slug)
);
CREATE TABLE IF NOT EXISTS gaps (
  id INTEGER PRIMARY KEY AUTOINCREMENT, module_id INTEGER NOT NULL REFERENCES modules(id), position_id INTEGER REFERENCES module_positions(id), generated_tool_id INTEGER REFERENCES tools(id),
  title TEXT NOT NULL, description TEXT NOT NULL, reason TEXT NOT NULL, priority TEXT NOT NULL,
  situation TEXT NOT NULL CHECK(situation IN ('Identificado','Em estudo','Em desenvolvimento','Resolvido')), future_tools TEXT
);
CREATE TABLE IF NOT EXISTS files (
  id INTEGER PRIMARY KEY AUTOINCREMENT, module_id INTEGER REFERENCES modules(id), tool_id INTEGER REFERENCES tools(id),
  gap_id INTEGER REFERENCES gaps(id), study_id INTEGER, name TEXT NOT NULL, file_type TEXT NOT NULL,
  description TEXT, origin TEXT, file_date TEXT, version TEXT, notes TEXT, path TEXT, status TEXT DEFAULT 'Catalogado'
);
CREATE TABLE IF NOT EXISTS studies (
  id INTEGER PRIMARY KEY AUTOINCREMENT, area TEXT NOT NULL, theme TEXT NOT NULL, slug TEXT UNIQUE NOT NULL,
  title TEXT NOT NULL, body TEXT NOT NULL, references_text TEXT, authors TEXT, created_at TEXT DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE IF NOT EXISTS tags (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT UNIQUE NOT NULL);
CREATE TABLE IF NOT EXISTS study_tags (study_id INTEGER REFERENCES studies(id), tag_id INTEGER REFERENCES tags(id), PRIMARY KEY(study_id,tag_id));
CREATE TABLE IF NOT EXISTS study_modules (study_id INTEGER REFERENCES studies(id), module_id INTEGER REFERENCES modules(id), PRIMARY KEY(study_id,module_id));
CREATE TABLE IF NOT EXISTS study_tools (study_id INTEGER REFERENCES studies(id), tool_id INTEGER REFERENCES tools(id), PRIMARY KEY(study_id,tool_id));
CREATE TABLE IF NOT EXISTS integrations (
  id INTEGER PRIMARY KEY AUTOINCREMENT, source_tool_id INTEGER NOT NULL REFERENCES tools(id), target_tool_id INTEGER REFERENCES tools(id),
  target_name TEXT, description TEXT
);
CREATE TABLE IF NOT EXISTS system_features (
  id INTEGER PRIMARY KEY AUTOINCREMENT, slug TEXT UNIQUE NOT NULL, name TEXT NOT NULL,
  description TEXT, system_path TEXT, status TEXT NOT NULL DEFAULT 'Planejada'
);
CREATE TABLE IF NOT EXISTS tool_system_features (
  tool_id INTEGER NOT NULL REFERENCES tools(id), system_feature_id INTEGER NOT NULL REFERENCES system_features(id),
  relationship_note TEXT, PRIMARY KEY(tool_id, system_feature_id)
);
CREATE TABLE IF NOT EXISTS tool_relationships (
  source_tool_id INTEGER REFERENCES tools(id), target_tool_id INTEGER REFERENCES tools(id), relationship_type TEXT NOT NULL,
  PRIMARY KEY(source_tool_id,target_tool_id,relationship_type)
);
CREATE TABLE IF NOT EXISTS tool_history (
  id INTEGER PRIMARY KEY AUTOINCREMENT, tool_id INTEGER NOT NULL REFERENCES tools(id), stage TEXT NOT NULL, event_date TEXT, notes TEXT
);
CREATE TABLE IF NOT EXISTS recovered_inventory_loads (
  key TEXT PRIMARY KEY, applied_at TEXT DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE IF NOT EXISTS page_notes (
  page_key TEXT PRIMARY KEY,
  content TEXT NOT NULL DEFAULT '',
  created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE IF NOT EXISTS quick_guides (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  title TEXT NOT NULL,
  description TEXT,
  original_filename TEXT NOT NULL,
  stored_filename TEXT UNIQUE NOT NULL,
  file_size INTEGER NOT NULL,
  created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE IF NOT EXISTS project_updates (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  update_key TEXT UNIQUE NOT NULL,
  update_date TEXT NOT NULL,
  category TEXT NOT NULL,
  title TEXT NOT NULL,
  description TEXT NOT NULL
);
