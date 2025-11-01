from flask import *
from funcionario import Funcionario

loginPadrao = "user"
senhaPadrao = "123"

#funcionario: nome, login, senha, tipo(gerente, caixa, serviços_gerais), salario

gerente = Funcionario("julia", "julia", "gerente", 3500.0, 2015, "123")
caixa = Funcionario("Ana", "ana", "caixa", 2500.0, 2019, "123")
servico = Funcionario("andressa", "andressa", "servico gerais",1250.0, 2020, "132")
funcionarios = [gerente, caixa, servico]
current_user = None

app = Flask(__name__)

@app.route("/")
def home():
    if current_user:
        return redirect(url_for("get_menu"))
    
    return render_template("login.html")

@app.route("/autenticar", methods=["POST"])
def autenticar():
    login = request.form.get("loginUsuario")
    senha = request.form.get("senhaUsuario")

    if(login == "" or senha == "" or " " in login):
        msg = "Usuário ou senha invalido"
        return render_template("login.html", mensagem = msg)
    else:
        logado, user = logar(login, senha)
        if(logado):
            global current_user
            current_user = user
            return redirect(url_for("get_menu"))
        else:
            msg = "login ou senha incorretos, tente novamente"
            return render_template("login.html", mensagem = msg)

def logar(login, senha):
    for func in funcionarios:
        if(func.login == login and func.senha == senha):
            return True, func
    return False, None

@app.route("/menu", methods=["GET"])
def get_menu():
    print(current_user.nome)
    return render_template("menu.html", user= current_user)

@app.route("/cadastrar")
def get_cadastro():
    return render_template("cadastro.html")

@app.route("/cadastrar", methods=["POST"])
def cadastro():
    nome = request.form.get("nome")
    login = request.form.get("login")
    cargo = request.form.get("tipo")
    salario = float(request.form.get("salario"))
    anoAdmissao = int(request.form.get("admissao"))
    senha = request.form.get("senha")

    if(nome == "" or login == "" or salario == "" or senha == ""):
        return render_template("cadastro.html", mensagem = "Campos inválidos")
    else:
        for func in funcionarios:
            if(login == func.login):
                return render_template("cadastro.html", mensagem = "Usuário com login já existe")
            
        if(cadastrar(nome, login, senha, cargo, anoAdmissao, salario)):
            return render_template("login.html")
        else:
            return render_template("cadastro.html", mensagem = "erro ao cadastrar usuário")
def cadastrar(nome, login, senha, cargo, anoAdmissao, salario):
    try:
        funcionarios.append(Funcionario(nome, login, cargo, salario, anoAdmissao, senha))
        return True
    except:
        return False

@app.route("/listar/Usuarios", methods=["GET", "POST"])
def listarUsuarios():
    return render_template("listarUsuario.html", funcionarios= funcionarios)


@app.route("/listar/usuarios/cargo", methods=["POST"])
def listar_usuarios_cargo():
    cargo = request.form.get("cargo")
    lista_funcionarios = funcionarios[0:]
    if cargo:
        lista_funcionarios = []
        for func in funcionarios:
            if func.cargo == cargo:
                lista_funcionarios.append(func)

    return render_template("listarUsuario.html", funcionarios= lista_funcionarios)

@app.route("/listar/usuario/nome", methods=["POST"])
def listar_usuarios_nome():
    nome = request.form.get("nome")
    lista_funcionarios = []
    if nome:
        lista_funcionarios.append(buscar_por_nome(nome))

    return render_template("listarUsuario.html", funcionarios= lista_funcionarios)

def buscar_por_nome(nome):
    for func in funcionarios:
        if nome == func.nome:
            return func
    return None

@app.route("/usuario/editar/<nome>", methods=["GET"])
def get_editar(nome):
    usuario = buscar_por_nome(nome)
    if not usuario:
        return render_template("editar_usuario.html", message= "Usuário não encontrado", usuario= None)
    
    return render_template("editar_usuario.html", message= None, usuario= usuario)

@app.route("/usuario/editar/<nome>", methods=["POST"])
def editar_usuario(nome):
    usuario = buscar_por_nome(nome)
    if not usuario:
        return "usuario não encontrado"
    
    senha = request.form.get("senha")

    if senha == current_user.senha:
        print("teste")
        usuario.nome = request.form.get("nome")
        usuario.login = request.form.get("login")
        usuario.anoAdmissaocargo = request.form.get("tipo")
        usuario.salario = float(request.form.get("salario"))
        usuario.anoAdmissao = int(request.form.get("admissao"))
        return redirect(url_for("get_menu"))
        

if __name__ == "__main__":
    app.run(debug=True)
