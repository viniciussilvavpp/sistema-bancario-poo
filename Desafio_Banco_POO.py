from abc import ABC, abstractmethod
from datetime import datetime

class Transacao(ABC):
    @abstractmethod
    def registrar(self, conta):
        pass

    def obter_valor(self):
        pass

class Deposito(Transacao):
    def __init__(self, valor):
        self.__valor = valor

    def registrar(self, conta):
        conta._Conta__saldo += self.__valor
        conta._Conta__historico.adicionar_transacao(self)
        historico_global.adicionar_transacao(self, conta)
        print(f"Depósito de R$ {self.__valor:.2f} realizado com sucesso.")

    def obter_valor(self):
        return self.__valor

class Saque(Transacao):
    def __init__(self, valor):
        self.__valor = valor

    def registrar(self, conta):
        if conta.sacar(self.__valor):
            conta._Conta__historico.adicionar_transacao(self)
            historico_global.adicionar_transacao(self, conta)
            print(f"Saque de R$ {self.__valor:.2f} realizado com sucesso.")
        else:
            print("Saque não autorizado.")
    
    def obter_valor(self):
        return self.__valor

class Historico:
    def __init__(self):
        self.__transacoes = []

    def adicionar_transacao(self, transacao, conta=None):
        if conta:
            numero, agencia = conta.obter_dados_conta()
            self.__transacoes.append((datetime.now(), transacao, numero, agencia))
        else:
            self.__transacoes.append((datetime.now(), transacao))

    def exibir_historico(self):
        for item in self.__transacoes:
            if len(item) == 4:
                data, transacao, numero, agencia = item
                print(f"{data} - {transacao.__class__.__name__} - Valor: R$ {transacao.obter_valor():.2f} - Conta: {numero} (Agência: {agencia})")
            else:
                data, transacao = item
                print(f"{data} - {transacao.__class__.__name__} - Valor: R$ {transacao.obter_valor():.2f}")

class Conta:
    def __init__(self, cliente, numero, agencia):
        self.__saldo = 0.0
        self.__numero = numero
        self.__agencia = agencia
        self.__cliente = cliente
        self.__historico = Historico()

    def sacar(self, valor):
        if valor > 0 and valor <= self.__saldo:
            self.__saldo -= valor
            return True
        return False

    def depositar(self, valor):
        if valor > 0:
            self.__saldo += valor
            return True
        return False

    def exibir_saldo(self):
        print(f"Saldo atual: R$ {self.__saldo:.2f}")

    def obter_historico(self):
        return self.__historico
    
    def obter_dados_conta(self):
        return self.__numero, self.__agencia

class ContaCorrente(Conta):
    def __init__(self, cliente, numero, agencia, limite=500, limite_saques=3):
        super().__init__(cliente, numero, agencia)
        self.__limite = limite
        self.__limite_saques = limite_saques
        self.__saques_realizados = 0
        self.__ultima_data_saque = None

    def sacar(self, valor):
        hoje = datetime.now().date()
        if self.__ultima_data_saque != hoje:
            self.__saques_realizados = 0
            self.__ultima_data_saque = hoje

        if self.__saques_realizados < self.__limite_saques and valor <= self.__limite:
            if super().sacar(valor):
                self.__saques_realizados += 1
                return True
        return False

class Cliente:
    def __init__(self, endereco):
        self.__endereco = endereco
        self.__contas = []

    def adicionar_conta(self, conta):
        self.__contas.append(conta)

    def realizar_transacao(self, conta, transacao):
        if conta in self.__contas:
            transacao.registrar(conta)
        else:
            print("Conta não pertence ao cliente.")

    def obter_contas(self):
        return self.__contas

class PessoaFisica(Cliente):
    def __init__(self, nome, cpf, data_nascimento, endereco):
        super().__init__(endereco)
        self.__nome = nome
        self.__cpf = cpf
        self.__data_nascimento = data_nascimento

clientes = []
historico_global = Historico()

def cadastrar_cliente():
    nome = input("Nome: ")
    cpf = input("CPF: ")
    data_nascimento = input("Data de Nascimento: ")
    endereco = input("Endereço: ")
    cliente = PessoaFisica(nome, cpf, data_nascimento, endereco)
    clientes.append(cliente)
    print("Cliente cadastrado com sucesso!")

def criar_conta():
    cpf = input("Digite o CPF do cliente: ")
    cliente = next((c for c in clientes if c._PessoaFisica__cpf == cpf), None)
    if cliente:
        numero = len(cliente.obter_contas()) + 1
        conta = ContaCorrente(cliente, numero, "001")
        cliente.adicionar_conta(conta)
        print("Nova conta criada com sucesso!")
    else:
        print("Cliente não encontrado.")

def listar_contas():
    cpf = input("Digite o CPF do cliente: ")
    cliente = next((c for c in clientes if c._PessoaFisica__cpf == cpf), None)
    if cliente:
        print("\nContas do Cliente:")
        for conta in cliente.obter_contas():
            numero, agencia = conta.obter_dados_conta()
            print(f"Número: {numero}, Agência: {agencia}")
    else:
        print("Cliente não encontrado.")

def buscar_conta(cliente, agencia, numero):
    for conta in cliente.obter_contas():
        num, ag = conta.obter_dados_conta()
        if str(num) == str(numero) and ag == agencia:
            return conta
    return None

def fazer_deposito():
    cpf = input("Digite o CPF do cliente: ")
    cliente = next((c for c in clientes if c._PessoaFisica__cpf == cpf), None)
    if cliente:
        agencia = input("Digite o número da agência: ")
        numero = input("Digite o número da conta: ")
        conta = buscar_conta(cliente, agencia, numero)
        if conta:
            try:
                valor = float(input("Valor do depósito: "))
                if valor > 0:
                    transacao = Deposito(valor)
                    cliente.realizar_transacao(conta, transacao)
                    conta.exibir_saldo()
                else:
                    print("Valor deve ser positivo!")
            except ValueError:
                print("Valor inválido! Digite um número.")
        else:
            print("Conta não encontrada.")
    else:
        print("Cliente não encontrado.")

def fazer_saque():
    cpf = input("Digite o CPF do cliente: ")
    cliente = next((c for c in clientes if c._PessoaFisica__cpf == cpf), None)
    if cliente:
        agencia = input("Digite o número da agência: ")
        numero = input("Digite o número da conta: ")
        conta = buscar_conta(cliente, agencia, numero)
        if conta:
            try:
                valor = float(input("Valor do saque: "))
                if valor > 0:
                    transacao = Saque(valor)
                    cliente.realizar_transacao(conta, transacao)
                    conta.exibir_saldo()
                else:
                    print("Valor deve ser positivo!")
            except ValueError:
                print("Valor inválido! Digite um número.")
        else:
            print("Conta não encontrada.")
    else:
        print("Cliente não encontrado.")

def verificar_saldo():
    cpf = input("Digite o CPF do cliente: ")
    cliente = next((c for c in clientes if c._PessoaFisica__cpf == cpf), None)
    if cliente:
        agencia = input("Digite o número da agência: ")
        numero = input("Digite o número da conta: ")
        conta = buscar_conta(cliente, agencia, numero)
        if conta:
            print(f"\nInformações da Conta {numero} (Agência {agencia}):")
            conta.exibir_saldo()
        else:
            print("Conta não encontrada.")
    else:
        print("Cliente não encontrado.")

def exibir_historico():
    print("\nHistórico de todas as transações realizadas:")
    if historico_global._Historico__transacoes:
        historico_global.exibir_historico()
    else:
        print("Nenhuma transação registrada ainda.")

def menu():
    while True:
        print("\n--- MENU ---")
        print("1. Cadastrar Cliente")
        print("2. Criar Nova Conta")
        print("3. Listar Contas do Cliente")
        print("4. Fazer Depósito")
        print("5. Fazer Saque")
        print("6. Exibir Histórico Geral")
        print("7. Verificar Saldo")
        print("8. Sair")
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            cadastrar_cliente()
        elif opcao == "2":
            criar_conta()
        elif opcao == "3":
            listar_contas()
        elif opcao == "4":
            fazer_deposito()
        elif opcao == "5":
            fazer_saque()
        elif opcao == "6":
            exibir_historico()
        elif opcao == "7":
            verificar_saldo()
        elif opcao == "8":
            print("Saindo...")
            break
        else:
            print("Opção inválida!")

menu()