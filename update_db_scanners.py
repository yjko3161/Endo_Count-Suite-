from app import create_app, db
from app.models import BlockedIp, SuspiciousEvent

app = create_app()
with app.app_context():
    # Only create tables that don't exist
    db.create_all()
    print("Database tables updated for blocked IPs.")
