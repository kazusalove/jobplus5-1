from flask_wtf import FlaskForm
from jobplus.models import db, User, CompanyDetail
from wtforms import StringField, PasswordField, SubmitField, ValidationError, BooleanField, IntegerField, TextAreaField
from wtforms.validators import Required, Length, Email, EqualTo

class RegisterForm(FlaskForm):
    name = StringField('name', validators=[Required(), Length(3, 24)])
    email = StringField('email', validators=[Required(), Email()])
    password = PasswordField('Password', validators=[Required(), Length(6, 24)])
    repeat_password = PasswordField('Password again', validators=[Required(), EqualTo('password')])
    submit = SubmitField('Submit')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('name used')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('email used')

    def create_user(self):
        user = User(username=self.name.data, email=self.email.data, password=self.password.data)
        db.session.add(user)
        db.session.commit()
        return user

class UserProfileForm(FlaskForm):
    real_name = StringField('real name')
    email = StringField('Email', validators=[Required(), Email()])
    password = PasswordField('Password(default)')
    phone = StringField('phone number')
    work_years = IntegerField('work years')
    resume_url = StringField('resume url')
    submit = SubmitField('Submit')

    def validate_phone(self, field):
        phone = field.data
        if phone[:2] not in ('13', '15', '18') and len(phone) != 11:
            raise ValidationError('phone error')

    def updated_profile(self, user):
        user.real_name = self.real_name.data
        user.email = self.email.data
        if self.password.data:
            user.password = self.password.data
        user.phone = self.phone.data
        user.work_years = self.work_years.data
        user.resume_url = self.resume_url.data
        db.session.add(user)
        db.session.commit()

class CompanyProfileForm(FlaskForm):
    name = StringField('Company name')
    email = StringField('Email', validators=[Required(), Email()])
    password = PasswordField('Password(default)')
    slug = StringField('Slug', validators=[Required(), Length(3, 24)])
    location = StringField('address', validators=[Length(0, 64)])
    site = StringField('company index url', validators=[Length(0, 64)])
    logo = StringField('Logo')
    desc = StringField('short description', validators=[Length(0, 100)])
    about = TextAreaField('abour company info', validators=[Length(0, 1024)])
    submit = SubmitField('Submit')

    def validate_phone(self, field):
        if phone[:2] not in ('13', '15', '18') and len(phone) != 11:
            raise ValidationError('phone error')

    def updated_profile(self, user):
        user.name = self.name.data
        user.email = self.email.data
        if self.password.data:
            user.password = self.password.data

        if user.company_detail:
            company_detail = user.company_detail
        else:
            company_detail = CompanyDetail()
            company_detail.user_id = user.id
        self.populate_obj(company_detail)
        db.session.add(user)
        db.session.add(company_detail)
        db.session.commit()

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[Required(), Email()])
    password = PasswordField('Password', validators=[Required(), Length(6, 24)])
    remember_me = BooleanField('Remember me')
    submit = SubmitField('Submit')

    def validate_email(self, field):
        if field.data and not User.query.filter_by(email=field.data).first():
            raise ValidationError('email not register')

    def validate_password(self, field):
        user = User.query.filter_by(email=self.email.data).first()
        if user and not user.check_password(field.data):
            raise ValidationError('Password error')
