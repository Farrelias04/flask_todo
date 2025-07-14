
from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# Setup the database
basedir = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(basedir, 'todo.db')
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Define a Task model
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f'<Task {self.id}: {self.content}>'

# Create the database (only once)
with app.app_context():
    db.create_all()

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        task_content = request.form.get("task")
        if task_content:
            new_task = Task(content=task_content)
            db.session.add(new_task)
            db.session.commit()
        return redirect("/")
    
    tasks = Task.query.all()
    return render_template("index.html", tasks=tasks)

@app.route("/delete/<int:id>", methods=["POST"])
def delete(id):
    task_to_delete = Task.query.get_or_404(id)
    db.session.delete(task_to_delete)
    db.session.commit()
    return redirect("/")

@app.route("/complete/<int:id>", methods=["POST"])
def complete(id):
    task = Task.query.get_or_404(id)
    task.completed = not task.completed # Toggle status
    db.session.commit()
    return redirect("/")

@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit(id):
    task = Task.query.get_or_404(id)

    if request.method == "POST":
        task.content = request.form['content']
        db.session.commit()
        return redirect("/")
    
    return render_template("edit.html", task=task) 

if __name__ == "__main__":
    app.run(debug=True)
