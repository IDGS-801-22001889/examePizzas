from flask import Flask, render_template, request, redirect, url_for
from flask import flash
from flask_wtf.csrf import CSRFProtect
from flask import g

from flask_migrate import Migrate

app = Flask(__name__)
csrf = CSRFProtect()

@app.route("/")
def index():
	return render_template('index.html')

if __name__ == '__main__':
	csrf.init_app(app)
	app.run()