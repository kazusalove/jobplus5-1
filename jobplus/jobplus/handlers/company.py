from flask import Blueprint, render_template, flash, redirect, url_for, request
from flask_login import login_required, current_user
from jobplus.models import User
from jobplus.forms import CompanyProfileForm

company = Blueprint('company', __name__, url_prefix='/company')

@company.route('/profile/', methods=['GET', 'POST'])
@login_required
def profile():
    if not current_user.is_company:
        flash('you don\'t company user', 'warning')
        return redirect(url_for('front.index'))
    form = CompanyProfileForm(obj=current_user.company_detail)
    form.name.data = current_user.username
    form.email.data = current_user.email
    if form.validate_on_submit():
        form.updated_profile(current_user)
        flash('update company info success', 'success')
        return redirect(url_for('front.index'))
    return render_template('company/profile.html', form=form)
