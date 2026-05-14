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

A seguir, apresentamos passo a passo o percurso de reformulação da equação original do circuito RLC até chegarmos à função de uma única variável $f(R)$, cuja raiz é determinada numericamente pelo Método da Bissecção.

### Passo 1 — Equação Original do Circuito RLC

O comportamento transiente da carga no capacitor do circuito após o fechamento da chave é regido por uma equação diferencial ordinária linear de segunda ordem, cuja solução analítica é:

$$q(t) = q_0 \cdot e^{-\frac{R}{2L} \cdot t} \cdot \cos \left( \sqrt{\frac{1}{LC} - \left(\frac{R}{2L}\right)^2} \cdot t \right)$$

*Onde:*
*   $q(t)$: carga do capacitor no instante de tempo $t$.
*   $q_0$: carga original (ou inicial) do capacitor.
*   $R$: resistência do resistor (a **incógnita** a ser descoberta).
*   $L$: indutância do indutor.
*   $C$: capacitância do capacitor.
*   $t$: tempo decorrido após o fechamento da chave.
*   $e$: base do logaritmo natural (constante de Euler).

### Passo 2 — Normalização da Equação

Para eliminar a dependência da carga inicial $q_0$ (que não é fornecida no problema), dividimos ambos os lados da equação por $q_0$:

$$\frac{q(t)}{q_0} = e^{-\frac{R}{2L} \cdot t} \cdot \cos \left( \sqrt{\frac{1}{LC} - \left(\frac{R}{2L}\right)^2} \cdot t \right)$$

O lado esquerdo agora representa a **fração da carga remanescente** no capacitor, um valor adimensional entre 0 e 1.

### Passo 3 — Imposição da Condição do Projeto

O enunciado exige que a carga seja dissipada a **1% de seu valor original** no instante $t = 0{,}05$ s. Isso significa:

$$\frac{q(t)}{q_0} = 0{,}01$$

Substituindo essa condição na equação normalizada:

$$0{,}01 = e^{-\frac{R}{2L} \cdot t} \cdot \cos \left( \sqrt{\frac{1}{LC} - \left(\frac{R}{2L}\right)^2} \cdot t \right)$$

### Passo 4 — Reformulação como Problema de Busca de Raízes

Para aplicar o Método da Bissecção, precisamos de uma função igualada a zero — isto é, $f(R) = 0$. Passamos o $0{,}01$ para o outro lado da igualdade:

$$f(R) = e^{-\frac{R}{2L} \cdot t} \cdot \cos \left( \sqrt{\frac{1}{LC} - \left(\frac{R}{2L}\right)^2} \cdot t \right) - 0{,}01 = 0$$

Agora temos uma **função de uma única variável** $R$. O valor de $R$ que faz $f(R) = 0$ é a raiz que procuramos — a resistência ideal para o circuito.

### Passo 5 — Substituição das Constantes Conhecidas

Os valores fornecidos pelo problema são:
| Constante | Símbolo | Valor |
|---|---|---|
| Indutância | $L$ | $5$ H |
| Capacitância | $C$ | $10^{-4}$ F |
| Tempo de dissipação | $t$ | $0{,}05$ s |

Substituindo cada termo:

**Termo do amortecimento exponencial:**

$$\frac{R}{2L} \cdot t = \frac{R}{2 \cdot 5} \cdot 0{,}05 = \frac{R}{10} \cdot 0{,}05 = \frac{R}{200} = 0{,}005R$$

**Termo da frequência angular (dentro da raiz quadrada):**

$$\frac{1}{LC} = \frac{1}{5 \cdot 10^{-4}} = \frac{1}{0{,}0005} = 2000$$

$$\left(\frac{R}{2L}\right)^2 = \left(\frac{R}{10}\right)^2 = \frac{R^2}{100}$$

$$\therefore \quad \frac{1}{LC} - \left(\frac{R}{2L}\right)^2 = 2000 - \frac{R^2}{100}$$

**Argumento do cosseno:**

$$\sqrt{2000 - \frac{R^2}{100}} \cdot t = 0{,}05 \cdot \sqrt{2000 - \frac{R^2}{100}}$$

### Passo 6 — Forma Final Simplificada

Reunindo todos os termos substituídos, a função implementada no código é:

$$\boxed{f(R) = e^{-0{,}005R} \cdot \cos \left( 0{,}05 \cdot \sqrt{2000 - \frac{R^2}{100}} \right) - 0{,}01}$$

Esta é uma **função transcendental** (envolve exponencial e cosseno simultaneamente) de uma **única variável** $R$. Apesar de não ser uma função linear nem polinomial, ela pode ser representada perfeitamente em um gráfico no **plano cartesiano** com:
*   **Eixo horizontal ($x$):** valores de $R$ (resistência em Ohms).
*   **Eixo vertical ($y$):** valores de $f(R)$.

### Interpretação Gráfica

A curva $y = f(R)$ plotada no plano cartesiano permite visualizar diretamente o comportamento da função:

*   Onde a curva **cruza o eixo horizontal** ($y = 0$), temos $f(R) = 0$ — ou seja, a **raiz** que satisfaz a condição do problema.
*   O Método da Bissecção opera justamente nessa lógica: dado um intervalo $[a, b]$ onde $f(a)$ e $f(b)$ possuem **sinais opostos** (um acima e outro abaixo do eixo $x$), o algoritmo vai estreitando o intervalo até localizar com precisão o ponto de cruzamento.

O gráfico gerado pelo programa ([`grafico_convergencia.png`](grafico_convergencia.png)) ilustra essa curva e destaca os pontos médios calculados a cada iteração, mostrando como as aproximações convergem visualmente em direção à raiz.

---

### Critério de Parada: Erro Relativo Percentual Aproximado

Como raramente a raiz exata é conhecida de antemão, o critério de parada adotado pelo nosso algoritmo é o do **Erro Relativo Percentual Aproximado ($\mathcal{E}_a$)**, calculado a cada novo refinamento da raiz:

$$\mathcal{E}_a = \left| \frac{x_r^{novo} - x_r^{velho}}{x_r^{novo}} \right| \times 100\%$$

*Onde:*
*   $\mathcal{E}_a$: erro relativo percentual aproximado.
*   $x_r^{novo}$: estimativa da raiz na iteração atual (ponto médio do subintervalo atual).
*   $x_r^{velho}$: estimativa da raiz na iteração anterior (ponto médio do subintervalo prévio).

O algoritmo compara o valor de $\mathcal{E}_a$ com a tolerância $\mathcal{E}_s$ definida pelo usuário. Quando $\mathcal{E}_a < \mathcal{E}_s$, a diferença entre as aproximações sucessivas é suficientemente pequena, indicando que a raiz foi localizada com a precisão desejada, e a execução é encerrada.

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
5. Durante a execução, o programa solicitará os seguintes parâmetros:
   - **Limite inferior (a)**: Extremidade esquerda do intervalo.
   - **Limite superior (b)**: Extremidade direita do intervalo.
   - **Tolerância (Es %)**: O erro relativo percentual aceitável para parada.
   - **Máximo de iterações (N0)**: Trava de segurança para evitar loops infinitos.

### Exemplo Prático de Execução
Para testar o algoritmo com valores validados pelo grupo, utilize as seguintes entradas:
- **a**: `320`
- **b**: `330`
- **Es**: `0.01`
- **N0**: `100`

6. O console irá gerar visualmente a tabela da solução e os dados processados serão armazenados automaticamente no arquivo [`resultados_tabela.txt`](resultados_tabela.txt) para conferência posterior.

### Google Colab (ainda não realizado)

1. Acesse o [Google Colab](https://colab.research.google.com/).
2. Clique em "Arquivo" > "Upload de notebook".
3. Selecione o arquivo `bisseccao_circuito_rlc.py`.
4. Siga os mesmos passos de execução do terminal.

## Resultados e Conclusão
Após a execução e a integração dos módulos desenvolvidos pelo grupo, utilizamos o intervalo validado manualmente de `[a, b] = [INSERIR_EXTREMO_A, INSERIR_EXTREMO_B]` juntamente com uma tolerância programada estrita. O critério de Erro Relativo foi alcançado com sucesso na iteração número `[INSERIR_NUMERO_DA_ITERACAO_FINAL]`.

O valor final determinado para o resistor do circuito, para que a carga de dissipação do capacitor cumpra a exigência de ser $1\%$ do seu original após $0,05$ segundos, convergiu com segurança para:
**$R \approx$ `[INSERIR_VALOR_FINAL_DE_R]` Ohms**.
