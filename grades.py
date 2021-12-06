from logging import debug
from flask import Flask, redirect, render_template, g, request, session, url_for, Blueprint

import sqlite3 as sqli

from werkzeug.utils import escape
from werkzeug.security import check_password_hash, generate_password_hash




app = Flask(__name__)

con = None

con = sqli.connect('hw13.db')
cur = con.cursor()

cur.execute("CREATE TABLE IF NOT EXISTS students( id INTEGER PRIMARY KEY AUTOINCREMENT NULL, first_name TEXT NULL, last_name TEXT NULL)")

cur.execute("CREATE TABLE IF NOT EXISTS quizzes(id INTEGER PRIMARY KEY AUTOINCREMENT NULL, subject TEXT NULL, quiz_questions INTEGER NULL, date DATE NULL)")

cur.execute("CREATE TABLE IF NOT EXISTS student_quiz_results(id INTEGER PRIMARY KEY AUTOINCREMENT NULL, student_first_name TEXT NULL,student_last_name TEXT NULL, score INTEGER NULL, FOREIGN KEY(student_first_name, student_last_name) REFERENCES students(first_name, last_name))")

cur.execute("CREATE TABLE IF NOT EXISTS user (id INTEGER PRIMARY KEY AUTOINCREMENT NULL, username TEXT NULL, password TEXT NULL)")

con.commit()


student_grades = []
student_quizzes = []

students = {}
student_quiz= {}

@app.route('/', methods =['GET'])
def dashboard():
    con = sqli.connect('hw13.db')
    cur = con.cursor()

    student = cur.execute('SELECT * FROM students').fetchall()
    quizzes = cur.execute('SELECT * FROM quizzes').fetchall()
    results = cur.execute('SELECT id, score FROM student_quiz_results').fetchall()

    students =student
    students_quizzes=quizzes
    student_grades.append(students)
    student_quizzes.append(students_quizzes)

 
    return render_template('dashboard.html', student_grades=student_grades, student_quizzes = student_quizzes)

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        con = sqli.connect('hw13.db')
        cur = con.cursor()
        error = None
        user = cur.execute(
            'SELECT * FROM user WHERE username = ?', (username,)
        ).fetchone()

        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('index'))

        flash(error)

 
    return render_template('login.html', error=error)



@app.route('/student/add', methods =['GET', 'POST'])
def add_student():
    con = sqli.connect('hw13.db')
    cur = con.cursor()
    if request.method == 'GET':
     return render_template('add.html')
    if request.method == 'POST':

        first_name = request.form['student_first_name']
        last_name = request.form['student_last_name']

        student=(
             (None, first_name, last_name)
        )
        cur.execute('INSERT OR IGNORE INTO students VALUES(?,?,?)',(student))
        con.commit()

        print(student)
        
        return redirect(url_for('dashboard'))
    return redirect(url_for('dashboard'))

@app.route('/quiz/add', methods=['GET', 'POST'])
def add_quiz():
    con = sqli.connect('hw13.db')
    cur = con.cursor()
    if request.method == 'GET':
     return render_template('add_quiz.html')
    if request.method == 'POST':

        subject = request.form['subject']
        questions = request.form['questions']
        date = request.form['date']
        grade = request.form['score']

        quiz=(
             (None, subject, questions, date)
        )
        grade=(
            (None, None, None, grade)
        )
        cur.execute('INSERT OR IGNORE INTO quizzes VALUES(?,?,?,?)',(quiz))
        cur.execute('INSERT OR IGNORE INTO student_quiz_results VALUES(?,?,?,?)',(grade))
        con.commit()
        
        return redirect(url_for('dashboard'))
    return redirect(url_for('dashboard'))

@app.route('/student/<id>', methods =['POST', 'GET'])
def student_id(id):
    con = sqli.connect('hw13.db')
    cur = con.cursor()
    if request.method == 'GET':

        result=cur.execute('SELECT id, student_first_name, student_last_name, score FROM student_quiz_results WHERE id=?',(id,)).fetchone()

        test_scores = result
        quiz_results = []
        quiz_results.append(test_scores)
        print(test_scores)
        print(quiz_results)
        return render_template('results.html', quiz_results = quiz_results, )

    return redirect(url_for('dashboard'))


if __name__ == '__main__':
    app.run(port=3000, debug=True)