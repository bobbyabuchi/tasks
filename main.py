from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy  import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tdl.db'

db = SQLAlchemy(app)

class todo_list(db.Model):
	"""docstring for todo_list"""
	td_id = db.Column(db.Integer, primary_key=True)
	td_text = db.Column(db.String(200))
	td_status = db.Column(db.Boolean)


@app.route('/')
def index():
	todo_items_from_db = todo_list.query.filter_by(td_status=False).all()
	done_items_from_db = todo_list.query.filter_by(td_status=True).all()

	return render_template('index.html', todo_items_from_db=todo_items_from_db, done_items_from_db=done_items_from_db)


@app.route('/add', methods=['post'])
def add():
	todo_data = todo_list(td_text=request.form['todo_item'], td_status=False)
	db.session.add(todo_data)
	db.session.commit()
	return redirect(url_for('index'))
    #return '<h1>{}</h1>'.format(request.form['todo_item'])


@app.route('/success/<td_id>')
def success(td_id):
	todo_data = todo_list.query.filter_by(td_id=int(td_id)).first() #.first, since we're expecting one...
	todo_data.td_status = True
	db.session.commit()

	# print(request.form[1]) # let's us see what gets returned
	return redirect(url_for('index'))


@app.route('/undo_success/<td_id>')
def undo_success(td_id):
	todo_data = todo_list.query.filter_by(td_id=int(td_id)).first() #.first, since we're expecting one...
	todo_data.td_status = False
	db.session.commit()

	# print(request.form[1]) # let's us see what gets returned
	return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)



 