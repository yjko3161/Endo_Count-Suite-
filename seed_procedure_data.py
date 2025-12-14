from app import create_app
from app.models import db, Category
from sqlalchemy import text

app = create_app()

def seed_procedures():
    with app.app_context():
        print("Truncating Exam Logs and Categories...")
        db.session.execute(text("SET FOREIGN_KEY_CHECKS = 0"))
        db.session.execute(text("TRUNCATE TABLE exam_logs"))
        db.session.execute(text("TRUNCATE TABLE categories"))
        db.session.execute(text("SET FOREIGN_KEY_CHECKS = 1"))
        db.session.commit()

        print("Seeding Procedure Categories...")
        
        procedures = [
            ('ENDO', 'Endo'),
            ('COLON', 'Colon'),
            ('ERCP', 'ERCP'),
            ('PEG', 'PEG'),
            ('CESD', 'C-ESD'),
            ('GESD', 'G-ESD')
        ]
        
        # 8 Metrics per procedure
        # Suffix -> Label Mapping
        metrics = [
            # Checkup Row
            ('PUB_S', '공수'),
            ('CHK_S', '검수'),
            ('PUB_G', '공일'),
            ('CHK_G', '검일'),
            # Other Row
            ('OUT_S', '외수'),
            ('INP_S', '병수'),
            ('OUT_G', '외일'),
            ('INP_G', '병일'),
        ]

        cats = []
        global_order = 1
        
        for proc_code, proc_name in procedures:
            for met_code, met_label in metrics:
                # metric_code example: "ENDO_PUB_S"
                full_code = f"{proc_code}_{met_code}"
                
                cat = Category(
                    group_name="Dashboard",
                    item_name=f"{proc_name} {met_label}",
                    group_code=proc_code, # Use group_code to identify column
                    metric_code=full_code,
                    label_ko=met_label,
                    display_order=global_order
                )
                cats.append(cat)
                global_order += 1

        db.session.add_all(cats)
        db.session.commit()
        print(f"Seeding Complete. {len(cats)} categories created.")

if __name__ == "__main__":
    seed_procedures()
