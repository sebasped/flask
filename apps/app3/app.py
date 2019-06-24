from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///test.db' # tres barras es relativo, cuatro es absoluto
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Task %r>' % self.id

@app.route('/', methods=['POST','GET'])
def index():
    if request.method == 'POST':
        task_content = request.form['content']
        new_task = Todo(content=task_content)
        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue agregando la tarea'
        # return 'Hola'
    else:
        tasks = Todo.query.order_by(Todo.date_created).all()
    # return "Hola mundo"
    return render_template('index.html', tasks=tasks)


@app.route('/delete/<int:id>')
def delete(id):
    task_a_borrar = Todo.query.get_or_404(id)
    try:
        db.session.delete(task_a_borrar)
        db.session.commit()
        return redirect('/')
    except:
        return 'No se pudo borrar la tarea'

@app.route('/update/<int:id>', methods=['POST','GET'])
def update(id):
    return ''


if __name__ == "__main__":
    app.run(debug=True)
