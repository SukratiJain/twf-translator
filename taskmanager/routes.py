from flask import render_template, request, redirect, url_for, flash, redirect, jsonify
from taskmanager import app, db, bcrypt
from taskmanager.forms import RegistrationForm, LoginForm, TaskForm
from taskmanager.models import User, Task, load_user
from flask_login import login_user, current_user, logout_user, login_required
from datetime import datetime
from googletrans import Translator

tasks = [
    {
        "id": 1,
        "title": "Knowledge | Personal",
        "description": "5 vocabulary words."
    },
    {
        "id": 2,
        "title": "Health",
        "description": "15 min exercise."
    }
]

@app.route("/home")
def home():
    return render_template('home.html')


@app.route('/translate', methods=["POST"])
def translate():
    text = request.json['text']
    translator = Translator()
    translated = translator.translate(text, dest='fr')
    print(translated, "---------------------------------")
    return jsonify({"translation": translated.text})


@app.route("/dashboard")
@login_required
def dashboard():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    tasks = Task.query.filter_by(user_id=current_user.id).all()
    form = TaskForm()
    return render_template('dashboard.html', tasks=tasks, form=form)

@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(first_name=form.first_name.data, last_name=form.last_name.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template("register.html", form=form, title="Register")


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('dashboard'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)



@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('dashboard'))

"""
@app.route('/tasks', methods=['GET', 'POST'])
def manage_tasks():
    if request.method == 'GET':
        tasks = Task.query.filter_by(user_id=current_user.id).all()
        task_data = [{"id": task.id, "title": task.title, "description": task.description, "status": task.status, "due_date": task.due_date, "created_date": task.created_date, "priority": task.priority} for task in tasks]
        return jsonify(task_data)
    elif request.method == 'POST':
        form = TaskForm()
        for k,v in request.form.items():
            print(k,v)
        if form.validate_on_submit():
            data = request.form
            new_task = Task(
                            title=form.title.data, 
                            description=form.description.data, 
                            status=form.status.data, 
                            due_date=form.due_date.data, 
                            created_date=datetime.now(), 
                            priority=form.priority.data, 
                            user_id=current_user.id
                        )
            # new_task = Task(title=data.get('title'), description=data.get('description'), status=data.get('status'), due_date=datetime.strptime(data.get('due_date'), '%Y-%m-%d').date(), created_date=datetime.now(), priority=data.get('priority'), user_id=current_user.id)
            db.session.add(new_task)
            db.session.commit()
            return jsonify({"success": True})

    else:
        return jsonify({"error": "Method not allowed"}), 405

@app.route("/task/<int:task_id>/update", methods=['GET', 'POST'])
@login_required
def update_task(task_id):
    task = Task.query.get_or_404(task_id)
    if task.user_id != current_user.id:
        return jsonify({"error": "You are not authorized to perform this action"}), 403
    form = TaskForm()
    if form.validate_on_submit():
        task.title = form.title.data
        task.content = form.content.data
        db.session.commit()
        flash('Your task has been updated!', 'success')
        return redirect(url_for('task', task_id=task.id))


@app.route('/tasks/<int:task_id>', methods=['PUT', 'DELETE'])
def manage_task(task_id):
    task = Task.query.get_or_404(task_id)
    if task.user_id != current_user.id:
        return jsonify({"error": "You are not authorized to perform this action"}), 403
    if request.method == 'PUT':
        data = request.form
        task.title = data.get('title')
        task.description = data.get('description')
        task.status = data.get('status')
        task.due_date = data.get('due_date')
        task.priority = data.get('priority')
        db.session.commit()
        return jsonify({"success": True})
    elif request.method == 'DELETE':
        db.session.delete(task)
        db.session.commit()
        return jsonify({"success": True})
    else:
        return jsonify({"error": "Method not allowed"}), 405

"""
