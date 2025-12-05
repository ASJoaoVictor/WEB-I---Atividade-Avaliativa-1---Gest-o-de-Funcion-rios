from flask import *
import controlador_BD as ctrl_bd
from funcionario import Funcionario

app = Flask(__name__)

ctrl_bd.criar_tabelas()

CURRENT_USER = None

#ctrl_bd.adicionar_usuarios()

@app.route("/")
def home():
    return render_template("login.html")

@app.route("/autenticar", methods=["POST"])
def login():
    login = request.form.get("loginUsuario")
    senha = request.form.get("senhaUsuario")

    if(login == "" or senha == "" or " " in login):
        msg = "Usuário ou senha invalido"
        return render_template("login.html", mensagem = msg)
    
    user = autenticar(login, senha)
    if(user):
        global CURRENT_USER
        CURRENT_USER = user
        return redirect(url_for("get_menu"))
    else:
        msg = "login ou senha incorretos, tente novamente"
        return render_template("login.html", mensagem = msg)

def autenticar(login, senha):
    try:
        return ctrl_bd.validar_usuario(login, senha)
    except:
        return False


@app.route("/menu", methods=["GET"])
def get_menu():
    return render_template("menu.html", user=CURRENT_USER)

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
        if cadastrar(nome, login, senha, cargo, anoAdmissao, salario):
            return render_template("cadastro.html", mensagem = "Usuário cadastrado")
        else:
            return render_template("cadastro.html", mensagem = "Não foi possível cadastrar usuário")
        
def cadastrar(nome, login, senha, cargo, anoAdmissao, salario):
    try:
        ctrl_bd.inserir_usuario(nome, login, cargo, anoAdmissao, salario, senha)
        return True
    except:
        return False

@app.route("/listar/usuarios", methods=["GET", "POST"])
def listar_usuarios(msg=""):
    funcionarios = ctrl_bd.listar_usuarios()
    if not funcionarios:
        msg = "Nenhum usuário cadastrado!"

    return render_template("listar_usuarios.html", msg= msg, funcionarios= funcionarios)

@app.route("/listar/usuarios/cargo", methods=["POST"])
def listar_usuarios_cargo():
    cargo = request.form.get("cargo")
    funcionarios_cargo = ctrl_bd.buscar_funcionario_cargo(cargo)
    if cargo:
        return render_template("listar_usuarios.html", funcionarios= funcionarios_cargo)

    return listar_usuarios()

@app.route("/listar/usuario/nome", methods=["POST"])
def listar_usuarios_nome():
    nome = request.form.get("nome")
    if nome:
        funcionarios_nome = ctrl_bd.buscar_funcionario_nome(nome)

    return render_template("listar_usuarios.html", funcionarios= funcionarios_nome)

@app.route("/usuario/remover/<id>", methods=["GET"])
def remover_usuario(id):
    print(f"{CURRENT_USER[0]} == {id}")
    if(CURRENT_USER[0] == int(id)):
        print("deu aiga")
        return listar_usuarios("Não é possível deletar usuário atual!")

    try:
        ctrl_bd.deletar_usuario(id)
        return listar_usuarios("Usuário removido com sucesso!")
    except:
        return listar_usuarios("Não foi possivel deletar usuário")


@app.route("/usuario/editar/<id>", methods=["GET"])
def get_editar(id):
    funcionario = ctrl_bd.buscar_funcionario_id(id)
    if not funcionario:
        return render_template("editar_usuario.html", mensagem= "Usuário não encontrado", funcionario= None)
    
    return render_template("editar_usuario.html", funcionario= funcionario)

@app.route("/usuario/editar/<int:id>", methods=["POST"])
def editar_usuario(id):
    funcionario = ctrl_bd.buscar_funcionario_id(id)
    if not funcionario:
        return "usuario não encontrado"
    
    id = funcionario[0]


    senha_confirmar = request.form.get("senha_confirmar")
    novo_nome = request.form.get("nome")
    novo_login = request.form.get("login")
    novo_anoAdmissao = None
    novo_cargo = request.form.get("tipo")
    novo_salario = request.form.get("salario")
    novo_anoAdmissao = request.form.get("admissao")
    novo_senha = request.form.get("senha")

    if senha_confirmar == CURRENT_USER[6]:
        if not novo_nome:
            novo_nome = funcionario[1]
        if not novo_login:
            novo_login = funcionario[2]
        if not novo_cargo:
            novo_cargo = funcionario[3]
        if not novo_anoAdmissao:
            novo_anoAdmissao = funcionario[4]
        if not novo_salario:
            novo_salario = funcionario[5]
        if not novo_senha:
            novo_senha = funcionario[6]

        novo_salario = float(novo_salario)

        try: 
            ctrl_bd.editar_funcionario(id, novo_nome, novo_login, novo_cargo, novo_anoAdmissao, novo_salario, novo_senha)
            mensagem = "Usuário editado com sucesso!"
        except:
            mensagem = "Não foi possível editar usuário"
        finally:
            funcionario_editado = ctrl_bd.buscar_funcionario_id(id)
            return render_template("editar_usuario.html", funcionario= funcionario_editado, mensagem=  mensagem)
    return render_template("editar_usuario.html", funcionario= funcionario, mensagem=  "Senha incorreta!")
        
@app.route("/usuarios/estatisticas", methods=["GET"])
def usuarios_estatisticas():
    funcionarios = ctrl_bd.listar_usuarios()
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
        if(int(func[4]) < int(usuario_mais_antigo[4])):
            usuario_mais_antigo = func

        if(func[5] > usuario_maior_salario[5]):
            usuario_maior_salario = func

        if(func[3] == "gerente"):
            quant_gerente += 1
            temp_salario_gerente += func[5]
        elif(func[3] == "caixa"):
            quant_caixa += 1
            temp_salario_caixa += func[5]
        elif(func[3] == "serviços gerais"):
            quant_servicos_gerais += 1
            temp_salario_servicos_gerais += func[5]

    if quant_gerente:
        media_salarial_gerente = temp_salario_gerente / quant_gerente
    if quant_caixa:    
        media_salarial_caixa = temp_salario_caixa / quant_caixa
    if quant_servicos_gerais:
        media_salarial_servicos_gerais = temp_salario_servicos_gerais / quant_servicos_gerais


    return render_template("usuarios_estatisticas.html", result= (usuario_mais_antigo[1],
                                                                  usuario_maior_salario[1], 
                                                                  media_salarial_gerente, 
                                                                  media_salarial_caixa,
                                                                  media_salarial_servicos_gerais,
                                                                  quant_gerente,
                                                                  quant_caixa,
                                                                  quant_servicos_gerais))
@app.route("/salario/aumento/setor", methods=["GET"])
def aumento_setor(msg=""):
    return render_template("aumento_setor.html", msg_setor= msg, funcionarios= ctrl_bd.listar_usuarios())

@app.route("/salario/aumento/individual", methods=["GET"])
def aumento_individual():
    return render_template("aumento_individual.html", msg= "", funcionarios= ctrl_bd.listar_usuarios())

@app.route("/salario/aumento/setor", methods=["POST"])
def aplicar_aumento_setor():
    taxa_aumento = (float(request.form.get("taxa_aumento"))/100)+1
    setor = request.form.get("setor")
    if setor == "todos":
        ctrl_bd.aumentar_salario_todos(taxa_aumento)
    else:
        for func in ctrl_bd.buscar_funcionario_cargo(setor):
                ctrl_bd.aumentar_salario_por_id(func[0], taxa_aumento)

    return aumento_setor("Aumento aplicado com sucesso!")

@app.route("/aumento/nome", methods=["POST"])
def aplicar_aumento_individual():
    funcionarios_aumento = request.form.getlist("funcionarios_aumento")
    taxa_aumento = (float(request.form.get("taxa_aumento"))/100)+1

    
    for id in funcionarios_aumento:
        usuario = ctrl_bd.buscar_funcionario_id(id)
        if not usuario:
            continue
        ctrl_bd.aumentar_salario_por_id(id, taxa_aumento)

    return render_template("aumento_individual.html", msg_individual= "Aumento aplicado", funcionarios= ctrl_bd.listar_usuarios())

if __name__ == "__main__":
    app.run(debug=True)
