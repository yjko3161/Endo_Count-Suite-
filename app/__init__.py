import os
from flask import Flask
from dotenv import load_dotenv

load_dotenv()

from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_wtf.csrf import CSRFProtect


db = SQLAlchemy()
login_manager = LoginManager()
bcrypt = Bcrypt()
csrf = CSRFProtect()


def create_app(test_config=None):
    app = Flask(__name__)
    
    # Apply ProxyFix to handle X-Forwarded-For headers if behind a proxy (Nginx, ELB, etc.)
    from werkzeug.middleware.proxy_fix import ProxyFix
    app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1)

    app.config.from_mapping(
        SECRET_KEY=os.environ.get("SECRET_KEY", "dev-secret-key"),
        SQLALCHEMY_DATABASE_URI=os.environ.get(
            "DATABASE_URI", "sqlite:///endo_count.db"
        ),
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        REMEMBER_COOKIE_DURATION=0,
    )

    if test_config:
        app.config.update(test_config)

    db.init_app(app)
    login_manager.init_app(app)
    bcrypt.init_app(app)
    csrf.init_app(app)

    login_manager.login_view = "auth.login"

    from .routes import auth, dashboard, admin

    app.register_blueprint(auth.bp)
    app.register_blueprint(dashboard.bp)
    app.register_blueprint(admin.bp)

    from .models import BlockedIp, SuspiciousEvent
    from werkzeug.exceptions import Forbidden, NotFound
    from datetime import datetime, timedelta
    from flask import request, abort

    @app.before_request
    def check_blocked_ip():
        client_ip = request.remote_addr
        blocked = BlockedIp.query.filter_by(ip_address=client_ip).first()
        if blocked:
            abort(403)

    @app.errorhandler(404)
    def handle_404(e):
        client_ip = request.remote_addr
        # Log event
        db.session.add(SuspiciousEvent(ip_address=client_ip, url=request.path))
        db.session.commit()

        # Check threshold (e.g., 5 failures in 1 minute)
        cutoff = datetime.utcnow() - timedelta(minutes=1)
        count = SuspiciousEvent.query.filter(
            SuspiciousEvent.ip_address == client_ip,
            SuspiciousEvent.timestamp >= cutoff
        ).count()

        if count >= 5:
            # Check if already blocked to avoid duplicates
            existing = BlockedIp.query.filter_by(ip_address=client_ip).first()
            if not existing:
                db.session.add(BlockedIp(ip_address=client_ip, reason="Excessive 404s"))
                db.session.commit()
                # print(f"Blocked IP {client_ip} due to excessive 404s") # Debug

        return "404 Not Found", 404


    with app.app_context():
        # db.create_all() - Schema managed externally
        # from .models import ensure_admin_exists
        # ensure_admin_exists()
        pass


    return app
