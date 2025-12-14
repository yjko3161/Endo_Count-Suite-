from app import create_app, db
from sqlalchemy import text

app = create_app()
with app.app_context():
    with db.engine.connect() as conn:
        result = conn.execute(text("SHOW CREATE TABLE users"))
        for row in result:
            print(row[1])
