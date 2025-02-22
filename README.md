# Sistema Bancário em Python

Este projeto implementa um sistema bancário simples em Python, utilizando os conceitos de Programação Orientada a Objetos (POO). O sistema permite o cadastro de clientes, criação de contas, realização de transações financeiras (depósitos e saques) e consulta de histórico de transações.

## Funcionalidades

- **Cadastro de Clientes:** Permite cadastrar clientes com nome, CPF, data de nascimento e endereço.
- **Criação de Contas:** Cria contas correntes associadas aos clientes cadastrados.
- **Depósitos:** Realiza depósitos nas contas, registrando a transação no histórico.
- **Saques:** Efetua saques, respeitando o limite diário e o saldo disponível.
- **Consulta de Saldo:** Exibe o saldo atual da conta.
- **Histórico de Transações:** Mostra todas as transações realizadas no sistema.

## Estrutura do Projeto

- **Transacao:** Classe abstrata para operações financeiras, com heranças para **Deposito** e **Saque**.
- **Conta:** Classe base para gerenciar saldo e transações.
- **ContaCorrente:** Especialização da classe **Conta**, com limites de saque diário.
- **Cliente:** Armazena dados do cliente e associa contas bancárias.
- **PessoaFisica:** Subclasse de **Cliente**, destinada a clientes pessoa física.
- **Historico:** Registra as transações de cada conta e o histórico global.

## Requisitos

- Python 3.x

## Como Executar

1. Clone o repositório:
```bash
git clone https://github.com/viniciussilvavpp/sistema-bancario-poo.git
```
2. Navegue até o diretório do projeto:
```bash
cd sistema-bancario
```
3. Execute o script principal:
```bash
python sistema_bancario.py
```

## Uso

Ao executar o programa, o menu exibirá as opções disponíveis:

1. Cadastrar Cliente
2. Criar Nova Conta
3. Listar Contas do Cliente
4. Fazer Depósito
5. Fazer Saque
6. Exibir Histórico Geral
7. Verificar Saldo
8. Sair

Basta selecionar a opção desejada e seguir as instruções fornecidas pelo programa.

## Exemplo de Uso

Para realizar um depósito, siga estas etapas:
- Selecione a opção "4. Fazer Depósito".
- Informe o CPF do cliente.
- Informe o número da agência e da conta.
- Digite o valor do depósito.
- O saldo atualizado será exibido.

## Licença

Este projeto é de uso livre e aberto sob a licença MIT.

