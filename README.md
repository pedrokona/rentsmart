# RentSmart — Sistema de Orçamento de Locação

Aplicação em Python, desenvolvida com Programação Orientada a Objetos, que calcula
automaticamente o orçamento de locação da **R.M Imóveis**: aluguel mensal com adicionais e
descontos, taxa contratual parcelada e projeção dos 12 primeiros meses em um arquivo CSV.

Trabalho da disciplina *Algorithmic Thinking & Introduction to Object-Oriented Programming*.

## Requisitos

- Python 3.8 ou superior
- Nenhuma biblioteca externa (usa só `csv` e `os`, que já vêm com o Python)

## Como executar

1. Baixe ou clone o repositório:
   ```bash
   git clone https://github.com/pedrokona/rentsmart.git
   cd rentsmart
   ```
2. Execute o programa:
   ```bash
   python main.py
   ```
3. Responda às perguntas no terminal (nome do cliente, tipo de imóvel, quartos, garagem /
   estacionamento, crianças e número de parcelas da taxa).
4. O orçamento detalhado aparece na tela e a projeção de 12 meses é salva em
   `orcamentos/projecao_12_meses_<nome_do_cliente>.csv`.

O CSV usa `;` como separador e vírgula como casa decimal, então abre direto no Excel em português.

## Estrutura do projeto

```
rentsmart/
├── main.py         # ponto de entrada: menu, perguntas ao usuário e montagem dos objetos
├── modelos.py      # classes: Cliente, Imovel, ImovelComQuartos, Apartamento, Casa,
│                   #          Estudio, TaxaContratual e Orcamento
├── utils.py        # funções de leitura/validação de entradas e formatação de moeda
├── orcamentos/     # CSVs gerados (há um exemplo: projecao_12_meses_maria_silva.csv)
└── README.md
```

## Regras de negócio implementadas

| Imóvel      | Aluguel-base | Adicionais                                                       | Desconto                          |
|-------------|-------------:|------------------------------------------------------------------|-----------------------------------|
| Apartamento | R$ 700,00    | 2 quartos: +R$ 200,00 · Garagem: +R$ 300,00                      | 5% se o cliente não tem crianças  |
| Casa        | R$ 900,00    | 2 quartos: +R$ 250,00 · Garagem: +R$ 300,00                      | —                                 |
| Estúdio     | R$ 1.200,00  | Pacote 2 vagas: +R$ 250,00 · cada vaga adicional: +R$ 60,00      | —                                 |

- **Taxa contratual:** R$ 2.000,00, em 1 a 5 parcelas, apresentada **separada** do aluguel.
  Quando a divisão não é exata (ex.: 3x), a última parcela recebe o ajuste de centavos para
  a soma fechar em R$ 2.000,00.
- **Desconto do apartamento:** aplicado sobre o aluguel já somado aos adicionais (quarto e garagem).
- **Projeção:** as parcelas da taxa entram nos primeiros meses; do mês seguinte em diante só o aluguel.

## Exemplo de execução

```
Nome do cliente: Maria Silva
Escolha o tipo de imóvel (1-3): 1
Quantidade de quartos (1 ou 2): 2
Deseja vaga de garagem? +R$ 300,00 (S/N): S
O cliente possui crianças? (S/N): N
Em quantas parcelas deseja pagar a taxa? (1-5): 3

ALUGUEL MENSAL
  Aluguel-base (Apartamento)                   R$ 700,00
  Adicional 2º quarto                          R$ 200,00
  Vaga de garagem                              R$ 300,00
  Subtotal                                   R$ 1.200,00
  Desconto 5% (cliente sem crianças)          - R$ 60,00
  >> VALOR MENSAL DO ALUGUEL                 R$ 1.140,00
TAXA CONTRATUAL (cobrada separadamente do aluguel)
  Valor total da taxa                        R$ 2.000,00
  Condição escolhida: 3x de R$ 666,67
...
  TOTAL PREVISTO NO 1º ANO                  R$ 15.680,00
```

## Autor

Pedro Henrique Lopes de Almeida
