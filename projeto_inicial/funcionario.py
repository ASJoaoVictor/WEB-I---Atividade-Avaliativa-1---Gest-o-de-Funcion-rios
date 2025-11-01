class Funcionario():
    def __init__(self, nome, login, cargo, salario, anoAdmissao, senha):
        self.nome = nome
        self.__login = login
        self.__cargo = cargo
        self.__salario = salario
        self.anoAdmissao = anoAdmissao
        self.__senha = senha

    @property
    def login(self):
        return self.__login

    @login.setter
    def login(self, value):
        self.__login = value

    @property
    def cargo(self):
        return self.__cargo

    @cargo.setter
    def cargo(self, value):
        self.__cargo = value

    @property
    def salario(self):
        return self.__salario

    @salario.setter
    def salario(self, value):
        self.__salario = value


    @property
    def senha(self):
        return self.__senha

    @senha.setter
    def senha(self, value):
        self.__senha = value

