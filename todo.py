import os
import sqlite3

from flask import Flask, render_template, request, abort, redirect

# create application object
app = Flask(__name__, instance_relative_config=True)

# database path: sqlite is a file on your system, you don't need a username and password
DATABASE = os.path.join(app.instance_path, 'todo.sqlite')


@app.route("/")
def index():
    db = sqlite3.connect(
        DATABASE,
        detect_types=sqlite3.PARSE_DECLTYPES
    )

    todos = db.execute(
        'SELECT id, created, description'
        ' FROM todo'
        ' ORDER BY created DESC'
    ).fetchall()

    db.close()

    return render_template('index.html', todos=todos)


@app.route("/create", methods=['POST'])
def create():
    description = request.form['new-description']

    if not description:
        abort(400)

    db = sqlite3.connect(
        DATABASE,
        detect_types=sqlite3.PARSE_DECLTYPES
    )

    print(description)

    db.execute(
        'INSERT INTO todo (description)'
        'VALUES (?)',
        (description,)
    )
    db.commit()

    db.close()

    return redirect('/')


@app.post("/update/<int:id>")
def update(id):
    description = request.form['description']

    if not description:
        abort(400)

    db = sqlite3.connect(
        DATABASE,
        detect_types=sqlite3.PARSE_DECLTYPES
    )
    db.execute(
        'UPDATE todo SET description = ?'
        ' WHERE id = ?',
        (description, id)
    )
    db.commit()
    db.close()

    return redirect('/')


@app.post("/delete/<int:id>")
def delete(id):
    db = sqlite3.connect(
        DATABASE,
        detect_types=sqlite3.PARSE_DECLTYPES
    )
    db.execute('DELETE FROM todo WHERE id = ?', (id,))
    db.commit()
    db.close()

    return redirect('/')
