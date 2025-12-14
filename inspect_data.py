from app import create_app, db
from app.models import ProcedureLog, Code, CodeGroup
from sqlalchemy import func

app = create_app()

with app.app_context():
    print("--- Distinct Patient Groups ---")
    groups = db.session.query(ProcedureLog.patient_group).distinct().all()
    for g in groups:
        print(g[0])

    print("\n--- Distinct Sedation Types ---")
    sedations = db.session.query(ProcedureLog.sedation_type).distinct().all()
    for s in sedations:
        print(s[0])
    
    print("\n--- Distinct Procedure Types ---")
    procs = db.session.query(ProcedureLog.procedure_type).distinct().all()
    for p in procs:
        print(p[0])

    print("\n--- Code Groups (Reference) ---")
    # Check what codes exist
    codes = Code.query.all()
    for c in codes:
        print(f"{c.group.group_code}: {c.code} ({c.name})")
