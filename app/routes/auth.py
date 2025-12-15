from datetime import datetime, timedelta
from flask import Blueprint, flash, redirect, render_template, request, session, url_for
from flask_login import current_user, login_required, login_user, logout_user
from ..forms import LoginForm
from ..models import User, LoginAttempt
from .. import db

bp = Blueprint("auth", __name__)


@bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("dashboard.index"))

    # IP Blocking Check
    client_ip = request.remote_addr
    # Count failed attempts in last 15 minutes
    # Assuming timezone naive UTC for simplicity, or just match server time
    cutoff = datetime.utcnow() - timedelta(minutes=15)
    
    # We need to import LoginAttempt differently to avoid circle, or just assume it's available via models
    # But usually imports are at top. We will add imports in a separate edit or assume they are there.
    # Let's add imports in this chunk as well if possible, or just use models.LoginAttempt if imported
    
    recent_attempts = LoginAttempt.query.filter(
        LoginAttempt.ip_address == client_ip,
        LoginAttempt.attempt_time >= cutoff
    ).count()

    if recent_attempts >= 5:
        flash("로그인 시도 횟수를 초과했습니다. 잠시 후 다시 시도해주세요.", "danger")
        return render_template("login.html", form=LoginForm())

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(login_id=form.username.data).first()
        if user and user.check_password(form.password.data):
            # Login Success
            login_user(user, remember=form.remember.data)
            
            # Reset failed attempts on success
            LoginAttempt.query.filter_by(ip_address=client_ip).delete()
            db.session.commit()
            
            return redirect(url_for("dashboard.index"))
        else:
            # Login Failed
            db.session.add(LoginAttempt(ip_address=client_ip))
            db.session.commit()
            flash("아이디 또는 비밀번호가 올바르지 않습니다.", "danger")
            
    return render_template("login.html", form=form)


@bp.route("/logout")
@login_required
def logout():
    # session_token = session.get("session_token")
    # if session_token:
    #     UserSession.query.filter_by(session_id=session_token).update({"is_active": False})
    #     db.session.commit()
    session.clear()
    logout_user()
    flash("로그아웃되었습니다.", "info")
    return redirect(url_for("auth.login"))
