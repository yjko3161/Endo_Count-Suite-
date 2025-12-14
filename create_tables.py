from app import create_app, db
from sqlalchemy import text

app = create_app()
with app.app_context():
    print("Adding missing columns...")
    with db.engine.connect() as conn:
        try:
            conn.execute(text("ALTER TABLE doctors ADD COLUMN doctor_code VARCHAR(50)"))
            print("Added doctor_code to doctors")
        except Exception as e:
            print(f"Skipped doctor_code: {e}")
            
        try:
            conn.execute(text("ALTER TABLE doctors ADD COLUMN display_order INT DEFAULT 0"))
            print("Added display_order to doctors")
        except Exception as e:
            print(f"Skipped display_order: {e}")

        try:
            conn.execute(text("ALTER TABLE categories ADD COLUMN category_code VARCHAR(50)"))
            print("Added category_code to categories")
        except Exception as e:
            print(f"Skipped category_code: {e}")
        
        try:
            conn.execute(text("ALTER TABLE categories ADD COLUMN category_name VARCHAR(50)"))
            print("Added category_name to categories")
        except Exception as e:
            print(f"Skipped category_name: {e}")

        conn.commit()
    print("Done.")
