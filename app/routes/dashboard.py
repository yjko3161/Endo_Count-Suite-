from datetime import date, datetime, timedelta
from collections import defaultdict
from flask import Blueprint, render_template, flash
from flask_login import login_required, current_user
from ..forms import DashboardFilterForm
from ..models import ProcedureLog, Doctor, Code, CodeGroup

bp = Blueprint("dashboard", __name__)


def _resolve_dates(form: DashboardFilterForm):
    today = date.today()
    if form.period.data == "today":
        return today, today
    if form.period.data == "week":
        start = today - timedelta(days=today.weekday())
        end = start + timedelta(days=6)
        return start, end
    if form.period.data == "month":
        start = today.replace(day=1)
        if start.month == 12:
            next_month = start.replace(year=start.year + 1, month=1, day=1)
        else:
            next_month = start.replace(month=start.month + 1, day=1)
        end = next_month - timedelta(days=1)
        return start, end
    return form.start_date.data, form.end_date.data


def _aggregate(start, end):
    query = ProcedureLog.query.filter(
        ProcedureLog.exam_date >= start, ProcedureLog.exam_date <= end
    )
    records = query.all()
    matrix = defaultdict(lambda: defaultdict(lambda: defaultdict(int)))
    summary = defaultdict(int)
    for row in records:
        matrix[row.doctor_code][row.patient_group][row.procedure_type] += row.qty
        key = f"{row.procedure_type}:{row.sedation_type}"
        summary[key] += row.qty
        summary[row.procedure_type] += row.qty
        summary[f"{row.sedation_type}_total"] += row.qty
        summary[f"doctor_{row.doctor_code}_external"] += (
            row.qty if row.patient_group == "외수" else 0
        )
    summary["overall"] = summary.get("일반_total", 0) + summary.get("수면_total", 0)
    return matrix, summary


@bp.route("/")
@login_required
def index():
    form = DashboardFilterForm()
    start, end = _resolve_dates(form)
    matrix, summary = _aggregate(start, end)
    doctors = Doctor.query.filter_by(is_active=True).order_by(Doctor.display_order).all()
    patient_groups = (
        Code.query.join(Code.group)
        .filter(CodeGroup.group_code == "PATIENT_GROUP", Code.is_active == True)
        .order_by(Code.display_order)
        .all()
    )
    procedure_types = (
        Code.query.join(Code.group)
        .filter(CodeGroup.group_code == "PROCEDURE_TYPE", Code.is_active == True)
        .order_by(Code.display_order)
        .all()
    )
    return render_template(
        "dashboard.html",
        form=form,
        start=start,
        end=end,
        matrix=matrix,
        summary=summary,
        doctors=doctors,
        patient_groups=patient_groups,
        procedure_types=procedure_types,
    )


@bp.route("/dashboard", methods=["GET", "POST"])
@login_required
def dashboard_view():
    form = DashboardFilterForm()
    if form.validate_on_submit():
        start, end = _resolve_dates(form)
    else:
        start, end = _resolve_dates(form)
    matrix, summary = _aggregate(start, end)
    doctors = Doctor.query.filter_by(is_active=True).order_by(Doctor.display_order).all()
    patient_groups = (
        Code.query.join(Code.group)
        .filter(CodeGroup.group_code == "PATIENT_GROUP", Code.is_active == True)
        .order_by(Code.display_order)
        .all()
    )
    procedure_types = (
        Code.query.join(Code.group)
        .filter(CodeGroup.group_code == "PROCEDURE_TYPE", Code.is_active == True)
        .order_by(Code.display_order)
        .all()
    )
    return render_template(
        "dashboard.html",
        form=form,
        start=start,
        end=end,
        matrix=matrix,
        summary=summary,
        doctors=doctors,
        patient_groups=patient_groups,
        procedure_types=procedure_types,
    )
