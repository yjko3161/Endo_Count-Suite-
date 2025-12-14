from app import create_app
from app.models import db, Category, ExamLog
from sqlalchemy import text

app = create_app()

def seed_simplified():
    with app.app_context():
        print("Truncating Exam Logs and Categories...")
        # Disable foreign key checks to allow truncation
        db.session.execute(text("SET FOREIGN_KEY_CHECKS = 0"))
        db.session.execute(text("TRUNCATE TABLE exam_logs"))
        db.session.execute(text("TRUNCATE TABLE categories"))
        db.session.execute(text("SET FOREIGN_KEY_CHECKS = 1"))
        db.session.commit()

        print("Seeding Simplified Categories...")
        
        # 4 Core Categories for the Grid
        # Group Code: DASHBOARD_GRID
        # Metric Codes map to the 4 quadrants
        cats = [
            Category(group_name="Dashboard", item_name="Checkup Sedation", group_code="GRID", metric_code="CS", label_ko="검수", display_order=1),
            Category(group_name="Dashboard", item_name="Checkup General",  group_code="GRID", metric_code="CG", label_ko="검일", display_order=2),
            Category(group_name="Dashboard", item_name="Other Sedation",   group_code="GRID", metric_code="OS", label_ko="외수", display_order=3),
            Category(group_name="Dashboard", item_name="Other General",    group_code="GRID", metric_code="OG", label_ko="외일", display_order=4),
            
            # Summary-only Categories (Optional, for now just core)
            # Procedure types can be added later if needed for specific counts
            Category(group_name="Procedure", item_name="ENDO Total",       group_code="PROC", metric_code="ENDO", label_ko="위내시경", display_order=10),
            Category(group_name="Procedure", item_name="Colon Total",      group_code="PROC", metric_code="COLON", label_ko="대장내시경", display_order=11),
        ]

        db.session.add_all(cats)
        db.session.commit()
        print("Seeding Complete.")

if __name__ == "__main__":
    seed_simplified()
