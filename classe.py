from abc import ABC, abstractmethod


class ContaBancaria(ABC):

    def __init__(self, nome_cliente, valor_inicial=0):
        self.titular = nome_cliente
        self.saldo = valor_inicial

    @property
    def titular(self):
        return self._titular

    @titular.setter
    def titular(self, nome):
        if not isinstance(nome, str) or len(nome.strip()) == 0:
            raise ValueError("Nome do titular inválido.")

        self._titular = nome.strip()

    @property
    def saldo(self):
        return self._saldo

    @saldo.setter
    def saldo(self, valor):
        if not isinstance(valor, (int, float)) or valor < 0:
            raise ValueError("O saldo não pode ser negativo.")

        self._saldo = valor

    def depositar(self, quantia):
        if not isinstance(quantia, (int, float)) or quantia <= 0:
            raise ValueError("O valor do depósito deve ser positivo.")

        self._saldo += quantia

    def sacar(self, quantia):
        if not isinstance(quantia, (int, float)) or quantia <= 0:
            raise ValueError("O valor do saque deve ser positivo.")

        if quantia > self._saldo:
            raise ValueError("Não há saldo suficiente.")

        self._saldo -= quantia

    @abstractmethod
    def rendimento(self):
        pass

    def __str__(self):
        return (
            f"Cliente: {self.titular} | "
            f"Conta: {type(self).__name__} | "
            f"Saldo: R$ {self.saldo:.2f}"
        )

    def __repr__(self):
        return (
            f"{type(self).__name__}"
            f"({self.titular!r}, {self.saldo!r})"
        )

    def __eq__(self, outra_conta):
        if not isinstance(outra_conta, ContaBancaria):
            return NotImplemented

        return (
            type(self) == type(outra_conta)
            and self.titular == outra_conta.titular
            and self.saldo == outra_conta.saldo
        )


class ContaCorrente(ContaBancaria):

    def __init__(self,
                  nome_cliente, valor_inicial=0, tarifa=12):
        super().__init__(nome_cliente, valor_inicial)
        self.tarifa = tarifa

    @property
    def tarifa(self):
        return self._tarifa

    @tarifa.setter
    def tarifa(self, valor):
        if not isinstance(valor, (int, float)) or valor < 0:
            raise ValueError("Tarifa inválida.")

        self._tarifa = valor

    def rendimento(self):
        return -self.tarifa


class ContaPoupanca(ContaBancaria):

    def __init__(self, nome_cliente, valor_inicial=0, percentual=0.006):
        super().__init__(nome_cliente, valor_inicial)
        self.percentual = percentual

    @property
    def percentual(self):
        return self._percentual

    @percentual.setter
    def percentual(self, valor):
        if not isinstance(valor, (int, float)) or valor < 0:
            raise ValueError("Percentual de juros inválido.")

        self._percentual = valor

    def rendimento(self):
        return self.saldo * self.percentual


class InstituicaoFinanceira:

    def __init__(self, nome_banco):
        self.nome = nome_banco
        self.lista_contas = []

    def cadastrar_conta(self, conta):
        if not isinstance(conta, ContaBancaria):
            raise TypeError("É necessário informar uma conta bancária.")

        self.lista_contas.append(conta)

    def mostrar_contas(self):
        if not self.lista_contas:
            print("Nenhuma conta cadastrada.")
            return

        for conta in self.lista_contas:
            print(conta)

    def saldo_geral(self):
        total = 0

        for conta in self.lista_contas:
            total += conta.saldo

        return total

    def __len__(self):
        return len(self.lista_contas)

    def __str__(self):
        return (
            f"{self.nome} - "
            f"{len(self)} contas cadastradas"
        )

    def __repr__(self):
        return f"InstituicaoFinanceira({self.nome!r})"


def executar():

    banco = InstituicaoFinanceira("Banco Digital")

    clientes = [
        ContaCorrente("Mariana", 1300),
        ContaPoupanca("Rafael", 2200),
        ContaCorrente("Lucas", 1750),
        ContaPoupanca("Beatriz", 3200),
        ContaCorrente("Rodrigo", 950),
        ContaPoupanca("Camila", 2700),
        ContaCorrente("Thiago", 1100),
        ContaPoupanca("Larissa", 4100),
        ContaCorrente("Pedro", 850),
        ContaPoupanca("Sofia", 3600)
    ]

    for conta in clientes:
        banco.cadastrar_conta(conta)

    print("\n========== LISTA DE CONTAS ==========")
    banco.mostrar_contas()

    print("\n========== RENDIMENTOS ==========")

    for conta in banco.lista_contas:
        resultado = conta.rendimento()

        print(
            f"{conta.titular}: "
            f"R$ {resultado:.2f}"
        )

    print("\n========== MOVIMENTAÇÕES ==========")

    clientes[0].depositar(350)
    print(f"Depois do depósito: {clientes[0]}")

    clientes[1].sacar(150)
    print(f"Depois do saque: {clientes[1]}")

    print("\n========== MÉTODOS ESPECIAIS ==========")

    print("STR:", str(clientes[0]))
    print("REPR:", repr(clientes[1]))
    print(
        "As contas são iguais?",
        clientes[0] == clientes[1]
    )
    print("Número de contas:", len(banco))

    print("\n========== TESTES DE ERROS ==========")

    try:
        clientes[2].sacar(10000)
    except ValueError as erro:
        print("Saque:", erro)

    try:
        clientes[3].saldo = -500
    except ValueError as erro:
        print("Saldo:", erro)

    try:
        clientes[4].depositar(0)
    except ValueError as erro:
        print("Depósito:", erro)

    try:
        clientes[5].titular = "   "
    except ValueError as erro:
        print("Titular:", erro)

    try:
        banco.cadastrar_conta("conta inválida")
    except TypeError as erro:
        print("Cadastro:", erro)

    print("\n========== RESUMO ==========")
    print(banco)

    total = banco.saldo_geral()

    print(f"Valor total armazenado: R$ {total:.2f}")


if __name__ == "__main__":
    executar()