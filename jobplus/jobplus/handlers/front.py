from flask import Blueprint, render_template, request, flash, url_for, redirect, current_app
from jobplus.models import User, CompanyDetail, db, Job
from jobplus.forms import UserRegisterForm, CompanyRegisterForm, LoginForm
from flask_login import login_user, login_required, logout_user

front = Blueprint('front', __name__)

@front.route('/')
def index():
    return render_template('index.html')

@front.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        login_user(user, form.remember_me.data)
        return redirect(url_for('.index'))
    return render_template('login.html', form=form)

@front.route('/logout')
@login_required
def logout():
    logout_user()
    flash('logout success', 'success')
    return redirect(url_for('.index'))

@front.route('/userregister', methods=['GET', 'POST'])
def userregister():
    form = UserRegisterForm()
    if form.validate_on_submit():
        form.create_user()
        flash('userregister success', 'success')
        return redirect(url_for('.login'))
    return render_template('userregister.html', form=form)

@front.route('/companyregister', methods=['GET', 'POST'])
def companyregister():
    form = CompanyRegisterForm()
    if form.validate_on_submit():
        form.create_company()
        flash('companyregister success', 'success')
        return redirect(url_for('.login'))
    return render_template('companyregister.html', form=form)
