from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = 'SECRET_KEY'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
db = SQLAlchemy(app)
    

class Users(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(100))
    password = db.Column(db.String(100))
    tasks = db.relationship('Tasks', backref='user')

class Tasks(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    task_name = db.Column(db.String(100))
    status = db.Column(db.Boolean)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))


@app.route("/", methods=['GET', 'POST']) 
def index():
    if request.method == 'POST':
        if request.form['submit'] == 'Add Task':
            task_name = request.form['task_name']
            user = Users.query.filter_by(username=session['username']).first()
            task = Tasks(task_name=task_name, status=False, user=user)
            db.session.add(task)
            db.session.commit()
            return redirect(url_for('index'))
    else:
        if 'username' in session:
            user = Users.query.filter_by(username=session['username']).first()
            tasks = Tasks.query.filter_by(user=user).all()
            return render_template('index.html', tasks=tasks)
        else:
            return redirect(url_for('login'))

@app.route('/add-task')
def add_task():
    return render_template('add_task.html')

@app.route('/remove/<task_id>')
def remove(task_id):
    task = Tasks.query.get(task_id)
    db.session.delete(task)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/toggle/<task_id>')
def toggle(task_id):
    task = Tasks.query.get(task_id)
    task.status = not task.status
    db.session.commit()
    return redirect(url_for('index'))



@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':

        if request.form['submit'] == 'Submit':
            username = request.form['username']
            password = request.form['password']
            users = Users.query.all()
            for user in users:
                if user.username == username and user.password == password:
                    session['username'] = username
                    return redirect(url_for('index'))
            return render_template('test.html')
        else:
            return redirect(url_for('register'))

    else:
        if 'username' in session:
            return redirect(url_for('index'))
        else:
            return render_template('login.html')



@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = Users(username=username, password=password)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))
    else:
        return render_template('register.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))


if __name__ == "__main__":
    app.run(debug = True) 