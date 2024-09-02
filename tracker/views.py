from flask import Blueprint, render_template, request, flash, url_for, redirect
from flask_login import login_required, current_user, logout_user
from werkzeug.security import check_password_hash
from .models import User, Transanction
from . import db

views = Blueprint('views', __name__)

@views.route("/home")
def home():
    return render_template('home.html')


@views.route("/dashboard")
@login_required
def dashboard():
    transanctions = Transanction.query.filter(Transanction.user_id==current_user.id)
    if transanctions.count() > 0:
        return render_template('dashboard.html', user=current_user, transanctions=transanctions)
    else:
        return render_template('dashboard.html', user=current_user)

@views.route("/welcome")
@login_required
def welcome():
    return "<h1>Hello user</h1>"

@views.route('delete-account/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_user_account(id: int):
    if request.method == 'POST':
        password = request.form.get('password')

        # validate password
        if check_password_hash(current_user.password_hash, password) != True:
            flash('Invalid password, not allowed to delete this account!', category='error')
        else:
            user = User.query.get(current_user.id)
            db.session.delete(user)
            db.session.commit()
            flash('User account deleted!', category='success')
            logout_user()
        return redirect(url_for('views.home'))
    return render_template('delete_account.html', user=current_user)