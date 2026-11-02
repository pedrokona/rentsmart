# modelos.py
# Classes que representam as entidades do sistema RentSmart.

import csv

from utils import formatar_moeda, formatar_numero_csv


# ---------------------------------------------------------------
# Cliente
# ---------------------------------------------------------------
class Cliente:
    def __init__(self, nome, possui_criancas=True):
        self.nome = nome
        self.possui_criancas = possui_criancas

    def __str__(self):
        return self.nome


# ---------------------------------------------------------------
# Imóveis
# ---------------------------------------------------------------
class Imovel:
    """Classe base (molde geral). Guarda o que todo imóvel tem em comum:
    o tipo e o aluguel-base. Cada tipo de imóvel completa as regras
    que são só dele."""

    def __init__(self, tipo, aluguel_base):
        self.tipo = tipo
        self.aluguel_base = aluguel_base

    def calcular_adicionais(self):
        """Devolve uma lista de tuplas (descrição, valor).
        Por padrão o imóvel não tem adicionais."""
        return []

    def calcular_desconto(self, cliente, subtotal):
        """Por padrão não existe desconto."""
        return 0.0

    def descrever(self):
        return self.tipo

    def __str__(self):
        return self.descrever()


class ImovelComQuartos(Imovel):
    """Casas e apartamentos funcionam do mesmo jeito: podem ter 1 ou 2
    quartos e podem ter 1 vaga de garagem. Só muda o valor do 2º quarto.
    Por isso essa lógica fica aqui, escrita uma única vez."""

    VALOR_GARAGEM = 300.0

    def __init__(self, tipo, aluguel_base, valor_segundo_quarto, quartos, garagem):
        super().__init__(tipo, aluguel_base)
        if quartos != 1 and quartos != 2:
            raise ValueError("A quantidade de quartos deve ser 1 ou 2.")
        self.valor_segundo_quarto = valor_segundo_quarto
        self.quartos = quartos
        self.garagem = garagem

    def calcular_adicionais(self):
        adicionais = []
        if self.quartos == 2:
            adicionais.append(("Adicional 2º quarto", self.valor_segundo_quarto))
        if self.garagem:
            adicionais.append(("Vaga de garagem", self.VALOR_GARAGEM))
        return adicionais

    def descrever(self):
        texto = f"{self.tipo} - {self.quartos} quarto(s)"
        if self.garagem:
            texto += " - com garagem"
        else:
            texto += " - sem garagem"
        return texto


class Apartamento(ImovelComQuartos):
    ALUGUEL_BASE = 700.0
    VALOR_SEGUNDO_QUARTO = 200.0
    PERCENTUAL_DESCONTO = 0.05   # 5% para quem não tem crianças

    def __init__(self, quartos, garagem):
        super().__init__("Apartamento", self.ALUGUEL_BASE, self.VALOR_SEGUNDO_QUARTO,
                         quartos, garagem)

    def calcular_desconto(self, cliente, subtotal):
        # Regra exclusiva do apartamento: 5% sobre o aluguel já com os
        # adicionais, somente se o cliente NÃO possui crianças.
        if not cliente.possui_criancas:
            return round(subtotal * self.PERCENTUAL_DESCONTO, 2)
        return 0.0


class Casa(ImovelComQuartos):
    ALUGUEL_BASE = 900.0
    VALOR_SEGUNDO_QUARTO = 250.0

    def __init__(self, quartos, garagem):
        super().__init__("Casa", self.ALUGUEL_BASE, self.VALOR_SEGUNDO_QUARTO,
                         quartos, garagem)


class Estudio(Imovel):
    ALUGUEL_BASE = 1200.0
    VALOR_PACOTE_VAGAS = 250.0   # pacote inicial com 2 vagas
    VAGAS_NO_PACOTE = 2
    VALOR_VAGA_EXTRA = 60.0

    def __init__(self, estacionamento, vagas_adicionais=0):
        super().__init__("Estúdio", self.ALUGUEL_BASE)
        if vagas_adicionais < 0:
            raise ValueError("A quantidade de vagas adicionais não pode ser negativa.")
        self.estacionamento = estacionamento
        # Sem estacionamento não faz sentido ter vagas adicionais
        if estacionamento:
            self.vagas_adicionais = vagas_adicionais
        else:
            self.vagas_adicionais = 0

    def total_vagas(self):
        if not self.estacionamento:
            return 0
        return self.VAGAS_NO_PACOTE + self.vagas_adicionais

    def calcular_adicionais(self):
        adicionais = []
        if self.estacionamento:
            adicionais.append(("Pacote estacionamento (2 vagas)", self.VALOR_PACOTE_VAGAS))
            if self.vagas_adicionais > 0:
                valor = self.vagas_adicionais * self.VALOR_VAGA_EXTRA
                descricao = (f"{self.vagas_adicionais} vaga(s) adicional(is) x "
                             f"{formatar_moeda(self.VALOR_VAGA_EXTRA)}")
                adicionais.append((descricao, valor))
        return adicionais

    def descrever(self):
        if self.estacionamento:
            return f"{self.tipo} - {self.total_vagas()} vaga(s) de estacionamento"
        return f"{self.tipo} - sem estacionamento"


# ---------------------------------------------------------------
# Taxa contratual
# ---------------------------------------------------------------
class TaxaContratual:
    VALOR_PADRAO = 2000.0
    MAXIMO_PARCELAS = 5

    def __init__(self, parcelas, valor=VALOR_PADRAO):
        if parcelas < 1 or parcelas > self.MAXIMO_PARCELAS:
            raise ValueError(f"A taxa pode ser parcelada de 1 a {self.MAXIMO_PARCELAS} vezes.")
        self.valor = valor
        self.parcelas = parcelas

    def valores_das_parcelas(self):
        """Divide a taxa em parcelas. Quando a divisão não é exata
        (ex.: 2000 / 3), a última parcela recebe o ajuste dos centavos
        para que a soma feche exatamente no valor da taxa."""
        valor_parcela = round(self.valor / self.parcelas, 2)
        lista = []
        for i in range(self.parcelas - 1):
            lista.append(valor_parcela)
        ultima = round(self.valor - valor_parcela * (self.parcelas - 1), 2)
        lista.append(ultima)
        return lista

    def parcela_do_mes(self, mes):
        """Valor da taxa cobrado no mês informado (1 a 12)."""
        if mes <= self.parcelas:
            return self.valores_das_parcelas()[mes - 1]
        return 0.0

    def __str__(self):
        if self.parcelas == 1:
            return f"À vista: {formatar_moeda(self.valor)}"
        return f"{self.parcelas}x de {formatar_moeda(self.valores_das_parcelas()[0])}"


# ---------------------------------------------------------------
# Orçamento
# ---------------------------------------------------------------
class Orcamento:
    MESES_PROJECAO = 12

    def __init__(self, cliente, imovel, taxa):
        self.cliente = cliente
        self.imovel = imovel
        self.taxa = taxa

    # ----- cálculos -----
    def calcular_subtotal(self):
        """Aluguel-base + todos os adicionais do imóvel."""
        total = self.imovel.aluguel_base
        for descricao, valor in self.imovel.calcular_adicionais():
            total += valor
        return round(total, 2)

    def calcular_desconto(self):
        return self.imovel.calcular_desconto(self.cliente, self.calcular_subtotal())

    def calcular_aluguel_mensal(self):
        return round(self.calcular_subtotal() - self.calcular_desconto(), 2)

    def gerar_projecao(self):
        """Monta uma lista com um dicionário para cada mês do 1º ano."""
        projecao = []
        aluguel = self.calcular_aluguel_mensal()
        acumulado = 0.0
        for mes in range(1, self.MESES_PROJECAO + 1):
            parcela = self.taxa.parcela_do_mes(mes)
            total_mes = round(aluguel + parcela, 2)
            acumulado = round(acumulado + total_mes, 2)
            projecao.append({
                "mes": mes,
                "aluguel": aluguel,
                "parcela_taxa": parcela,
                "total_mes": total_mes,
                "acumulado": acumulado,
            })
        return projecao

    # ----- saídas -----
    def exibir_resumo(self):
        largura = 56
        print()
        print("=" * largura)
        print("RENTSMART - ORÇAMENTO DE LOCAÇÃO".center(largura))
        print("R.M Imóveis".center(largura))
        print("=" * largura)
        print(f"Cliente: {self.cliente}")
        print(f"Imóvel : {self.imovel}")
        print("-" * largura)

        print("ALUGUEL MENSAL")
        self._linha(f"Aluguel-base ({self.imovel.tipo})", self.imovel.aluguel_base, largura)
        for descricao, valor in self.imovel.calcular_adicionais():
            self._linha(descricao, valor, largura)
        self._linha("Subtotal", self.calcular_subtotal(), largura)

        desconto = self.calcular_desconto()
        if desconto > 0:
            self._linha("Desconto 5% (cliente sem crianças)", -desconto, largura)
        self._linha(">> VALOR MENSAL DO ALUGUEL", self.calcular_aluguel_mensal(), largura)
        print("-" * largura)

        print("TAXA CONTRATUAL (cobrada separadamente do aluguel)")
        self._linha("Valor total da taxa", self.taxa.valor, largura)
        print(f"  Condição escolhida: {self.taxa}")
        parcelas = self.taxa.valores_das_parcelas()
        for i in range(len(parcelas)):
            self._linha(f"   Parcela {i + 1}/{len(parcelas)} (mês {i + 1})", parcelas[i], largura)
        print("-" * largura)

        projecao = self.gerar_projecao()
        total_alugueis = self.calcular_aluguel_mensal() * self.MESES_PROJECAO
        print("RESUMO DO 1º ANO DE CONTRATO")
        self._linha("Aluguéis (12 meses)", total_alugueis, largura)
        self._linha("Taxa contratual", self.taxa.valor, largura)
        self._linha("TOTAL PREVISTO NO 1º ANO", projecao[-1]["acumulado"], largura)
        print("=" * largura)

    def _linha(self, descricao, valor, largura):
        """Imprime 'descrição ........ valor' alinhado à direita."""
        valor_txt = formatar_moeda(valor)
        espacos = largura - len(descricao) - len(valor_txt) - 2
        print("  " + descricao + " " * max(espacos, 1) + valor_txt)

    def exportar_csv(self, caminho):
        """Grava a projeção de 12 meses em um arquivo CSV."""
        with open(caminho, "w", newline="", encoding="utf-8-sig") as arquivo:
            escritor = csv.writer(arquivo, delimiter=";")
            escritor.writerow(["Mês", "Aluguel (R$)", "Parcela taxa contratual (R$)",
                               "Total do mês (R$)", "Total acumulado (R$)"])
            for linha in self.gerar_projecao():
                escritor.writerow([
                    linha["mes"],
                    formatar_numero_csv(linha["aluguel"]),
                    formatar_numero_csv(linha["parcela_taxa"]),
                    formatar_numero_csv(linha["total_mes"]),
                    formatar_numero_csv(linha["acumulado"]),
                ])
        return caminho
