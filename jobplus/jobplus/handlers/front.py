from flask import Blueprint, render_template, request
from jobplus.models import User, Company
from jobplus.forms import UserRegisterForm, CompanyRegisterForm, LoginForm
from flask_login import login_user, login_required, logout_user

front = Blueprint('front', __name__, profix='/')

@front.route('/')
def index():
    return render_template('index.html')

TODU
