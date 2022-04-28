from app import app, db, bcrypt
from flask import render_template, redirect, flash, url_for, request
from flask_login import current_user, login_user, logout_user
from app.forms import LoginForm, RegistrationForm
from app.models import User

# Home
#@app.route('/')
#def home():
#    user = -1
#    if current_user.is_authenticated:
#        user = current_user.get_id()
#    u = User.query.get(user)
#    return render_template('home.html', u=u)


# Employee views ---------------------------------------------------------------
# Projects list
@app.route('/')
@app.route('/e/projects')
def projects():
    user = -1
    if current_user.is_authenticated:
        user = current_user.get_id()
    u = User.query.get(user)
    return render_template('static/employee-project-list.html', u=u)

# Taskboard list
@app.route('/e/taskboard')
def taskboard():
    user = -1
    if current_user.is_authenticated:
        user = current_user.get_id()
    u = User.query.get(user)
    return render_template('static/employee-task-board.html', u=u)

# Single project
@app.route('/e/projects/p')
def project():
    user = -1
    if current_user.is_authenticated:
        user = current_user.get_id()
    u = User.query.get(user)
    return render_template('static/employee-project-view.html', u=u)

# Add new task
@app.route('/e/projects/p/addtask')
def addtask():
    user = -1
    if current_user.is_authenticated:
        user = current_user.get_id()
    u = User.query.get(user)
    return render_template('static/task-add.html', u=u)


# Login/registration -----------------------------------------------------------
@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(login=form.login.data, password=hashed_password, name=form.name.data, surname=form.surname.data,
                    role=form.role.data, active=True)
        db.session.add(user)
        db.session.commit()
        flash('Użytkownik utworzony', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(login=form.login.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Logowanie się nie powiodło', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))
