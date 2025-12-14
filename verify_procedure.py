from app import create_app
from app.models import Doctor, Category, ExamLog, db
from app.routes.dashboard import _aggregate
from datetime import date

app = create_app()

def verify_procedure_flow():
    with app.app_context():
        # 1. Clean
        # db.session.query(ExamLog).delete()
        # db.session.commit()
        
        # 2. Add an Endo Checkup log
        doc = Doctor.query.first()
        # metric ENDO_PUB_S
        met_code = "ENDO_PUB_S"
        cat = Category.query.filter_by(metric_code=met_code).first()
        
        if not cat:
            print("Category ENDO_PUB_S not found!")
            return

        print(f"Adding log for {doc.doctor_name} - {met_code}")
        log = ExamLog(
            exam_date=date.today(),
            doctor_id=doc.doctor_id,
            category_id=cat.category_id,
            created_by=1,
            action_type='INSERT'
        )
        db.session.add(log)
        db.session.commit()
        
        # 3. Check Aggregation
        matrix, summary, dates = _aggregate(date.today(), date.today())
        
        # matrix['M1']['ENDO']['PUB_S'] should be >= 1
        val = matrix[doc.doctor_name]['ENDO']['PUB_S']
        print(f"Aggregated ENDO_PUB_S: {val}")
        
        if val >= 1:
            print("SUCCESS: Aggregation verified.")
        else:
            print("FAILURE: Aggregation returned 0.")

if __name__ == "__main__":
    verify_procedure_flow()
