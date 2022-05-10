from flask import Blueprint
from flask import render_template, flash, redirect, url_for, abort
from flask import request
from flask_login import current_user, login_required, login_user, logout_user

from app.consts import INVALID_CREDENTIALS_MESSAGE, LOG_IN_MESSAGE, LOG_OUT_MESSAGE, TASK_CREATED_MESSAGE, TASK_DELETED_MESSAGE, TASK_UPDATED_MESSAGE, USER_CREATED_MESSAGE

from .forms import LoginForm, RegisterForm, TaskForm
from .models import User, Task
from . import login_manager
from .email import welcome_mail

page = Blueprint('page', __name__)


@login_manager.user_loader
def load_user(id):
    return User.get_by_id(id)


@page.route("/")
def index():
    return render_template('index.html', title="Index", active="index")


@page.app_errorhandler(404)
def page_not_found(error):
    return render_template("errors/404.html"), 404


@page.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for(".tasks"))

    form = LoginForm(request.form)

    if request.method == "POST" and form.validate():

        user = User.get_by_username(form.username.data)

        if user and user.verify_password(form.password.data):
            login_user(user)
            flash(LOG_IN_MESSAGE)
            print("Nueva sesión creada")
            print(form.username.data)
            print(form.password.data)
            return redirect(url_for(".tasks"))
        else:
            flash(INVALID_CREDENTIALS_MESSAGE, "error")

    return render_template("auth/login.html", title="Login", form=form, active="login")


@page.route("/logout")
def logout():
    logout_user()
    flash(LOG_OUT_MESSAGE)
    return redirect(url_for(".login"))


@page.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for(".tasks"))

    form = RegisterForm(request.form)

    if request.method == "POST" and form.validate():
        user = User.create_element(
            username=form.username.data, password=form.password.data, email=form.email.data)
        flash(USER_CREATED_MESSAGE)
        print(f"{USER_CREATED_MESSAGE}. User id: {user.id}")
        welcome_mail(user)
        login_user(user)
        return redirect(url_for(".tasks"))

    return render_template("auth/register.html", title="Register", form=form, active="register")


@page.route("/tasks")
@page.route("/tasks/<int:page>")
@login_required
def tasks(page=1, per_page=2):
    pagination = current_user.tasks.paginate(page, per_page=per_page)

    tasks_list = pagination.items

    return render_template("tasks/list.html", title="Tasks", tasks_list=tasks_list, pagination=pagination, page=page, active="tasks")


@page.route("/tasks/show/<int:task_id>")
@login_required
def get_task(task_id):
    task = Task.query.get_or_404(task_id)

    return render_template("tasks/show.html", title=f"Tarea {task_id}", task=task)


@page.route("/tasks/new", methods=["GET", "POST"])
@login_required
def new_task():
    form = TaskForm(request.form)

    if request.method == "POST" and form.validate():
        task = Task.create_element(
            title=form.title.data, description=form.description.data, user_id=current_user.id)
        if task:
            flash(TASK_CREATED_MESSAGE)
            return redirect(url_for(".tasks"))

    return render_template("tasks/new.html", title="New Task", form=form, active="new_task")


@page.route("/tasks/edit/<int:task_id>", methods=["GET", "POST"])
@login_required
def edit_task(task_id):
    task = Task.query.get_or_404(task_id)

    if task.user_id != current_user.id:
        abort(404)

    form = TaskForm(request.form, obj=task)

    if request.method == "POST" and form.validate():
        task = Task.update_element(
            task_id, form.title.data, form.description.data)
        if task:
            flash(TASK_UPDATED_MESSAGE)
            return redirect(url_for(".tasks"))

    return render_template("tasks/edit.html", title="Edit Task", form=form)


@page.route("/tasks/delete/<int:task_id>", methods=["GET", "POST"])
@login_required
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)

    if task.user_id != current_user.id:
        abort(404)

    if Task.delete_element(task.id):
        flash(TASK_DELETED_MESSAGE)

    return redirect(url_for(".tasks"))
