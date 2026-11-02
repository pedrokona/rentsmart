# utils.py
# Funções auxiliares de entrada de dados e formatação.
# Ficam separadas das classes para poderem ser reaproveitadas
# em qualquer parte do projeto (import from utils import ...).


def ler_texto(mensagem):
    """Lê um texto e não aceita que o usuário deixe em branco."""
    texto = input(mensagem).strip()
    while texto == "":
        print("  [!] Este campo não pode ficar vazio.")
        texto = input(mensagem).strip()
    return texto


def ler_inteiro(mensagem, minimo, maximo):
    """Lê um número inteiro e só aceita valores entre minimo e maximo."""
    while True:
        try:
            valor = int(input(mensagem))
            if valor >= minimo and valor <= maximo:
                return valor
            print(f"  [!] Digite um número entre {minimo} e {maximo}.")
        except ValueError:
            print("  [!] Valor inválido. Digite apenas números inteiros.")


def ler_sim_nao(mensagem):
    """Lê uma resposta S ou N e devolve True (sim) ou False (não)."""
    resposta = input(mensagem).strip().upper()
    while resposta != "S" and resposta != "N":
        print("  [!] Responda apenas com S (sim) ou N (não).")
        resposta = input(mensagem).strip().upper()
    return resposta == "S"


def formatar_moeda(valor):
    """Formata um número no padrão brasileiro: 1234.5 -> R$ 1.234,50"""
    if valor < 0:
        return "- " + formatar_moeda(-valor)
    texto = f"{valor:,.2f}"                     # 1,234.50 (padrão americano)
    texto = texto.replace(",", "X").replace(".", ",").replace("X", ".")
    return f"R$ {texto}"


def formatar_numero_csv(valor):
    """Número com vírgula decimal, para o Excel em português abrir certo."""
    return f"{valor:.2f}".replace(".", ",")
