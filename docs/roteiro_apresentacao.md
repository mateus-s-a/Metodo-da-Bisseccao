# Roteiro e Guia de Estudos para Apresentação

Este documento serve como base teórica para o nivelamento da equipe. Todos os membros devem ser capazes de explicar os pontos abaixo, conforme exigido na **Issue #5**.

---

## 1. A Matemática do Problema

### Como chegamos em $f(R) = 0$?
A equação original descreve a carga $q(t)$ no capacitor. O projeto exige que a carga seja dissipada para 1% do seu valor inicial ($q_0$).
- Matematicamente: $q(t) = 0,01 \cdot q_0$
- Substituindo na fórmula: $q_0 \cdot e^{-\frac{R}{2L}t} \cos[\dots] = 0,01 \cdot q_0$
- Simplificando $q_0$ em ambos os lados, chegamos na nossa função de busca de raízes:
  $$f(R) = e^{-\frac{R}{2L}t} \cos \left[ \left( \sqrt{\frac{1}{LC} - \left(\frac{R}{2L}\right)^2} \right) \cdot t \right] - 0,01 = 0$$

### O que significa a raiz que encontramos?
A raiz é o valor da resistência $R$ (em Ohms) que faz com que a equação acima seja zero, ou seja, o valor exato que atende à condição de dissipação de 1% no tempo $t = 0,05s$.

---

## 2. O Método da Bissecção

### Por que ele funciona? (Teorema do Valor Intermediário)
O método baseia-se no fato de que, se uma função contínua $f(x)$ assume valores de sinais opostos em um intervalo $[a, b]$ (ou seja, $f(a) \cdot f(b) < 0$), então obrigatoriamente existe pelo menos uma raiz dentro desse intervalo.

### O que é Truncamento Binário?
É a estratégia de "dividir para conquistar". A cada iteração:
1. Calculamos o ponto médio $p = (a+b)/2$.
2. Verificamos em qual metade a raiz está (onde ocorre a troca de sinal).
3. Descartamos a outra metade.
Isso garante que o erro máximo caia pela metade a cada iteração.

---

## 3. Decisões de Desenvolvimento (Justificativas)

### Por que não usamos Newton-Raphson?
Embora o método de Newton seja mais rápido, ele exige o cálculo da **derivada** $f'(R)$. No nosso caso:
- A função $f(R)$ é uma composição complexa de exponencial e cosseno com termos internos dependentes de $R$.
- Calcular essa derivada manualmente é trabalhoso e propenso a erros.
- Como o tempo de processamento não é um problema para este cálculo específico, a robustez e simplicidade da Bissecção foram priorizadas.

### Para que serve o $N_0$ e a Validação de Sinal?
- **Validação $f(a) \cdot f(b) < 0$**: Sem isso, o algoritmo poderia rodar em um intervalo sem raiz, resultando em uma resposta falsa.
- **Limite $N_0$**: É uma trava de segurança. Se o usuário pedir uma precisão maior do que a capacidade do computador (erro de arredondamento) ou se o método não convergir, o programa para e evita travamentos.
