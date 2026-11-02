# main.py
# RentSmart - Sistema de Orçamento de Locação da R.M Imóveis
# Ponto de entrada do programa: conversa com o usuário, cria os
# objetos e pede para eles calcularem e exibirem o orçamento.

import os

from modelos import Cliente, Apartamento, Casa, Estudio, TaxaContratual, Orcamento
from utils import ler_texto, ler_inteiro, ler_sim_nao, formatar_moeda

PASTA_SAIDA = "orcamentos"

# Tabela usada no menu: opção -> (nome, aluguel-base)
# Os valores vêm das próprias classes, assim o preço fica em um só lugar.
TIPOS_DE_IMOVEL = {
    1: ("Apartamento", Apartamento.ALUGUEL_BASE),
    2: ("Casa", Casa.ALUGUEL_BASE),
    3: ("Estúdio", Estudio.ALUGUEL_BASE),
}


def exibir_cabecalho():
    print()
    print("=" * 56)
    print("RENTSMART".center(56))
    print("Sistema de Orçamento de Locação - R.M Imóveis".center(56))
    print("=" * 56)


def escolher_tipo_imovel():
    print("\nTipos de imóvel disponíveis:")
    for opcao, dados in TIPOS_DE_IMOVEL.items():
        nome, aluguel = dados
        print(f"  {opcao} - {nome:<12} (aluguel-base {formatar_moeda(aluguel)})")
    return ler_inteiro("Escolha o tipo de imóvel (1-3): ", 1, 3)


def montar_imovel(tipo, cliente):
    """Faz as perguntas específicas de cada tipo e devolve o objeto do imóvel."""
    if tipo == 1 or tipo == 2:
        quartos = ler_inteiro("Quantidade de quartos (1 ou 2): ", 1, 2)
        garagem = ler_sim_nao("Deseja vaga de garagem? +R$ 300,00 (S/N): ")
        if tipo == 1:
            # A pergunta sobre crianças só interessa para apartamento
            cliente.possui_criancas = ler_sim_nao("O cliente possui crianças? (S/N): ")
            return Apartamento(quartos, garagem)
        return Casa(quartos, garagem)

    # tipo == 3 -> Estúdio
    estacionamento = ler_sim_nao("Deseja estacionamento? Pacote 2 vagas +R$ 250,00 (S/N): ")
    vagas_adicionais = 0
    if estacionamento:
        vagas_adicionais = ler_inteiro("Quantas vagas ADICIONAIS além das 2 do pacote? "
                                       "(R$ 60,00 cada, 0 a 10): ", 0, 10)
    return Estudio(estacionamento, vagas_adicionais)


def nome_do_arquivo(nome_cliente):
    """Gera um nome de arquivo simples a partir do nome do cliente."""
    nome = ""
    for letra in nome_cliente.lower():
        if letra.isalnum():
            nome += letra
        elif letra == " ":
            nome += "_"
    if nome == "":
        nome = "cliente"
    return f"projecao_12_meses_{nome}.csv"


def novo_orcamento():
    nome = ler_texto("\nNome do cliente: ")
    cliente = Cliente(nome)

    tipo = escolher_tipo_imovel()
    imovel = montar_imovel(tipo, cliente)

    print("\nTaxa contratual: R$ 2.000,00 (pode ser parcelada em até 5x)")
    parcelas = ler_inteiro("Em quantas parcelas deseja pagar a taxa? (1-5): ", 1, 5)
    taxa = TaxaContratual(parcelas)

    orcamento = Orcamento(cliente, imovel, taxa)
    orcamento.exibir_resumo()

    try:
        os.makedirs(PASTA_SAIDA, exist_ok=True)
        caminho = os.path.join(PASTA_SAIDA, nome_do_arquivo(cliente.nome))
        orcamento.exportar_csv(caminho)
        print(f"\nProjeção de 12 meses salva em: {caminho}")
    except PermissionError:
        print("\n[!] Não foi possível salvar o CSV. Verifique se o arquivo "
              "não está aberto em outro programa (ex.: Excel).")
    except OSError as erro:
        print(f"\n[!] Erro ao salvar o arquivo CSV: {erro}")


def main():
    exibir_cabecalho()
    continuar = True
    while continuar:
        novo_orcamento()
        continuar = ler_sim_nao("\nDeseja fazer outro orçamento? (S/N): ")
    print("\nObrigado por usar o RentSmart!")


if __name__ == "__main__":
    main()
