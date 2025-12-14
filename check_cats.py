from app import create_app
from app.models import Category, db

app = create_app()
with app.app_context():
    cats = Category.query.filter(Category.metric_code.like('%_PUB_S%')).all()
    print("Existing PUB_S categories:")
    for c in cats:
        print(c.metric_code)
