from app import app

@app.route('/')
@app.route('/index')
def index():
	return "coming soon, masih belajar lagi"
