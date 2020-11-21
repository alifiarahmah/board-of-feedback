from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'test.db'
db = SQLAlchemy(app)

class Messages(db.Model):
	id = db.Column(db.Integer, primary_key=True)

	#sender = db.Column(db.String(50), nullable=True)
	msg = db.Column(db.String(300), nullable=False)
	date_created = db.Column(db.DateTime, default=datetime.utcnow)

	def __repr__(self):
		# return '<Task %r' % self.id
		return '<Messages %r>' % self.id

class Config(object):
	LOG_TO_STDOUT = os.environ.get('LOG_TO_STDOUT')

@app.route('/', methods=['POST', 'GET'])
def index():
	if request.method == 'POST':
		msg_content = request.form['msg']
		#sender_content = request.form['sender']
		#new_msg = Messages(msg=msg_content, sender=sender_content)
		new_msg = Messages(msg=msg_content)

		try:
			db.session.add(new_msg)
			db.session.commit()
			return redirect('/')
		except:
			return 'error maap'

	else:
		msg_list = Messages.query.order_by(Messages.date_created.desc()).all()
		#msg_list = Messages['msg'].query.order_by(Messages.date_created.desc()).all()
		#sender_list = Messages['sender'].query.order_by(Messages.date_created.desc()).all()
		#return render_template('index.html', msg_list=msg_list, sender=sender_list)
		return render_template('index.html', msg_list=msg_list)


@app.route('/adm00n')
def adm00n():
	msg_list = Messages.query.order_by(Messages.date_created.desc()).all()
	return render_template('adm00n.html', msg_list=msg_list)

@app.route('/delete/<int:id>')
def delete(id):
	msg_to_delete = Messages.query.get_or_404(id)
	try:
		db.session.delete(msg_to_delete)
		db.session.commit()
		return redirect('/adm00n')
	except:
		return 'error delete yhA'

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
	msg = Messages.query.get_or_404(id)

	if request.method == 'POST':
		msg.msg = request.form['msg']

		try:
			db.session.commit()
			return redirect('/adm00n')
		except:
			return '✨ s i l a h k a n  c o b  a  l a g i ✨'

	else:
		return render_template('update.html', msg=msg)

def create_app(config_class=Config):
    # ...
    if not app.debug and not app.testing:
        # ...

        if app.config['LOG_TO_STDOUT']:
            stream_handler = logging.StreamHandler()
            stream_handler.setLevel(logging.INFO)
            app.logger.addHandler(stream_handler)
        else:
            if not os.path.exists('logs'):
                os.mkdir('logs')
            file_handler = RotatingFileHandler('logs/microblog.log',
                                               maxBytes=10240, backupCount=10)
            file_handler.setFormatter(logging.Formatter(
                '%(asctime)s %(levelname)s: %(message)s '
                '[in %(pathname)s:%(lineno)d]'))
            file_handler.setLevel(logging.INFO)
            app.logger.addHandler(file_handler)

        app.logger.setLevel(logging.INFO)
        app.logger.info('Microblog startup')

    return app

if __name__ == "__main__":
	app.run(debug=True)