from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import Email, EqualTo, DataRequired, Length, ValidationError
from projetosite.models import Usuario
from flask_login import current_user
# criando as classes dos formulários.
# em vez de se passar o __init__ vamos passar FlaskForm.

class FormCriarConta(FlaskForm):
    # agr vamos passar os parametros que nós iremos utilizar dentro do forms
    #lembrando que os validators sõa passados dentro de listas, EqualTo("nome da função na qual vc quer comparar.")
    username = StringField('Usário', validators=[DataRequired()])
    email = StringField('E-mail',validators=[DataRequired(),Email()])
    senha=PasswordField('Senha',validators=[DataRequired(),Length(6,20)])
    confirmacao_senha = PasswordField('Confirmação da senha',validators=[DataRequired(), EqualTo('senha')])
    botao_submit_criarconta = SubmitField('Criar Conta',)

    # criando função para verificar se já existe um mesmo email dentro do banco de dados.
    def validate_email(self, email):
        usuario =Usuario.query.filter_by(email=email.data).first() # pegando o primeiro valor dentro do banco de dados
        if usuario:
            raise ValidationError ('E-mail já cadastrado.')

# lembrando o nome do botão não pode ser o mesmo, pois estão na mesma página.
class FormLogin(FlaskForm):
    email = StringField('E-mail',validators=[DataRequired(),Email()])
    senha=PasswordField('Senha',validators=[DataRequired(),Length(6,20)])
    botao_submit_login= SubmitField('Fazer Login')
    botao_lembrar_senha = BooleanField('Lembrar dados de acesso')

class FormEditarPerfil(FlaskForm):
    username = StringField('Nome de Usuário', validators=[DataRequired()])
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    foto_perfil = FileField('Atualizar Foto de Perfil', validators=[FileAllowed(['jpg', 'png'])])
    botao_submit_editarperfil = SubmitField('Confirmar Edição')

    def validate_email(self, email):
        if current_user.email != email.data:
            usuario = Usuario.query.filter_by(email=email.data).first()
            if usuario:
                raise ValidationError('Já existe um usuário com esse e-mail. Cadastre outro e-mail')
            

class FormChecklist(FlaskForm):
    titulo = StringField('Título',validators=[DataRequired(), Length(5, 140)])
    corpo = TextAreaField('Descreva uma Atividade Aqui.', validators=[DataRequired()])
    botao_submit = SubmitField('Confirmar')
    botao_check = BooleanField('Realizado')