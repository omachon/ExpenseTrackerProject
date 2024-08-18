from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_user,logout_user,current_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from forms import CategoryForm
from models import Category, Expense, User
from app import db


auth = Blueprint('auth',__name__)


@auth.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form('email')
        password = request.form('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect details, try again!', category='error')
        else:
            flash('Email does not exist!', category='error')
    return render_template("login.html", user=current_user)

@auth.route("/logout")
@login_required
def logout():
    logout_user()
    flash('Logged out successfully!', category='info')
    return redirect(url_for('auth.login'))

@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form('email')
        first_name = request.form('first_name')
        password1 = request.form('password1')
        password2 = request.form('password2')

    user = User.query.filter_by(email=email).first()
    if user:
        flash('Email already exists!', category='error')
    elif len(email) < 4:
        flash('Email too short! Must be greater than three characters.', category='error')
    elif len(first_name) < 2:
        flash('First name is too short! Must be greater than two characters.', category='error')
    elif password1 != password2:
        flash('Passwords don\'t match.', category='error')
    elif len(password1) < 7:
        flash('Password too short!', category='error')
    else:
        new_user = User(email=email, first_name=first_name, password=generate_password_hash(
            password1, method='sha256'))
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user, remember=True)
        flash('Account created!', category='success')
        return redirect(url_for('views.home'))
    return render_template("sign_up.html", user=current_user)

@auth.route('/view', methods=['GET'])
@login_required
def viewExpense():
    expenses = Expense.query.filter_by(user_id=current_user.id).order_by(Expense.date.desc()).all()

    categories = Category.query.filter_by(user_id=current_user.id).all()
    expenses_by_category = {}
    for category in categories:
        expenses_by_category[category.name] = Expense.query.filter_by(user_id=current_user.id, category_id=category.id).all()
    
    return render_template('view.html', expenses=expenses)


@auth.route('/categories', methods=['GET', 'POST'])
@login_required
def manage_categories():
    form = CategoryForm()
    if form.validate_on_submit():
        category = Category(name=form.name.data, user_id=current_user.id)
        db.session.add(category)
        db.session.commit()
        flash('Category created successfully!', 'success')
        return redirect(url_for('manage_categories'))
    
    categories = Category.query.filter_by(user_id=current_user.id).all()
    return render_template('manage_categories.html', form=form, categories=categories)

@auth.route('/add-expense', methods=['GET', 'POST'])
@login_required
def add_expense():
    form = ExpenseForm()
    if form.validate_on_submit():
        new_expense = Expense(
            amount=form.amount.data,
            category=form.category.data,
            description=form.description.data,
            date=form.date.data,
            user_id=current_user.id
        )
        db.session.add(new_expense)
        db.session.commit()
        flash('Expense added successfully!', 'success')
        return redirect(url_for('view_expenses'))
    
    return render_template('add_expense.html', form=form)