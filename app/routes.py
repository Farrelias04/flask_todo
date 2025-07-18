from flask import Blueprint, render_template, request, redirect
from .models import Task
from . import db

main = Blueprint('main', __name__)

@main.route("/")
def index():
    tasks = Task.query.all()
    return render_template("index.html", tasks=tasks)

@main.route("/add", methods=["POST"])
def add():
    task_content = request.form["content"]
    new_task = Task(content=task_content)
    db.session.add(new_task)
    db.session.commit()
    return redirect("/")

@main.route("/delete/<int:id>", methods=["GET", "POST"])
def delete(id):
    task = Task.query.get_or_404(id)
    db.session.delete(task)
    db.session.commit()
    return redirect("/")

@main.route("/edit/<int:id>", methods=["GET", "POST"])
def edit(id):
    task = Task.query.get_or_404(id)
    if request.method == "POST":
        task.content = request.form["content"]
        db.session.commit()
        return redirect("/")
    return render_template("edit.html", task=task)

@main.route("/toggle/<int:task_id>")
def toggle_task(task_id):
    task = Task.query.get_or_404(task_id)
    task.is_done = not task.is_done
    db.session.commit()
    return redirect("/")
