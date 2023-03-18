import os
import sqlite3

from flask import Flask, render_template, request, abort, redirect, g

# create application object
app = Flask(__name__, instance_relative_config=True)

# database path: sqlite is a file on your system, you don't need a username and password
DATABASE = os.path.join(app.instance_path, 'todo.sqlite')


def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            DATABASE,
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()


# this will run at the end of each request
app.teardown_appcontext(close_db)


@app.route("/")
def index():
    db = get_db()
    todos = db.execute(
        'SELECT id, created, description'
        ' FROM todo'
        ' ORDER BY created DESC'
    ).fetchall()

    return render_template('index.html', todos=todos)


@app.route("/create", methods=['POST'])
def create():
    description = request.form['new-description']

    if not description:
        abort(400)

    db = get_db()
    db.execute(
        'INSERT INTO todo (description)'
        'VALUES (?)',
        (description,)
    )
    db.commit()

    return redirect('/')


@app.post("/update/<int:id>")
def update(id):
    description = request.form['description']

    if not description:
        abort(400)

    db = get_db()
    db.execute(
        'UPDATE todo SET description = ?'
        ' WHERE id = ?',
        (description, id)
    )
    db.commit()

    return redirect('/')


@app.post("/delete/<int:id>")
def delete(id):
    db = get_db()
    db.execute('DELETE FROM todo WHERE id = ?', (id,))
    db.commit()

    return redirect('/')
