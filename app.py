from flask import Flask, render_template
from flask_wtf.csrf import CSRFProtect
from flask_migrate import Migrate
from config import DevelopmentConfig
from models import db

from pedidos.routes import pedidos
from reportes.routes import reportes

app = Flask(__name__)
app.config.from_object(DevelopmentConfig)

app.register_blueprint(pedidos)
app.register_blueprint(reportes)

csrf = CSRFProtect()
db.init_app(app)
migrate = Migrate(app, db)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    csrf.init_app(app)
    app.run()