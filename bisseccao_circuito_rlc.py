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

def resolver_bisseccao(a, b, es):
    """
    Núcleo do algoritmo do Método da Bissecção (Issue #1).
    [ISSUE #2] - Implementa cálculo de erro e formatação de tabela.
    """
    # TODO: Jeanderson (Issue #3) - Validar se f(a) * f(b) < 0 antes de iniciar.
    
    print("\n" + "="*85)
    print(f"{'Iter':<5} | {'a':<12} | {'b':<12} | {'p':<12} | {'f(p)':<12} | {'Erro (%)':<10}")
    print("-" * 85)

    p_velho = None
    iteracao = 1

    # TODO: Jeanderson (Issue #3) - Substituir por loop for i in range(N0).
    while True:
        # 1. Cálculo do ponto médio (Issue #1)
        p = (a + b) / 2
        fp = f(p)
        
        # 2. Cálculo do Erro Relativo Percentual Aproximado (Issue #2)
        ea = 0
        erro_str = "---"
        if p_velho is not None:
            ea = abs((p - p_velho) / p) * 100
            erro_str = f"{ea:.6f}%"

        # 3. Impressão da linha da tabela formatada (Issue #2)
        print(f"{iteracao:<5} | {a:<12.6f} | {b:<12.6f} | {p:<12.6f} | {fp:<12.6f} | {erro_str:<10}")

        # 4. Critério de Parada por Erro (Issue #2)
        if p_velho is not None and ea < es:
            print("-" * 85)
            print(f"Critério de parada atingido: Ea ({ea:.6f}%) < Es ({es:.6f}%)")
            break

        # 5. Lógica de substituição de extremidades (Issue #1)
        if f(a) * fp > 0:
            a = p
        else:
            b = p
        
        p_velho = p
        iteracao += 1
            
    return p

if __name__ == "__main__":
    print("TRABALHO DE CÁLCULO NUMÉRICO - IFMT")
    print("INTEGRAÇÃO: ISSUE #1 (NÚCLEO) + ISSUE #2 (ERRO E TABELA)\n")
    
    # Entradas de dados
    # TODO: Jeanderson (Issue #3) - Solicitar N0 (Máximo de iterações).
    limite_a = float(input("Digite o limite inferior (a): "))
    limite_b = float(input("Digite o limite superior (b): "))
    tolerancia_es = float(input("Digite a tolerância desejada (Es %): "))
    
    resultado = resolver_bisseccao(limite_a, limite_b, tolerancia_es)
    
    print("=" * 85)
    print(f"Resultado final aproximado para R: {resultado:.6f} Ohms")
    print("=" * 85)
