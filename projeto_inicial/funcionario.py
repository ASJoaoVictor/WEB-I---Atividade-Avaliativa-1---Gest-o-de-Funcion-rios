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
    
    @property
    def cargo(self):
        return self.__cargo
    
    @property
    def salario(self):
        return self.__salario
    
    @property
    def senha(self):
        return self.__senha