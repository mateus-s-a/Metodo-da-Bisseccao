import math

# =============================================================================
# [ISSUE #1] CONSTANTES E FUNÇÃO DO CIRCUITO RLC
# =============================================================================
L = 5.0      # Indutância (H)
C = 1e-4     # Capacitância (F)
T = 0.05     # Tempo de dissipação (s)
ALVO = 0.01  # q(t)/q0 = 1%

def f(R):
    """
    Calcula o valor da função f(R) baseada na equação do circuito RLC.
    Modelagem matemática designada para a Issue #1.
    """
    # f(R) = e^(-R*t/(2L)) * cos(sqrt(1/(LC) - (R/(2L))^2) * t) - 0.01
    termo_exponencial = math.exp(-(R / (2 * L)) * T)
    frequencia = math.sqrt((1 / (L * C)) - (R / (2 * L))**2)
    
    return termo_exponencial * math.cos(frequencia * T) - ALVO

def resolver_bisseccao(a, b, es, n0):
    """
    Núcleo do algoritmo do Método da Bissecção (Issue #1).
    [ISSUE #2] - Implementa cálculo de erro e formatação de tabela.
    [ISSUE #3] - Implementa validação de sinal e limite de iterações (N0).
    """
    # 1. Validação de Segurança Inicial (Issue #3)
    fa = f(a)
    fb = f(b)
    
    if fa * fb >= 0:
        print("\n" + "!"*85)
        print(f"ERRO DE ENTRADA: f({a}) * f({b}) = {fa*fb:.6f}")
        print("O Método da Bissecção requer que a função mude de sinal no intervalo [a, b].")
        print("Tente um intervalo diferente onde f(a) * f(b) < 0.")
        print("!"*85)
        return None
    
    print("\n" + "="*85)
    print(f"{'Iter':<5} | {'a':<12} | {'b':<12} | {'p':<12} | {'f(p)':<12} | {'Erro (%)':<10}")
    print("-" * 85)

    p_velho = None

    # 2. Laço de repetição com trava de segurança N0 (Issue #3)
    for iteracao in range(1, n0 + 1):
        # Cálculo do ponto médio (Issue #1)
        p = (a + b) / 2
        fp = f(p)
        
        # Cálculo do Erro Relativo (Issue #2)
        ea = 0
        erro_str = "---"
        if p_velho is not None:
            ea = abs((p - p_velho) / p) * 100
            erro_str = f"{ea:.6f}%"

        # Impressão da linha (Issue #2)
        print(f"{iteracao:<5} | {a:<12.6f} | {b:<12.6f} | {p:<12.6f} | {fp:<12.6f} | {erro_str:<10}")

        # 3. Critério de Parada por Erro (Issue #2)
        if p_velho is not None and ea < es:
            print("-" * 85)
            print(f"Critério de parada atingido: Ea ({ea:.6f}%) < Es ({es:.6f}%)")
            return p

        # Lógica de substituição (Issue #1)
        if f(a) * fp > 0:
            a = p
        else:
            b = p
        
        p_velho = p

    # Caso atinja N0 sem atingir Es (Issue #3)
    print("-" * 85)
    print(f"AVISO: O limite máximo de {n0} iterações foi atingido sem satisfazer a tolerância Es.")
    return p

if __name__ == "__main__":
    print("TRABALHO DE CÁLCULO NUMÉRICO - IFMT")
    print("MÉTODO DA BISSECÇÃO - CIRCUITO RLC (FASE 1 CONCLUÍDA)\n")
    
    try:
        # Entradas de dados (Issues #1, #2 e #3)
        limite_a = float(input("Digite o limite inferior (a): "))
        limite_b = float(input("Digite o limite superior (b): "))
        tolerancia_es = float(input("Digite a tolerância desejada (Es %): "))
        max_iter_n0 = int(input("Digite o número máximo de iterações (N0): "))
        
        resultado = resolver_bisseccao(limite_a, limite_b, tolerancia_es, max_iter_n0)
        
        if resultado is not None:
            print("=" * 85)
            print(f"Resultado final aproximado para R: {resultado:.6f} Ohms")
            print("=" * 85)
            
    except ValueError:
        print("\nErro: Por favor, insira apenas valores numéricos válidos.")
