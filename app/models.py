from datetime import datetime
from flask_login import UserMixin
from . import db, login_manager, bcrypt

class User(UserMixin, db.Model):
    __tablename__ = "users"
    user_id = db.Column(db.Integer, primary_key=True)
    login_id = db.Column(db.String(50), unique=True, nullable=False)
    name = db.Column(db.String(50), nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(10), default="user")
    is_active = db.Column(db.Integer, default=1)

    @property
    def is_admin(self):
        return self.role and self.role.lower() == 'admin'

    def get_id(self):
        return str(self.user_id)
    
    # We might need to verify how passwords are hashed in the legacy DB.
    # Assuming standard bcrypt for now, but if "armscii8_bin" implies something old, might be different.
    # User didn't specify, so assuming new app can control users or it uses compatible hash.
    def check_password(self, password: str) -> bool:
        return bcrypt.check_password_hash(self.password_hash, password)

    def set_password(self, password: str):
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class CodeGroup(db.Model):
    __tablename__ = 'code_groups'
    id = db.Column(db.Integer, primary_key=True)
    group_code = db.Column(db.String(50), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    
    codes = db.relationship('Code', backref='group', lazy=True)

class Code(db.Model):
    __tablename__ = 'codes'
    id = db.Column(db.Integer, primary_key=True)
    group_id = db.Column(db.Integer, db.ForeignKey('code_groups.id'), nullable=False)
    code = db.Column(db.String(50), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    display_order = db.Column(db.Integer, default=0)
    is_active = db.Column(db.Boolean, default=True)

class Doctor(db.Model):
    __tablename__ = "doctors"
    doctor_id = db.Column(db.Integer, primary_key=True)
    doctor_name = db.Column(db.String(200), nullable=False)
    # doctor_code column might be missing in legacy, but admin uses it. 
    # If legacy doesn't have it, we might adding it or aliasing.
    # But admin.py form writes to it. Assuming we should add the column definition.
    doctor_code = db.Column(db.String(50)) 
    department = db.Column(db.String(50))
    display_order = db.Column(db.Integer, default=0)
    is_active = db.Column(db.Integer, default=1)

class Category(db.Model):
    __tablename__ = "categories"
    category_id = db.Column(db.Integer, primary_key=True)
    category_code = db.Column(db.String(50))
    category_name = db.Column(db.String(50)) # Alias for item_name or separate? Admin uses category_name.
    # Existing model has group_name, item_name. Admin uses category_name. 
    # Let's map category_name to item_name if they are same, or add column. 
    # Admin form writes to category_name. Let's add the column.
    group_name = db.Column(db.String(50))
    item_name = db.Column(db.String(50))
    display_order = db.Column(db.Integer, default=0)
    is_active = db.Column(db.Integer, default=1)
    group_code = db.Column(db.String(20))
    metric_code = db.Column(db.String(20))
    label_ko = db.Column(db.String(50))

class ExamLog(db.Model):
    __tablename__ = "exam_logs"
    exam_id = db.Column(db.Integer, primary_key=True)
    exam_date = db.Column(db.String(10), nullable=False) # stored as string 'YYYY-MM-DD'
    doctor_id = db.Column(db.Integer, db.ForeignKey("doctors.doctor_id"), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey("categories.category_id"), nullable=False)
    created_by = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    action_type = db.Column(db.String(10)) # INSERT, DELETE

    doctor = db.relationship("Doctor", backref="logs")
    category = db.relationship("Category", backref="logs")
