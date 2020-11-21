from flask import render_template, flash, request, redirect
from app import app, db
from app.forms import LoginForm
from flask_login import login_required, login_user, logout_user
from app.models import User, Messages

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
	if request.method == 'POST':
		sender_content = request.form['sender']
		msg_content = request.form['msg']
		new_msg = Messages(sender=sender_content, msg=msg_content)

		try:
			db.session.add(new_msg)
			db.session.commit()
			return redirect('/')
		except:
			return 'error nambahin pesan'
	else:
		msg_list = Messages.query.order_by(Messages.timestamp.desc()).all()
		return render_template('index.html', msg_list=msg_list)

@app.route('/login', methods=['GET', 'POST'])
def login():
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(username=form.username.data).first()
		if user is None or not user.check_password(form.password.data):
			flash('Invalid username or password')
			return redirect('/login')
		login_user(user)
		return redirect('/adm00n')
	return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
	logout_user()
	return redirect('/')

@app.route('/adm00n')
@login_required
def adm00n():
	msg_list = Messages.query.order_by(Messages.timestamp.desc()).all()
	return render_template('adm00n.html', msg_list=msg_list)

@app.route('/delete/<int:id>')
def delete(id):
	msg_to_delete = Messages.query.get_or_404(id)
	try:
		db.session.delete(msg_to_delete)
		db.session.commit()
		return redirect('/adm00n')
	except:
		return 'error delet :((('

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
	msg = Messages.query.get_or_404(id)
	if request.method == 'POST':
		msg.sender = request.form['sender']
		msg.msg = request.form['msg']
		try:
			db.session.commit()
			return redirect('/adm00n')
		except:
			return 'pengen update malah eror'
	else:
		return render_template('update.html', msg=msg)

@app.route('/reply/<int:id>', methods=['GET', 'POST'])
def reply(id):
	msg = Messages.query.get_or_404(id)
	if request.method == 'POST':
		sender_content = Messages.query.get_or_404(id).sender
		msg_content = Messages.query.get_or_404(id).msg
		reply_content = request.form['reply']
		new_msg = Messages(sender=sender_content, msg=msg_content, reply=reply_content)
		msg = new_msg
		try:
			db.session.commit()
			return redirect('/adm00n')
		except:
			return 'anjir error dong pengen reply'
	else:
		return render_template('reply.html', msg=msg)