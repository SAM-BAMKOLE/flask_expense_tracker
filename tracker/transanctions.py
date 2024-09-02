from flask import Blueprint, request, redirect, render_template, flash, url_for
from flask_login import current_user, login_required
from .models import Transanction
from . import db

transanctions = Blueprint('transanctions', __name__)

@transanctions.route("/create", methods=['GET', 'POST'])
@login_required
def create():
    if request.method == 'POST':
        amount = request.form.get('amount')
        type = request.form.get('type')
        description = request.form.get('description')
        category = request.form.get('category')

        transanction = Transanction(amount=amount, type=type, description=description, category=category, user_id=current_user.id)
        
        db.session.add(transanction)
        db.session.commit()

        flash('Transanction added', category='success')
        return render_template('transanctions/create.html')
    return render_template('transanctions/create.html')

@transanctions.route('delete-all')
def delete_all():
    transanction = Transanction.query.get(1)
    db.session.delete(transanction)
    db.session.commit()
    return redirect(url_for('views.dashboard'))