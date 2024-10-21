

from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configure the SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database
db = SQLAlchemy(app)

# Define a model for the To-Do List items
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(100), nullable=False)
    completed = db.Column(db.Boolean, default=False)

# Create the database and tables
with app.app_context():
    db.create_all()

# Home page route to show all tasks
@app.route('/')
def index():
    tasks = Todo.query.all()
    return render_template('index.html', tasks=tasks)

# Route to add a new task
@app.route('/add', methods=['POST'])
def add_task():
    task_content = request.form.get('task')
    if task_content:
        new_task = Todo(task=task_content)
        db.session.add(new_task)
        db.session.commit()
    return redirect(url_for('index'))

# Route to delete a task
@app.route('/delete/<int:task_id>')
def delete_task(task_id):
    task_to_delete = Todo.query.get(task_id)
    if task_to_delete:
        db.session.delete(task_to_delete)
        db.session.commit()
    return redirect(url_for('index'))

# Route to update a task
@app.route('/update/<int:task_id>', methods=['GET', 'POST'])
def update_task(task_id):
    task = Todo.query.get(task_id)
    if request.method == 'POST':
        task_content = request.form.get('task')
        if task_content:
            task.task = task_content
            db.session.commit()
            return redirect(url_for('index'))
    return render_template('update.html', task=task)

# Route to mark a task as completed or pending
@app.route('/complete/<int:task_id>')
def complete_task(task_id):
    task = Todo.query.get(task_id)
    if task:
        task.completed = not task.completed  # Toggle the completed status
        db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
