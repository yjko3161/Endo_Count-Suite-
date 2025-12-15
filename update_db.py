from app import create_app, db
from app.models import LoginAttempt

app = create_app()
with app.app_context():
    # Only create tables that don't exist
    # Since we are using SQLAlchemy create_all, it usually skips existing tables but we should be careful.
    # However, create_all() is safe to call, it won't overwrite data.
    db.create_all()
    print("Database tables updated.")
