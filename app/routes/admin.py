from flask import Blueprint, flash, redirect, render_template, url_for
from flask_login import current_user, login_required
from ..forms import UserForm, CodeGroupForm, CodeForm, DoctorForm, CategoryForm
from ..models import (
    User,
    UserSession,
    CodeGroup,
    Code,
    Doctor,
    Category,
)
from .. import db

bp = Blueprint("admin", __name__, url_prefix="/admin")


def admin_required():
    if not current_user.is_authenticated or not current_user.is_admin:
        flash("관리자 권한이 필요합니다.", "danger")
        return False
    return True


@bp.before_request
def protect_admin():
    if not current_user.is_authenticated:
        return redirect(url_for("auth.login"))
    if not current_user.is_admin:
        flash("관리 메뉴에 접근할 수 없습니다.", "warning")
        return redirect(url_for("dashboard.index"))


@bp.route("/users")
@login_required
def users():
    users = User.query.order_by(User.created_at.desc()).all()
    return render_template("admin/users.html", users=users)


@bp.route("/users/new", methods=["GET", "POST"])
@login_required
def create_user():
    form = UserForm()
    if form.validate_on_submit():
        user = User(
            username=form.username.data,
            name=form.name.data,
            role=form.role.data,
            is_active=form.is_active.data,
        )
        if form.password.data:
            user.set_password(form.password.data)
        else:
            user.set_password("changeme")
        db.session.add(user)
        db.session.commit()
        flash("사용자를 추가했습니다.", "success")
        return redirect(url_for("admin.users"))
    return render_template("admin/user_form.html", form=form)


@bp.route("/users/<int:user_id>", methods=["GET", "POST"])
@login_required
def edit_user(user_id):
    user = User.query.get_or_404(user_id)
    form = UserForm(
        username=user.username,
        name=user.name,
        role=user.role,
        is_active=user.is_active,
    )
    if form.validate_on_submit():
        user.username = form.username.data
        user.name = form.name.data
        user.role = form.role.data
        user.is_active = form.is_active.data
        if form.password.data:
            user.set_password(form.password.data)
        db.session.commit()
        flash("사용자 정보를 저장했습니다.", "success")
        return redirect(url_for("admin.users"))
    return render_template("admin/user_form.html", form=form, user=user)


@bp.route("/users/<int:user_id>/reset")
@login_required
def reset_password(user_id):
    user = User.query.get_or_404(user_id)
    user.set_password("changeme")
    db.session.commit()
    flash("비밀번호를 초기화했습니다.", "info")
    return redirect(url_for("admin.users"))


@bp.route("/users/<int:user_id>/logout")
@login_required
def force_logout(user_id):
    UserSession.query.filter_by(user_id=user_id, is_active=True).update({"is_active": False})
    db.session.commit()
    flash("해당 사용자를 강제 로그아웃했습니다.", "info")
    return redirect(url_for("admin.users"))


@bp.route("/codes")
@login_required
def codes():
    groups = CodeGroup.query.order_by(CodeGroup.group_code).all()
    codes = Code.query.order_by(Code.display_order).all()
    return render_template("admin/codes.html", groups=groups, codes=codes)


@bp.route("/codes/groups/new", methods=["GET", "POST"])
@login_required
def create_code_group():
    form = CodeGroupForm()
    if form.validate_on_submit():
        group = CodeGroup(group_code=form.group_code.data, name=form.name.data)
        db.session.add(group)
        db.session.commit()
        flash("코드 그룹을 추가했습니다.", "success")
        return redirect(url_for("admin.codes"))
    return render_template("admin/code_group_form.html", form=form)


@bp.route("/codes/<int:group_id>/edit", methods=["GET", "POST"])
@login_required
def edit_code_group(group_id):
    group = CodeGroup.query.get_or_404(group_id)
    form = CodeGroupForm(group_code=group.group_code, name=group.name)
    if form.validate_on_submit():
        group.group_code = form.group_code.data
        group.name = form.name.data
        db.session.commit()
        flash("코드 그룹을 수정했습니다.", "success")
        return redirect(url_for("admin.codes"))
    return render_template("admin/code_group_form.html", form=form, group=group)


@bp.route("/codes/new", methods=["GET", "POST"])
@login_required
def create_code():
    form = CodeForm()
    form.group_id.choices = [(g.id, g.group_code) for g in CodeGroup.query.all()]
    if form.validate_on_submit():
        code = Code(
            group_id=form.group_id.data,
            code=form.code.data,
            name=form.name.data,
            display_order=form.display_order.data or 0,
            is_active=form.is_active.data,
        )
        db.session.add(code)
        db.session.commit()
        flash("코드를 추가했습니다.", "success")
        return redirect(url_for("admin.codes"))
    return render_template("admin/code_form.html", form=form)


@bp.route("/codes/<int:code_id>/edit", methods=["GET", "POST"])
@login_required
def edit_code(code_id):
    code = Code.query.get_or_404(code_id)
    form = CodeForm(
        group_id=code.group_id,
        code=code.code,
        name=code.name,
        display_order=code.display_order,
        is_active=code.is_active,
    )
    form.group_id.choices = [(g.id, g.group_code) for g in CodeGroup.query.all()]
    if form.validate_on_submit():
        code.group_id = form.group_id.data
        code.code = form.code.data
        code.name = form.name.data
        code.display_order = form.display_order.data or 0
        code.is_active = form.is_active.data
        db.session.commit()
        flash("코드를 수정했습니다.", "success")
        return redirect(url_for("admin.codes"))
    return render_template("admin/code_form.html", form=form, code=code)


@bp.route("/doctors")
@login_required
def doctors():
    doctors = Doctor.query.order_by(Doctor.display_order, Doctor.doctor_code).all()
    return render_template("admin/doctors.html", doctors=doctors)


@bp.route("/doctors/new", methods=["GET", "POST"])
@login_required
def create_doctor():
    form = DoctorForm()
    if form.validate_on_submit():
        doctor = Doctor(
            doctor_code=form.doctor_code.data,
            doctor_name=form.doctor_name.data,
            display_order=form.display_order.data or 0,
            is_active=form.is_active.data,
        )
        db.session.add(doctor)
        db.session.commit()
        flash("의사를 등록했습니다.", "success")
        return redirect(url_for("admin.doctors"))
    return render_template("admin/doctor_form.html", form=form)


@bp.route("/doctors/<int:doctor_id>/edit", methods=["GET", "POST"])
@login_required
def edit_doctor(doctor_id):
    doctor = Doctor.query.get_or_404(doctor_id)
    form = DoctorForm(
        doctor_code=doctor.doctor_code,
        doctor_name=doctor.doctor_name,
        display_order=doctor.display_order,
        is_active=doctor.is_active,
    )
    if form.validate_on_submit():
        doctor.doctor_code = form.doctor_code.data
        doctor.doctor_name = form.doctor_name.data
        doctor.display_order = form.display_order.data or 0
        doctor.is_active = form.is_active.data
        db.session.commit()
        flash("의사 정보를 수정했습니다.", "success")
        return redirect(url_for("admin.doctors"))
    return render_template("admin/doctor_form.html", form=form, doctor=doctor)


@bp.route("/categories")
@login_required
def categories():
    categories = Category.query.order_by(Category.display_order, Category.category_code).all()
    return render_template("admin/categories.html", categories=categories)


@bp.route("/categories/new", methods=["GET", "POST"])
@login_required
def create_category():
    form = CategoryForm()
    if form.validate_on_submit():
        category = Category(
            category_code=form.category_code.data,
            category_name=form.category_name.data,
            group_code=form.group_code.data,
            display_order=form.display_order.data or 0,
            is_active=form.is_active.data,
        )
        db.session.add(category)
        db.session.commit()
        flash("카테고리를 추가했습니다.", "success")
        return redirect(url_for("admin.categories"))
    return render_template("admin/category_form.html", form=form)


@bp.route("/categories/<int:category_id>/edit", methods=["GET", "POST"])
@login_required
def edit_category(category_id):
    category = Category.query.get_or_404(category_id)
    form = CategoryForm(
        category_code=category.category_code,
        category_name=category.category_name,
        group_code=category.group_code,
        display_order=category.display_order,
        is_active=category.is_active,
    )
    if form.validate_on_submit():
        category.category_code = form.category_code.data
        category.category_name = form.category_name.data
        category.group_code = form.group_code.data
        category.display_order = form.display_order.data or 0
        category.is_active = form.is_active.data
        db.session.commit()
        flash("카테고리를 수정했습니다.", "success")
        return redirect(url_for("admin.categories"))
    return render_template("admin/category_form.html", form=form, category=category)
