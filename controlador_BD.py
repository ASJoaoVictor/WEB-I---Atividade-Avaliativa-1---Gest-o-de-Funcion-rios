import sqlite3 as sqlite

def criar_tabelas():
    conexao = sqlite.connect('database.sqlite')
    cursor = conexao.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS funcionario(
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   nome TEXT NOT NULL,
                   login TEXT NOT NULL UNIQUE,
                   cargo TEXT NOT NULL,
                   ano_admissao TEXT NOT NULL,
                   salario FLOAT,
                   senha TEXT NOT NULL
                   )
    """)
    conexao.commit()
    conexao.close()

def inserir_usuario(nome, login, cargo, ano_admissao, salario, senha):
    conexao = sqlite.connect("database.sqlite")
    cursor = conexao.cursor()
    cursor.execute("INSERT INTO funcionario(nome, login, cargo, ano_admissao, salario, senha) VALUES (?, ?, ?, ?, ?, ?)", (nome,
                                                                                                              login, 
                                                                                                              cargo, 
                                                                                                              ano_admissao, 
                                                                                                              salario, 
                                                                                                              senha))
    conexao.commit()
    conexao.close()

def validar_usuario(login, senha):
    conexao = sqlite.connect("database.sqlite")
    cursor = conexao.cursor()

    cursor.execute("SELECT * FROM funcionario WHERE login = ? AND senha = ?", (login, senha))
    resultado = cursor.fetchone()

    conexao.close()
    return resultado

def listar_usuarios():
    conexao = sqlite.connect("database.sqlite")
    cursor = conexao.cursor()

    cursor.execute("SELECT * FROM funcionario")
    resultado = cursor.fetchall()

    conexao.close()
    return resultado


def deletar_usuario(id):
    conexao = sqlite.connect("database.sqlite")
    cursor = conexao.cursor()

    cursor.execute("DELETE FROM funcionario WHERE id = ?", (id,))

    conexao.commit()
    conexao.close()

def buscar_funcionario_cargo(cargo):
    conexao = sqlite.connect("database.sqlite")
    cursor = conexao.cursor()

    cursor.execute("SELECT * FROM funcionario WHERE cargo = ?", (cargo,))
    resultado = cursor.fetchall()

    conexao.close()
    return resultado

def buscar_funcionario_nome(nome):
    nome = f"{nome}%"
    print(nome)
    conexao = sqlite.connect("database.sqlite")
    cursor = conexao.cursor()

    cursor.execute("SELECT * FROM funcionario WHERE nome like ?", (nome,))
    resultado = cursor.fetchall()

    conexao.close()
    return resultado

def buscar_funcionario_id(id):
    conexao = sqlite.connect("database.sqlite")
    cursor = conexao.cursor()

    cursor.execute("SELECT * FROM funcionario WHERE id = ?", (id,))
    resultado = cursor.fetchone()

    conexao.close()
    return resultado

def editar_funcionario(id, nome, login, cargo, ano_admissao, salario, senha):
    conexao = sqlite.connect("database.sqlite")
    cursor = conexao.cursor()

    cursor.execute("""
                   UPDATE funcionario
                   SET nome = ?, login = ?, cargo = ?, ano_admissao = ?, salario = ?, senha = ?
                   WHERE id = ?
                   """, (nome, login, cargo, ano_admissao, salario, senha, id,))

    conexao.commit()
    conexao.close()

def aumentar_salario_todos(taxa):
    conexao = sqlite.connect("database.sqlite")
    cursor = conexao.cursor()

    cursor.execute("""
                   UPDATE funcionario
                   SET salario = salario * ?
                   """, (taxa,))
    
    conexao.commit()
    conexao.close()

def aumentar_salario_por_id(id, taxa):
    conexao = sqlite.connect("database.sqlite")
    cursor = conexao.cursor()

    cursor.execute("""
                   UPDATE funcionario
                   SET salario = salario * ?
                   WHERE id = ?
                   """, (taxa, id,))
    conexao.commit()
    conexao.close()

def adicionar_usuarios():
    conexao = sqlite.connect('database.sqlite')
    cursor = conexao.cursor()

    cargos = ["gerente", "caixa", "serviços gerais"]

    nomes = [
        "Ana Silva", "Pedro Martins", "Carla Souza", "João Almeida", "Mariana Castro",
        "Rafael Gomes", "Beatriz Rocha", "Lucas Fernandes", "Juliana Ribeiro",
        "Bruno Carvalho", "Patrícia Melo", "Diego Santos", "Aline Costa",
        "Felipe Nunes", "Camila Duarte"
    ]

    logins = [
        "anasil", "pmartins", "csouza", "jalmeida", "mcastro",
        "rgomes", "brocha", "lfernandes", "jribeiro",
        "bcarvalho", "pmelo", "dsantos", "acosta",
        "fnunes", "cduarte"
    ]

    for i in range(15):
        nome = nomes[i]
        login = logins[i]
        cargo = cargos[i % len(cargos)]
        ano_admissao = f"{2010 + (i % 10)}"
        salario = 2500 + (i * 150)
        senha = f"senha{i+1}"

        try:
            cursor.execute("""
                INSERT INTO funcionario (nome, login, cargo, ano_admissao, salario, senha)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (nome, login, cargo, ano_admissao, salario, senha))

        except sqlite.IntegrityError:
            print(f"⚠️ Login '{login}' já existe. Pulando...")

    conexao.commit()
    conexao.close()


