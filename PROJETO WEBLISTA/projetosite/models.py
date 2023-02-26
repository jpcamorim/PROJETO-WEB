from projetosite import database, login_manager
from datetime import datetime
from flask_login import UserMixin


@login_manager.user_loader
def load_usuario(id_usuario):
    return Usuario.query.get(int(id_usuario))


class Usuario(database.Model , UserMixin):
    # criando colunas do banco de dados.
    id = database.Column(database.Integer, primary_key=True)
    username = database.Column(database.String, nullable = False)
    email = database.Column(database.String, nullable=True, unique= True)
    senha = database.Column(database.String, nullable=False)
    foto_perfil = database.Column(database.String, default='default.jpg')

class Post(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    titulo = database.Column(database.String, nullable=True)
    corpo = database.Column(database.Text, nullable=False)
    data_criacao = database.Column(database.DateTime, nullable = False, default=datetime.utcnow)

