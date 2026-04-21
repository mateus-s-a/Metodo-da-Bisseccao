# Trabalho de Cálculo Numérico: Dimensionamento de Resistor em Circuito RLC

**Data da Apresentação:** 14/05/2026
**Equipe de Desenvolvimento:**
* Mateus de Souza Arruda
* Rayssa Conceição Santiago
* Jeanderson Athamay Araújo dos Anjos

## Descrição do Projeto
Este repositório contém a implementação computacional do **Método da Bissecção**, desenvolvida como requisito para o trabalho prático da disciplina de Cálculo Numérico. O objetivo prático é resolver um problema de engenharia envolvendo o comportamento transiente de um circuito RLC. Especificamente, o algoritmo determina o valor apropriado da resistência elétrica capaz de dissipar a carga de um capacitor para 1% de seu valor original em um tempo estipulado, utilizando componentes fixos dados.

A escolha pelo Método da Bissecção justifica-se, conforme as orientações do trabalho, devido à complexidade matemática para o cálculo da derivada da equação de carga, o que tornaria a aplicação do método de Newton-Raphson trabalhosa e inconveniente.

## Modelo Matemático
O comportamento transiente da carga no capacitor do circuito após o fechamento da chave é regido por uma equação diferencial ordinária linear de segunda ordem, cuja solução é fornecida por:

$q(t) = q_0 e^{-\frac{R}{2L}t} \cos \left[ \left( \sqrt{\frac{1}{LC} - \left(\frac{R}{2L}\right)^2} \right) \cdot t \right]$

*Onde:*
*   $q(t)$: carga do capacitor no instante de tempo $t$.
*   $q_0$: carga original (ou inicial) do capacitor.
*   $R$: resistência do resistor (a incógnita a ser descoberta).
*   $L$: indutância do indutor.
*   $C$: capacitância do capacitor.
*   $t$: tempo decorrido após o fechamento da chave.
*   $e$: base do logaritmo natural (constante de Euler).

Para aplicar o Método numérico, a equação foi adaptada considerando as exigências do projeto: a carga deve ser dissipada a 1% de seu valor original ($q(t)/q_0 = 0,01$) no instante $t = 0,05$ s, com constantes indutivas e capacitivas fixadas em $L = 5$ H e $C = 10^{-4}$ F. Isolando os termos para criar uma função de busca de raízes, temos a equação igualada a zero:

$f(R) = e^{-\frac{R}{2L}t} \cos \left[ \left( \sqrt{\frac{1}{LC} - \left(\frac{R}{2L}\right)^2} \right) \cdot t \right] - 0,01 = 0$

*Onde:*
*   $f(R)$: função a ser avaliada iterativamente da qual procuramos a raiz (o ponto de cruzamento onde $f(R) = 0$).
*   $R$: resistência do resistor.
*   $L$: indutância do indutor ($5$ H).
*   $C$: capacitância do capacitor ($10^{-4}$ F).
*   $t$: tempo de dissipação estipulado ($0,05$ s).
*   $0,01$: relação $q/q_0$ exigida pelo projeto (1%).
*   $e$: base do logaritmo natural.

Como raramente a raiz exata é conhecida de antemão, o critério de parada adotado pelo nosso algoritmo é o do **Erro Relativo Percentual Aproximado ($\mathcal{E}_a$)**, calculado interativamente a cada novo refinamento da raiz:

$\mathcal{E}_a = \left| \frac{x_r^{novo} - x_r^{velho}}{x_r^{novo}} \right| \times 100\%$

*Onde:*
*   $\mathcal{E}_a$: erro relativo percentual aproximado.
*   $x_r^{novo}$: estimativa da raiz na iteração atual (ponto médio do subintervalo atual).
*   $x_r^{velho}$: estimativa da raiz na iteração anterior (ponto médio do subintervalo prévio).

## Estrutura do Repositório
*   [`bisseccao_circuito_rlc.py`](bisseccao_circuito_rlc.py): Código-fonte principal em Python. Engloba a modelagem da equação (Mateus), a formatação e análise iterativa do erro (Rayssa) e as rotinas rigorosas de segurança, prevenção de loop infinito e validação inicial de truncamento (Jeanderson).
*   [`resultados_tabela.txt`](resultados_tabela.txt): Arquivo de log gravando a saída final do terminal, exibindo ao orientador as métricas e o histórico da Bissecção iteração por iteração.
*   [`docs/Av2_1_EXERCICIO_TRABALHO.pdf`](docs/Av2_1_EXERCICIO_TRABALHO.pdf): Documento com o enunciado original base para resolução.
*   [`docs/roteiro_apresentacao.md`](docs/roteiro_apresentacao.md): Material unificado de apoio teórico com as definições para o sorteio da apresentação.

## Como Executar

### Localmente

1. Certifique-se de que o interpretador Python (versão 3.x) esteja devidamente instalado no sistema.
2. Clone este repositório para a sua máquina ou realize o download como `.zip`.
3. Abra o seu terminal de preferência (Prompt de Comando, PowerShell, bash) e navegue até a pasta raiz onde o arquivo está alocado.
4. Execute o programa usando o comando:
   ```bash
   python bisseccao_circuito_rlc.py
   ```
5. Durante a execução, as validações de segurança solicitarão a entrada dos limites de intervalo `[a, b]` previamente descobertos pelo grupo (que satisfazem a restrição $f(a) \times f(b) < 0$), o limite máximo de iterações $N_0$ e a tolerância do erro relativo $\mathcal{E}_s$.
6. O console irá gerar visualmente a tabela da solução e os dados processados serão armazenados para conferência.

### Google Colab (ainda não realizado)

1. Acesse o [Google Colab](https://colab.research.google.com/).
2. Clique em "Arquivo" > "Upload de notebook".
3. Selecione o arquivo `bisseccao_circuito_rlc.py`.
4. Siga os mesmos passos de execução do terminal.

## Resultados e Conclusão
Após a execução e a integração dos módulos desenvolvidos pelo grupo, utilizamos o intervalo validado manualmente de `[a, b] = [INSERIR_EXTREMO_A, INSERIR_EXTREMO_B]` juntamente com uma tolerância programada estrita. O critério de Erro Relativo foi alcançado com sucesso na iteração número `[INSERIR_NUMERO_DA_ITERACAO_FINAL]`.

O valor final determinado para o resistor do circuito, para que a carga de dissipação do capacitor cumpra a exigência de ser $1\%$ do seu original após $0,05$ segundos, convergiu com segurança para:
**$R \approx$ `[INSERIR_VALOR_FINAL_DE_R]` Ohms**.
