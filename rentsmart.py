"""
RentSmart - Sistema de Orçamento de Locação
Execute: python rentsmart.py
Requer Python 3.8 ou superior. Usa apenas bibliotecas padrão.
"""
from abc import ABC, abstractmethod
import csv
from pathlib import Path


class Imovel(ABC):
    def __init__(self, quartos, aluguel_base):
        self.quartos = quartos
        self.aluguel_base = aluguel_base

    @abstractmethod
    def calcular_adicional_quartos(self):
        raise NotImplementedError

    @abstractmethod
    def calcular_estacionamento(self, quantidade_vagas):
        raise NotImplementedError


class Apartamento(Imovel):
    def __init__(self, quartos):
        super().__init__(quartos, 700.00)

    def calcular_adicional_quartos(self):
        return 200.00 if self.quartos == 2 else 0.00

    def calcular_estacionamento(self, quantidade_vagas):
        return 300.00 if quantidade_vagas == 1 else 0.00


class Casa(Imovel):
    def __init__(self, quartos):
        super().__init__(quartos, 900.00)

    def calcular_adicional_quartos(self):
        return 250.00 if self.quartos == 2 else 0.00

    def calcular_estacionamento(self, quantidade_vagas):
        return 300.00 if quantidade_vagas == 1 else 0.00


class Estudio(Imovel):
    def __init__(self):
        super().__init__(0, 1200.00)

    def calcular_adicional_quartos(self):
        return 0.00

    def calcular_estacionamento(self, quantidade_vagas):
        if quantidade_vagas == 0:
            return 0.00
        if quantidade_vagas <= 2:
            return 250.00
        return 250.00 + (quantidade_vagas - 2) * 60.00


class Orcamento:
    TAXA_CONTRATUAL = 2000.00
    DESCONTO_APARTAMENTO_SEM_CRIANCAS = 0.05

    def __init__(self, imovel, quantidade_vagas, possui_criancas, parcelas_taxa):
        self.imovel = imovel
        self.quantidade_vagas = quantidade_vagas
        self.possui_criancas = possui_criancas
        self.parcelas_taxa = parcelas_taxa
        self.aluguel_base = imovel.aluguel_base
        self.adicional_quartos = imovel.calcular_adicional_quartos()
        self.adicional_estacionamento = imovel.calcular_estacionamento(quantidade_vagas)
        self.subtotal = self.aluguel_base + self.adicional_quartos + self.adicional_estacionamento

        self.desconto = 0.00
        if isinstance(imovel, Apartamento) and not possui_criancas:
            self.desconto = self.subtotal * self.DESCONTO_APARTAMENTO_SEM_CRIANCAS

        self.aluguel_mensal = self.subtotal - self.desconto
        self.valor_parcela_taxa = self.TAXA_CONTRATUAL / self.parcelas_taxa

    def gerar_projecao(self, quantidade_meses=12):
        linhas = []
        for mes in range(1, quantidade_meses + 1):
            parcela = self.valor_parcela_taxa if mes <= self.parcelas_taxa else 0.00
            linhas.append({
                "mes": mes,
                "aluguel": round(self.aluguel_mensal, 2),
                "parcela_taxa": round(parcela, 2),
                "total_mes": round(self.aluguel_mensal + parcela, 2)
            })
        return linhas

    def exibir_resumo(self):
        print("\n" + "=" * 50)
        print("             ORÇAMENTO RENTSMART")
        print("=" * 50)
        print(f"Aluguel-base:                 R$ {self.aluguel_base:,.2f}")
        print(f"Adicional de quartos:         R$ {self.adicional_quartos:,.2f}")
        print(f"Adicional de estacionamento: R$ {self.adicional_estacionamento:,.2f}")
        print(f"Subtotal antes do desconto:   R$ {self.subtotal:,.2f}")
        print(f"Desconto aplicado:            R$ {self.desconto:,.2f}")
        print("-" * 50)
        print(f"ALUGUEL MENSAL:                R$ {self.aluguel_mensal:,.2f}")
        print("-" * 50)
        print(f"Taxa contratual:              R$ {self.TAXA_CONTRATUAL:,.2f}")
        print(f"Parcelamento:                 {self.parcelas_taxa}x de R$ {self.valor_parcela_taxa:,.2f}")
        print("A taxa contratual é separada do aluguel mensal.")
        print("=" * 50)


def ler_inteiro(mensagem, minimo, maximo=None):
    while True:
        try:
            valor = int(input(mensagem))
            if valor < minimo or (maximo is not None and valor > maximo):
                limite = f" e no máximo {maximo}" if maximo is not None else ""
                print(f"Informe um número a partir de {minimo}{limite}.")
                continue
            return valor
        except ValueError:
            print("Entrada inválida. Digite um número inteiro.")


def ler_sim_nao(mensagem):
    while True:
        resposta = input(mensagem).strip().lower()
        if resposta in ("s", "sim"):
            return True
        if resposta in ("n", "nao", "não"):
            return False
        print("Digite S para sim ou N para não.")


def escolher_imovel():
    print("\nTIPO DE IMÓVEL")
    print("1 - Apartamento")
    print("2 - Casa")
    print("3 - Estúdio")
    opcao = ler_inteiro("Escolha uma opção: ", 1, 3)

    if opcao == 1:
        quartos = ler_inteiro("Quantidade de quartos (1 ou 2): ", 1, 2)
        return Apartamento(quartos), "Apartamento"
    if opcao == 2:
        quartos = ler_inteiro("Quantidade de quartos (1 ou 2): ", 1, 2)
        return Casa(quartos), "Casa"
    return Estudio(), "Estúdio"


def coletar_dados():
    imovel, tipo_nome = escolher_imovel()
    if isinstance(imovel, Estudio):
        vagas = ler_inteiro("Quantidade de vagas (0 ou mais): ", 0)
    else:
        vagas = ler_inteiro("Garagem? 0 - Não / 1 - Sim: ", 0, 1)

    if isinstance(imovel, Apartamento):
        possui_criancas = ler_sim_nao("O cliente possui crianças? (S/N): ")
    else:
        possui_criancas = True

    parcelas = ler_inteiro("Em quantas parcelas deseja pagar a taxa (1 a 5)? ", 1, 5)
    return imovel, tipo_nome, vagas, possui_criancas, parcelas


def salvar_csv(orcamento, tipo_nome, caminho="projecao_rentsmart.csv"):
    caminho = Path(caminho)
    with caminho.open("w", newline="", encoding="utf-8-sig") as arquivo:
        campos = ["Mes", "Tipo de imovel", "Aluguel mensal (R$)",
                  "Parcela da taxa contratual (R$)", "Total previsto no mes (R$)"]
        escritor = csv.DictWriter(arquivo, fieldnames=campos, delimiter=";")
        escritor.writeheader()
        for linha in orcamento.gerar_projecao(12):
            escritor.writerow({
                "Mes": linha["mes"],
                "Tipo de imovel": tipo_nome,
                "Aluguel mensal (R$)": f'{linha["aluguel"]:.2f}'.replace(".", ","),
                "Parcela da taxa contratual (R$)": f'{linha["parcela_taxa"]:.2f}'.replace(".", ","),
                "Total previsto no mes (R$)": f'{linha["total_mes"]:.2f}'.replace(".", ",")
            })
    return caminho


def main():
    print("=" * 50)
    print(" BEM-VINDO AO RENTSMART - R.M IMÓVEIS")
    print("=" * 50)
    imovel, tipo_nome, vagas, possui_criancas, parcelas = coletar_dados()
    orcamento = Orcamento(imovel, vagas, possui_criancas, parcelas)
    orcamento.exibir_resumo()
    arquivo = salvar_csv(orcamento, tipo_nome)
    print(f"\nArquivo CSV gerado com sucesso: {arquivo.resolve()}")
    print("A projeção contém os 12 meses da locação.")


if __name__ == "__main__":
    main()
