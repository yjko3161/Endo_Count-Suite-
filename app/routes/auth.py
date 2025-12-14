from datetime import datetime
from flask import Blueprint, flash, redirect, render_template, request, session, url_for
from flask_login import current_user, login_required, login_user, logout_user
from ..forms import LoginForm
from ..models import User
from .. import db

bp = Blueprint("auth", __name__)


@bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("dashboard.index"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(login_id=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember.data)
            # Session management removed for legacy DB compatibility
            return redirect(url_for("dashboard.index"))
        else:
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
