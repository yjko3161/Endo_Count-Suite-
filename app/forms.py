from datetime import date
from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    PasswordField,
    BooleanField,
    SubmitField,
    SelectField,
    IntegerField,
    DateField,
)
from wtforms.validators import DataRequired, Length


class LoginForm(FlaskForm):
    username = StringField("아이디", validators=[DataRequired(), Length(max=64)])
    password = PasswordField("비밀번호", validators=[DataRequired()])
    remember = BooleanField("로그인 유지")
    submit = SubmitField("로그인")


class UserForm(FlaskForm):
    username = StringField("로그인ID", validators=[DataRequired(), Length(max=64)])
    name = StringField("이름", validators=[DataRequired(), Length(max=120)])
    role = SelectField("권한", choices=[("Admin", "Admin"), ("User", "User")])
    is_active = BooleanField("활성")
    password = PasswordField("비밀번호 (신규/변경 시)")
    submit = SubmitField("저장")


class CodeGroupForm(FlaskForm):
    group_code = StringField("코드그룹", validators=[DataRequired(), Length(max=64)])
    name = StringField("이름", validators=[DataRequired(), Length(max=120)])
    submit = SubmitField("저장")


class CodeForm(FlaskForm):
    group_id = SelectField("코드그룹", coerce=int, validators=[DataRequired()])
    code = StringField("코드", validators=[DataRequired(), Length(max=64)])
    name = StringField("이름", validators=[DataRequired(), Length(max=120)])
    display_order = IntegerField("표시순서", default=0)
    is_active = BooleanField("활성")
    submit = SubmitField("저장")


class DoctorForm(FlaskForm):
    doctor_code = StringField("의사코드", validators=[DataRequired(), Length(max=32)])
    doctor_name = StringField("이름", validators=[DataRequired(), Length(max=120)])
    display_order = IntegerField("표시순서", default=0)
    is_active = BooleanField("활성")
    submit = SubmitField("저장")


class CategoryForm(FlaskForm):
    category_code = StringField("카테고리코드", validators=[DataRequired(), Length(max=64)])
    category_name = StringField("이름", validators=[DataRequired(), Length(max=120)])
    group_code = StringField("그룹코드", validators=[DataRequired(), Length(max=64)])
    display_order = IntegerField("표시순서", default=0)
    is_active = BooleanField("활성")
    submit = SubmitField("저장")


class DashboardFilterForm(FlaskForm):
    period = SelectField(
        "기간",
        choices=[
            ("today", "오늘"),
            ("week", "이번주"),
            ("month", "이번달"),
            ("custom", "사용자 지정"),
        ],
        default="today",
    )
    start_date = DateField("시작", default=date.today)
    end_date = DateField("종료", default=date.today)
    submit = SubmitField("조회")
