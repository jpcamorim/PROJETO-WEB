from flask import Flask
import os
from flask_sqlalchemy import SQLAlchemy 
from flask_bcrypt import Bcrypt 
from flask_login import LoginManager

app = Flask(__name__)


SECRET_KEY = os.urandom(32) # gerando uma secret_key
app.config['SECRET_KEY'] = SECRET_KEY
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db' # criando o banco de dados.

database = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = "login"
login_manager.login_message_category = "alert-info"
from projetosite import routs