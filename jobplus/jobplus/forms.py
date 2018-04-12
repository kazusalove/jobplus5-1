from flask_wtf import FlaskForm
from jobplus.models import db, User, Company
from wtforms import StringField, PasswordField, SubmitField, ValidationError, BooleanField
from wtforms.validators import Required, Length, Email, EqualTo

class UserRegisterForm(FlaskForm):
    username = StringField('Username', validators=[Required(), Length(3, 24)])
    email = StringField('Email', validators=[Required(), Email()])
    password = PasswordField('Password', validators=[Required(), Length(6, 24)])
    repeat_password = PasswordField('Password again', validators=[Required(), EqualTo('password')])
    submit = SubmitField('Submit')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('username used')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('email used')

    def create_user(self):
        user = User()
        user.username = self.username.data
        user.email = self.email.data
        user.password = self.password.data
        db.session.add(user)
        db.session.commit()
        return user


class CompanyRegisterForm(FlaskForm):
    company = StringField('Company name', validators=[Required(), Length(3, 24)])
    email = StringField('Email', validators=[Required(), Email()])
    password = PasswordField('Password', validators=[Required(), Length(6, 24)])
    repeat_password = PasswordField('Password again', validators=[Required(), EqualTo('password')])
    submit = SubmitField('Submit')

    def validate_company(self, field):
        if Company.query.filter_by(company=field.data).first():
            raise ValidationError('company name used')

    def validate_email(self, field):
        if Company.query.filter_by(email=field.data).first():
            raise ValidationError('email used')

    def create_user(self):
        company = Company()
        company.company = self.company.data
        company.email = self.email.data
        company.password = self.password.data
        db.session.add(company)
        db.session.commit()
        return company

class LoginForm(FlaskForm):
    email = StringField('Email', Validators=[Required(), Email()])
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
