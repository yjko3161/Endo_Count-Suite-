from app import create_app
from app.models import db, Category, ExamLog
from sqlalchemy import text

app = create_app()

def seed_detailed():
    with app.app_context():
        print("Truncating Exam Logs and Categories...")
        db.session.execute(text("SET FOREIGN_KEY_CHECKS = 0"))
        db.session.execute(text("TRUNCATE TABLE exam_logs"))
        db.session.execute(text("TRUNCATE TABLE categories"))
        db.session.execute(text("SET FOREIGN_KEY_CHECKS = 1"))
        db.session.commit()

        print("Seeding 8 Detailed Categories...")
        
        # 8 Categories mapping to 4 Quadrants
        # Metric Codes: 
        # PUB_S (Public Sedation), CHK_S (Checkup Sedation) -> Q1 (checkup_sedation)
        # PUB_G (Public General), CHK_G (Checkup General) -> Q2 (checkup_general)
        # OUT_S (Outpatient Sedation), INP_S (Inpatient Sedation) -> Q3 (other_sedation)
        # OUT_G (Outpatient General), INP_G (Inpatient General) -> Q4 (other_general)
        
        cats = [
            # Q1: Checkup Sedation (검수)
            Category(group_name="Dashboard", item_name="Public Sedation", group_code="GRID", metric_code="PUB_S", label_ko="공수", display_order=1),
            Category(group_name="Dashboard", item_name="Checkup Sedation", group_code="GRID", metric_code="CHK_S", label_ko="검수", display_order=2),
            
            # Q2: Checkup General (검일)
            Category(group_name="Dashboard", item_name="Public General", group_code="GRID", metric_code="PUB_G", label_ko="공일", display_order=3),
            Category(group_name="Dashboard", item_name="Checkup General", group_code="GRID", metric_code="CHK_G", label_ko="검일", display_order=4),
            
            # Q3: Other Sedation (외수/병수)
            Category(group_name="Dashboard", item_name="Outpatient Sedation", group_code="GRID", metric_code="OUT_S", label_ko="외수", display_order=5),
            Category(group_name="Dashboard", item_name="Inpatient Sedation", group_code="GRID", metric_code="INP_S", label_ko="병수", display_order=6),
            
            # Q4: Other General (외일/병일)
            Category(group_name="Dashboard", item_name="Outpatient General", group_code="GRID", metric_code="OUT_G", label_ko="외일", display_order=7),
            Category(group_name="Dashboard", item_name="Inpatient General", group_code="GRID", metric_code="INP_G", label_ko="병일", display_order=8),
            
            # Summary-only Categories
            Category(group_name="Procedure", item_name="ENDO Total",       group_code="PROC", metric_code="ENDO", label_ko="위내시경", display_order=10),
            Category(group_name="Procedure", item_name="Colon Total",      group_code="PROC", metric_code="COLON", label_ko="대장내시경", display_order=11),
        ]

        db.session.add_all(cats)
        db.session.commit()
        print("Seeding Complete.")

if __name__ == "__main__":
    seed_detailed()
