from flask import *
from funcionario import Funcionario

loginPadrao = "user"
senhaPadrao = "123"

#funcionario: nome, login, senha, tipo(gerente, caixa, serviços_gerais), salario

gerente = Funcionario("julia", "julia", "gerente", 3500.0, 2015, "123")
caixa = Funcionario("ana", "ana", "caixa", 2500.0, 2010, "123")
servico = Funcionario("andressa", "andressa", "serviços gerais",1250.0, 2020, "132")
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

@app.route("/logoff", methods=["GET"])
def logoff():
    global current_user
    current_user = None
    return redirect(url_for("home"))

@app.route("/menu", methods=["GET"])
def get_menu():
    return render_template("menu.html", user= current_user)

@app.route("/cadastrar")
def get_cadastro():
    return render_template("cadastro.html")

@app.route("/cadastrar", methods=["POST"])
def cadastro():
    nome = request.form.get("nome").lower()
    login = request.form.get("login").lower()
    cargo = request.form.get("tipo")
    salario = float(request.form.get("salario"))
    anoAdmissao = int(request.form.get("admissao"))
    senha = request.form.get("senha")

    if(nome == "" or login == "" or salario == "" or senha == "" or " " in login):
        return render_template("cadastro.html", mensagem = "Campos inválidos")
    else:
        for func in funcionarios:
            if(login == func.login):
                return render_template("cadastro.html", mensagem = "Usuário com login já existe")
            
        if(cadastrar(nome, login, senha, cargo, anoAdmissao, salario)):
            return render_template("login.html", mensagem= "Usuário cadastro com sucesso!")
        else:
            return render_template("cadastro.html", mensagem = "erro ao cadastrar usuário")
def cadastrar(nome, login, senha, cargo, anoAdmissao, salario):
    try:
        funcionarios.append(Funcionario(nome, login, cargo, salario, anoAdmissao, senha))
        return True
    except:
        return False

@app.route("/listar/usuarios", methods=["GET", "POST"])
def listar_usuarios(msg=""):

    if not funcionarios:
        msg = "Nenhum usuário cadastrado!"

    return render_template("listar_usuarios.html", msg= msg, funcionarios= funcionarios)

@app.route("/listar/usuarios/cargo", methods=["POST"])
def listar_usuarios_cargo():
    cargo = request.form.get("cargo")
    lista_funcionarios = funcionarios[0:]
    if cargo:
        lista_funcionarios = []
        for func in funcionarios:
            if func.cargo == cargo:
                lista_funcionarios.append(func)

    return render_template("listar_usuarios.html", funcionarios= lista_funcionarios)

@app.route("/listar/usuario/nome", methods=["POST"])
def listar_usuarios_nome():
    nome = request.form.get("nome")
    lista_funcionarios = []
    if nome:
        lista_funcionarios.append(buscar_por_nome(nome))

    return render_template("listar_usuarios.html", funcionarios= lista_funcionarios)

def buscar_por_nome(nome):
    for func in funcionarios:
        if nome == func.nome:
            return func
    return None

@app.route("/usuario/remover/<nome>", methods=["GET"])
def remover_usuario(nome):
    usuario = buscar_por_nome(nome)

    if(current_user.nome == nome):
        return listar_usuarios("Não é possível remover usuário atual!")
    funcionarios.remove(usuario)

    return listar_usuarios("Usuário removido com sucesso!")

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
    
    senha_confirmar = request.form.get("senha_confirmar")
    nome = request.form.get("nome")
    login = request.form.get("login")
    anoAdmissao = None
    cargo = request.form.get("tipo")
    salario = request.form.get("salario")
    anoAdmissao = request.form.get("admissao")
    senha = request.form.get("senha")

    if senha_confirmar == "123":
        if nome:
            usuario.nome = nome
        if login:
            usuario.login = login
        if anoAdmissao:
            usuario.anoAdmissao = int(anoAdmissao)
        if cargo:
            usuario.cargo = cargo
        if salario:
            usuario.salario = float(salario)
        if senha:
            usuario.senha = senha

    return render_template("editar_usuario.html", usuario= usuario, mensagem= "Usuário editado com sucesso!")
        
@app.route("/usuarios/estatisticas", methods=["GET"])
def usuarios_estatisticas():
    usuario_mais_antigo = funcionarios[0]
    usuario_maior_salario = funcionarios[0]
    media_salarial_gerente = 0
    media_salarial_caixa = 0
    media_salarial_servicos_gerais = 0
    quant_gerente = 0
    quant_caixa = 0
    quant_servicos_gerais = 0

    temp_salario_gerente = 0
    temp_salario_caixa = 0
    temp_salario_servicos_gerais = 0

    for func in funcionarios:
        if(func.anoAdmissao < usuario_mais_antigo.anoAdmissao):
            usuario_mais_antigo = func

        if(func.salario > usuario_maior_salario.salario):
            usuario_maior_salario = func

        if(func.cargo == "gerente"):
            print(func.nome)
            quant_gerente += 1
            temp_salario_gerente += func.salario
        elif(func.cargo == "caixa"):
            print(func.nome)
            quant_caixa += 1
            temp_salario_caixa += func.salario
        elif(func.cargo == "serviços gerais"):
            print(func.nome)
            quant_servicos_gerais += 1
            temp_salario_servicos_gerais += func.salario

    if quant_gerente:
        media_salarial_gerente = temp_salario_gerente / quant_gerente
    if quant_caixa:    
        media_salarial_caixa = temp_salario_caixa / quant_caixa
    if quant_servicos_gerais:
        media_salarial_servicos_gerais = temp_salario_servicos_gerais / quant_servicos_gerais


    return render_template("usuarios_estatisticas.html", result= (usuario_mais_antigo.nome,
                                                                  usuario_maior_salario.nome, 
                                                                  media_salarial_gerente, 
                                                                  media_salarial_caixa,
                                                                  media_salarial_servicos_gerais,
                                                                  quant_gerente,
                                                                  quant_caixa,
                                                                  quant_servicos_gerais))
@app.route("/salario/aumento/setor", methods=["GET"])
def aumento_setor(msg=""):
    return render_template("aumento_setor.html", msg_setor= msg, funcionarios= funcionarios)

@app.route("/salario/aumento/individual", methods=["GET"])
def aumento_individual():
    return render_template("aumento_individual.html", msg= "", funcionarios= funcionarios)

@app.route("/salario/aumento/setor", methods=["POST"])
def aplicar_aumento_setor():
    taxa_aumento = (float(request.form.get("taxa_aumento"))/100)+1
    setor = request.form.get("setor")
    if setor == "todos":
        for func in funcionarios:
            func.salario *= taxa_aumento
    else:
        for func in funcionarios:
            if func.cargo == setor:
                func.salario *= taxa_aumento

    return aumento_setor("Aumento aplicado com sucesso!")

@app.route("/aumento/nome", methods=["POST"])
def aplicar_aumento_individual():
    funcionarios_aumento = request.form.getlist("funcionarios_aumento")
    taxa_aumento = (float(request.form.get("taxa_aumento"))/100)+1

    
    for nome in funcionarios_aumento:
        usuario = buscar_por_nome(nome)
        if not usuario:
            continue
            return render_template("aumento.html", msg_individual= "usuário não encontrado")
        usuario.salario *= taxa_aumento

    return render_template("aumento_individual.html", msg_individual= "Aumento aplicado", funcionarios= funcionarios)

if __name__ == "__main__":
    app.run(debug=True)
