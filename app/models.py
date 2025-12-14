from datetime import datetime
import uuid
from flask_login import UserMixin
from . import db, login_manager, bcrypt


class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    name = db.Column(db.String(120), nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(10), default="User")
    is_active = db.Column(db.Boolean, default=True)
    last_login = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    sessions = db.relationship("UserSession", backref="user", lazy=True)

    def set_password(self, password: str) -> None:
        self.password_hash = bcrypt.generate_password_hash(password).decode("utf-8")

    def check_password(self, password: str) -> bool:
        return bcrypt.check_password_hash(self.password_hash, password)

    @property
    def is_admin(self) -> bool:
        return self.role.lower() == "admin"

    def get_id(self):
        return str(self.id)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class UserSession(db.Model):
    __tablename__ = "user_sessions"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    session_id = db.Column(db.String(64), unique=True, nullable=False)
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)

    @staticmethod
    def create_for_user(user_id: int) -> "UserSession":
        UserSession.query.filter_by(user_id=user_id, is_active=True).update(
            {"is_active": False}
        )
        session = UserSession(
            user_id=user_id,
            session_id=uuid.uuid4().hex,
            last_seen=datetime.utcnow(),
            is_active=True,
        )
        db.session.add(session)
        db.session.commit()
        return session


class CodeGroup(db.Model):
    __tablename__ = "code_groups"
    id = db.Column(db.Integer, primary_key=True)
    group_code = db.Column(db.String(64), unique=True, nullable=False)
    name = db.Column(db.String(120), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    codes = db.relationship("Code", backref="group", lazy=True)


class Code(db.Model):
    __tablename__ = "codes"
    id = db.Column(db.Integer, primary_key=True)
    group_id = db.Column(db.Integer, db.ForeignKey("code_groups.id"), nullable=False)
    code = db.Column(db.String(64), nullable=False)
    name = db.Column(db.String(120), nullable=False)
    display_order = db.Column(db.Integer, default=0)
    is_active = db.Column(db.Boolean, default=True)


class Doctor(db.Model):
    __tablename__ = "doctors"
    id = db.Column(db.Integer, primary_key=True)
    doctor_code = db.Column(db.String(32), unique=True, nullable=False)
    doctor_name = db.Column(db.String(120), nullable=False)
    display_order = db.Column(db.Integer, default=0)
    is_active = db.Column(db.Boolean, default=True)


class Category(db.Model):
    __tablename__ = "categories"
    id = db.Column(db.Integer, primary_key=True)
    category_code = db.Column(db.String(64), unique=True, nullable=False)
    category_name = db.Column(db.String(120), nullable=False)
    group_code = db.Column(db.String(64), nullable=False)
    display_order = db.Column(db.Integer, default=0)
    is_active = db.Column(db.Boolean, default=True)


class ProcedureLog(db.Model):
    __tablename__ = "procedure_logs"
    id = db.Column(db.Integer, primary_key=True)
    exam_date = db.Column(db.Date, nullable=False)
    doctor_code = db.Column(db.String(32), nullable=False)
    procedure_type = db.Column(db.String(64), nullable=False)
    patient_group = db.Column(db.String(64), nullable=False)
    sedation_type = db.Column(db.String(64), nullable=False)
    qty = db.Column(db.Integer, default=1)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


# utility helpers

def ensure_admin_exists():
    admin = User.query.filter_by(username="admin").first()
    if not admin:
        admin = User(username="admin", name="Administrator", role="Admin")
        admin.set_password("admin1234")
        db.session.add(admin)
        db.session.commit()
    return admin
