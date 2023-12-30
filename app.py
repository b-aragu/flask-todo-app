from flask import Flask, render_template, request, redirect
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# configure database URI (uniform resource allocator)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'

# creating a SQLAlchemy instance and associating it with flask app 
db =  SQLAlchemy(app)

#creating a class named todo that represents table in database
class todo(db.Model):
    # defines colum of the 'todo' table
    id  = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Integer, default=0)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Task %r>' % self.id

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        task_content = request.form['content']
        new_task = todo(content=task_content)

        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue adding tasks'
    else:
        tasks = todo.query.order_by(todo.date_created).all()
        return render_template('index.html', tasks = tasks)
@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = todo.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was a problem reading that task'

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    task = todo.query.get_or_404(id)

    if request.method == 'POST':
        task.content = request.form['content']

        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'issue updating task'

    else:
        return render_template('update.html', task=task)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    app.run(debug=True)
