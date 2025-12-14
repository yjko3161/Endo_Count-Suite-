from datetime import datetime
from flask import Blueprint, flash, redirect, render_template, request, session, url_for
from flask_login import current_user, login_required, login_user, logout_user
from ..forms import LoginForm
from ..models import User, UserSession
from .. import db

bp = Blueprint("auth", __name__)


def _set_active_session(user: User):
    active_session = UserSession.create_for_user(user.id)
    session["session_token"] = active_session.session_id
    user.last_login = datetime.utcnow()
    db.session.commit()


def _validate_session():
    if not current_user.is_authenticated:
        return
    session_token = session.get("session_token")
    if not session_token:
        logout_user()
        return redirect(url_for("auth.login"))
    active = UserSession.query.filter_by(
        user_id=current_user.id, session_id=session_token, is_active=True
    ).first()
    if not active:
        logout_user()
        session.clear()
        flash("다른 곳에서 로그인되어 종료되었습니다.", "warning")
        return redirect(url_for("auth.login"))
    active.last_seen = datetime.utcnow()
    db.session.commit()


@bp.before_app_request
def before_request():
    # enforce active session
    if current_user.is_authenticated:
        redirect_resp = _validate_session()
        if redirect_resp:
            return redirect_resp


@bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("dashboard.index"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if not user or not user.check_password(form.password.data):
            flash("아이디 또는 비밀번호가 올바르지 않습니다.", "danger")
            return render_template("login.html", form=form)
        if not user.is_active:
            flash("비활성 계정입니다. 관리자에게 문의하세요.", "warning")
            return render_template("login.html", form=form)
        login_user(user, remember=form.remember.data)
        _set_active_session(user)
        return redirect(url_for("dashboard.index"))
    return render_template("login.html", form=form)


@bp.route("/logout")
@login_required
def logout():
    session_token = session.get("session_token")
    if session_token:
        UserSession.query.filter_by(session_id=session_token).update({"is_active": False})
        db.session.commit()
    session.clear()
    logout_user()
    flash("로그아웃되었습니다.", "info")
    return redirect(url_for("auth.login"))
