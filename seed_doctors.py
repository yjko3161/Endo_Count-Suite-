from app import create_app
from app.models import db, Doctor
from sqlalchemy import text

app = create_app()

def seed_doctors():
    with app.app_context():
        print("Truncating Exam Logs and Doctors...")
        db.session.execute(text("SET FOREIGN_KEY_CHECKS = 0"))
        # Must truncate logs as they depend on doctor_id (unless cascading, but safer to truncate)
        db.session.execute(text("TRUNCATE TABLE exam_logs")) 
        db.session.execute(text("TRUNCATE TABLE doctors"))
        db.session.execute(text("SET FOREIGN_KEY_CHECKS = 1"))
        db.session.commit()

        print("Seeding Doctors in specific order...")
        
        # User defined order: M1, M2, M4, M12, FM2, FM3, FM1, M30
        doctor_names = ['M1', 'M2', 'M4', 'M12', 'FM2', 'FM3', 'FM1', 'M30']
        
        doctors = []
        for name in doctor_names:
            doc = Doctor(
                doctor_name=name,
                is_active=True
                # other fields default or nullable
            )
            doctors.append(doc)
            
        db.session.add_all(doctors)
        db.session.commit()
        print(f"Seeded {len(doctors)} doctors.")

if __name__ == "__main__":
    seed_doctors()
