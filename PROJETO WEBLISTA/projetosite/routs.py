from flask import render_template, redirect, url_for, request, flash, session
from projetosite import app, database , bcrypt
from projetosite.forms import FormCriarConta, FormLogin, FormEditarPerfil, FormChecklist
from projetosite.models import Usuario,Post
from flask_login import login_user, logout_user, current_user, login_required
import secrets
import os
from PIL import Image

# criando as paginas 

def check_realizados(form):
    lista_realizado = []
    for campo in form:
            if campo.data:
                lista_realizado.append(campo.label.text)
    return ';'.join(lista_realizado)

@app.route("/")
@login_required
def inicio():
    form = FormChecklist()
    form.botao_check.value=True
    current_user.username = check_realizados(form)
    posts = Post.query.order_by(Post.id.desc())
    checkbox_state = session.get('botao_check.data', False)
    return render_template('inicio.html', posts=posts, form=form, checkbox_state=checkbox_state) # necessário passar o mesmo nome do arquivo para que possa ser lido.



@app.route("/login", methods=['GET', 'POST'])
def login():
    # importamos as instancias para dentro das nossa função.Para que seja possível retorna-las em HTML, passa no return dentro do render_template
    form_criar_conta = FormCriarConta()
    form_login = FormLogin()

    # verificando quando o botão for validado, será enviado uma msng de sucesso após será redirecionado.
    if form_criar_conta.validate_on_submit() and 'botao_submit_criarconta' in request.form: 
        # criptografando senha do usuario
        senha_crypt = bcrypt.generate_password_hash(form_criar_conta.senha.data)
        # pegando informações preenchidas pelo usuario e add no database
        usuario= Usuario(username=form_criar_conta.username.data, email=form_criar_conta.email.data, senha=senha_crypt)
        database.session.add(usuario)
        database.session.commit()

        flash(f'Conta criada com sucesso para o  e-mail {form_criar_conta.email.data}' , 'alert-success') # exibindo informação 
        return redirect(url_for('inicio')) # redirecionando para a função 

    if form_login.validate_on_submit() and 'botao_submit_login' in request.form:
        usuario = Usuario.query.filter_by(email=form_login.email.data).first()
        if usuario and bcrypt.check_password_hash(usuario.senha, form_login.senha.data):
            login_user(usuario, remember=form_login.botao_lembrar_senha.data)
            flash(f'Login feito com sucesso no e-mail {form_login.email.data}', 'alert-success')
            par_next = request.args.get("next")
            if par_next:
                return redirect(par_next)
            else:
                return redirect(url_for('inicio')) # redirecionando para a função return redirect(url_for("inicio")
        else:
            flash('Falha no Login.E-mail ou senha Incorretos', 'alert-danger')

    return render_template ('login.html', form_criar_conta= form_criar_conta, form_login=form_login)

@app.route("/sair")
@login_required
def sair():
    logout_user()
    flash(f'Logout feito com sucesso', 'alert-success')
    return redirect(url_for('inicio'))

@app.route('/perfil')
@login_required
def perfil():
    post_total= Post.query.all()
    tamanho = len(post_total)
    foto_perfil = url_for('static', filename='fotos/{}'.format(current_user.foto_perfil))
    return render_template('perfil.html', foto_perfil=foto_perfil, tamanho=tamanho)
    
@app.route("/checklist", methods=['GET', 'POST'])
@login_required
def checklist():
    form = FormChecklist()
    if form.validate_on_submit():
        post = Post(titulo = form.titulo.data, corpo = form.corpo.data)
        database.session.add(post)
        database.session.commit()
        flash('Checklist Criado com Sucesso', 'alert-success')
        return redirect(url_for('inicio'))
    return render_template('checklist.html', form=form)
    

# função para modificar nome da imagem, reduzir e salvar
def salvar_imagem(imagem):
    codigo = secrets.token_hex(8) 
    nome, extensao = os.path.splitext(imagem.filename)
    nome_arquivo = nome + codigo + extensao
    caminho_completo = os.path.join(app.root_path,'static/fotos', nome_arquivo)
    tamanho = (200, 200)
    imagem_reduzida = Image.open(imagem)
    imagem_reduzida = imagem_reduzida.resize(tamanho)
    imagem_reduzida.save(caminho_completo)
    return nome_arquivo


@app.route('/perfil/editar', methods=['GET', 'POST'])
@login_required
def editar_perfil():
    form = FormEditarPerfil()
    post_total= Post.query.all()
    tamanho = len(post_total)
    if form.validate_on_submit():
        current_user.email = form.email.data
        current_user.username = form.username.data
        if form.foto_perfil.data:
            nome_imagem = salvar_imagem(form.foto_perfil.data)
            current_user.foto_perfil = nome_imagem
        database.session.commit()
        flash('Perfil atualizado com Sucesso', 'alert-success')
        return redirect(url_for('perfil'))
    elif request.method == "GET":
        form.email.data = current_user.email
        form.username.data = current_user.username
    foto_perfil = url_for('static', filename='fotos/{}'.format(current_user.foto_perfil))
    return render_template('editarperfil.html', foto_perfil=foto_perfil, form=form, tamanho=tamanho)

@app.route('/post/<post_id>', methods=['GET', 'POST'])
@login_required
def exibir_post(post_id):
    post = Post.query.get(post_id)
    form = FormChecklist()
    if request.method == 'GET':
        form.titulo.data = post.titulo
        form.corpo.data = post.corpo
    elif form.validate_on_submit():
        post.titulo = form.titulo.data
        post.corpo = form.corpo.data
        database.session.commit()
        flash('CheckList Atualizado com Sucesso', 'alert-success')
        return redirect(url_for('inicio'))
    else:
        form = None
    return render_template('post.html', post=post, form=form)

@app.route('/post/<post_id>/excluir', methods=['GET', 'POST'])
@login_required
def excluir_post(post_id):
    post = Post.query.get(post_id)
    database.session.delete(post)
    database.session.commit()
    flash("CheckList deletado com sucesso" , 'alert-danger')
    return redirect(url_for('inicio'))