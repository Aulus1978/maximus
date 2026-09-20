import os
from flask import Flask

from .db import close_db, init_db


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY=os.environ.get("MAXIMUS_SECRET", "dev-change-me"),
        DATABASE=os.path.join(app.instance_path, "maximus.sqlite"),
        QUICK_GUIDES_UPLOAD_FOLDER=os.path.join(app.instance_path, "uploads", "guias-rapidos"),
        MAX_CONTENT_LENGTH=16 * 1024 * 1024,
    )
    if test_config:
        app.config.update(test_config)
    os.makedirs(app.instance_path, exist_ok=True)
    os.makedirs(app.config["QUICK_GUIDES_UPLOAD_FOLDER"], exist_ok=True)

    from .routes import bp
    app.register_blueprint(bp)
    app.teardown_appcontext(close_db)

    with app.app_context():
        init_db()
    return app

