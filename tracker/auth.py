from flask import Blueprint, request, redirect, flash, render_template, url_for
from. import db
from flask_login import login_user, login_required, logout_user, current_user
from .models import User
from datetime import timedelta
from werkzeug.security import generate_password_hash, check_password_hash

auth = Blueprint("auth", __name__)

@auth.route("signup", methods=["GET", "POST"])
def signup():
    TEMPLATE = 'auth/signup.html'
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')

        if len(username) < 5 or len(email) < 6 or len(password) < 4:
            flash('Invalid credentials', category='error')
            return render_template(TEMPLATE, username=username, email=email, password=password)
        

        new_user = User(username=username, email=email, password_hash=generate_password_hash(password, 'scrypt', 10))
        db.session.add(new_user)
        try:
            db.session.commit()
        except:
            flash("Invalid credentials, email and username must be unique!", category='error')
            return render_template(TEMPLATE, username=username, email=email, password=password)

        flash("User created successfully", category='success')
        return redirect(url_for('auth.signin'))
    return render_template(TEMPLATE)

@auth.route('signin', methods=['GET', 'POST'])
def signin():
    TEMPLATE = 'auth/signin.html'
    if request.method == 'POST':
        user = request.form.get('user')
        password = request.form.get('password')
        remember_me: bool = request.form.get('remember_me')

        if User.query.filter(User.username==user).first() != None:
            # get user if user == username
            found_user = User.query.filter(User.username==user).first()
        elif User.query.filter(User.email==user).first() != None:
            # get user if user == email
            found_user = User.query.filter(User.email==user).first()
        else:
            flash("Invalid credentials, user does not exist", category='error')
            return render_template(TEMPLATE, user=user, password=password)
        
        # check password
        if check_password_hash(found_user.password_hash, password) != True:
            flash("Invalid password", category='error')
            return render_template(TEMPLATE, user=user, password=password)
            
        login_user(found_user, remember=remember_me, duration=timedelta(minutes=2))
        flash("User logged in successfully!", category='success')
        return redirect(request.args.get('next')) if request.args.get('next') else redirect(url_for('views.dashboard'))
        
    return render_template(TEMPLATE)
    

@auth.route('logout', methods=['GET', 'POST'])
@login_required 
def logout_view():
    if request.method == 'GET':
        return redirect(url_for('views.home'))

    # if not current_user or current_user == None:
    #     return redirect(url_for('views.home'))
    
    logout_user()
    return redirect(url_for('auth.signin'))