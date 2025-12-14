from app import create_app
from app.models import Category, db

app = create_app()

metrics = {
    'PUB_S': '공수', 
    'CHK_S': '검수', 
    'PUB_G': '공일', 
    'CHK_G': '검일',
    'OUT_S': '외수', 
    'INP_S': '병수', 
    'OUT_G': '외일', 
    'INP_G': '병일'
}

with app.app_context():
    print("Seeding SIG categories (Retry)...")
    for suffix, label in metrics.items():
        code = f"SIG_{suffix}"
        if not Category.query.filter_by(metric_code=code).first():
            # Schema: group_name, item_name, group_code, metric_code, label_ko
            new_cat = Category(
                group_name='SIG',
                item_name=code,
                group_code='SIG',
                metric_code=code,
                label_ko=label,
                display_order=1
            )
            db.session.add(new_cat)
            print(f"Added {code}")
        else:
            print(f"Skipped {code} (exists)")
            
    db.session.commit()
    print("Done.")
