
from flask import Flask, render_template, request, redirect

app = Flask(__name__)
tasks = []  # Temporary storage

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        task = request.form.get("task")
        if task:
            tasks.append(task)
        return redirect("/")  # Prevent form resubmission

    return render_template("index.html", tasks=tasks)

if __name__ == "__main__":
    app.run(debug=True)
