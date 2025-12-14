from app import create_app, db
from app.models import CodeGroup, Code, Doctor, ProcedureLog
from datetime import date, timedelta
import random

app = create_app()

def seed():
    with app.app_context():
        # Clear existing data (optional, but good for clean slate)
        # db.drop_all()
        # db.create_all()
        # For now, just ensuring codes exist
        
        # 1. Code Groups
        groups = {
            "PATIENT_GROUP": "환자 구분",
            "SEDATION_TYPE": "진정 구분",
            "PROCEDURE_TYPE": "프로시저 구분"
        }
        
        group_objs = {}
        for code, name in groups.items():
            g = CodeGroup.query.filter_by(group_code=code).first()
            if not g:
                g = CodeGroup(group_code=code, name=name)
                db.session.add(g)
            group_objs[code] = g
        db.session.commit()
        
        # Refresh group objects
        for code in groups:
            group_objs[code] = CodeGroup.query.filter_by(group_code=code).first()

        # 2. Codes
        # Format: (Group, Code, Name, Order)
        initial_codes = [
            ("PATIENT_GROUP", "CHECKUP", "검진", 1),
            ("PATIENT_GROUP", "OUTPATIENT", "외래", 2),
            ("PATIENT_GROUP", "INPATIENT", "병동", 3),
            
            ("SEDATION_TYPE", "SEDATION", "수면", 1),
            ("SEDATION_TYPE", "GENERAL", "일반", 2),
            
            ("PROCEDURE_TYPE", "ENDO", "ENDO", 1),
            ("PROCEDURE_TYPE", "COLON", "colon", 2),
            ("PROCEDURE_TYPE", "ERCP", "ERCP", 3),
            ("PROCEDURE_TYPE", "PEG", "PEG", 4),
            ("PROCEDURE_TYPE", "C-ESD", "C-ESD", 5),
            ("PROCEDURE_TYPE", "G-ESD", "G-ESD", 6),
        ]

        for g_code, c_code, c_name, order in initial_codes:
            group = group_objs[g_code]
            c = Code.query.filter_by(group_id=group.id, code=c_code).first()
            if not c:
                c = Code(group_id=group.id, code=c_code, name=c_name, display_order=order)
                db.session.add(c)
        db.session.commit()

        # 3. Doctors
        doctors = ["M1", "M2", "M4", "M12", "FM1", "FM2", "FM3", "M30"]
        for idx, d_code in enumerate(doctors):
            d = Doctor.query.filter_by(doctor_code=d_code).first()
            if not d:
                d = Doctor(doctor_code=d_code, doctor_name=d_code, display_order=idx+1)
                db.session.add(d)
        db.session.commit()
        
        print("Codes and Doctors seeded.")

        # 4. Dummy Procedure Logs (Last 7 days)
        if ProcedureLog.query.count() == 0:
            print("Seeding dummy logs...")
            today = date.today()
            
            doc_objs = Doctor.query.all()
            p_codes = Code.query.join(Code.group).filter(CodeGroup.group_code=="PROCEDURE_TYPE").all()
            pt_codes = Code.query.join(Code.group).filter(CodeGroup.group_code=="PATIENT_GROUP").all()
            s_codes = Code.query.join(Code.group).filter(CodeGroup.group_code=="SEDATION_TYPE").all()

            for i in range(7):
                day = today - timedelta(days=i)
                for _ in range(20): # 20 logs per day random
                    log = ProcedureLog(
                        exam_date=day,
                        doctor_code=random.choice(doc_objs).doctor_code,
                        procedure_type=random.choice(p_codes).code,
                        patient_group=random.choice(pt_codes).code,
                        sedation_type=random.choice(s_codes).code,
                        qty=1
                    )
                    db.session.add(log)
            db.session.commit()
            print("Dummy logs seeded.")

if __name__ == "__main__":
    seed()
