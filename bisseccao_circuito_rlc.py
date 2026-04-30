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

def resolver_bisseccao(a, b):
    """
    Núcleo do algoritmo do Método da Bissecção (Issue #1).
    Implementa a divisão do intervalo e a lógica de substituição.
    """
    # TODO: Jeanderson (Issue #3) - Validar se f(a) * f(b) < 0 antes de iniciar.
    
    print("-" * 40)
    print("Iniciando iterações da Issue #1...")
    # TODO: Rayssa (Issue #2) - Adicionar cabeçalho da tabela formatada.
    print("-" * 40)

    # Laço de repetição principal para refinamento da raiz
    # TODO: Jeanderson (Issue #3) - Substituir por loop for i in range(N0).
    while True:
        # 1. Cálculo do ponto médio (Issue #1)
        p = (a + b) / 2
        fp = f(p)
        
        # TODO: Rayssa (Issue #2) - Calcular Erro Relativo Percentual Aproximado.
        # TODO: Rayssa (Issue #2) - Imprimir linha da tabela formatada.

        print(f"Ponto médio (p): {p:.4f} | f(p): {fp:.6f}")

        # 2. Lógica de substituição de extremidades (Issue #1)
        # Se f(a) e f(p) têm o mesmo sinal, a raiz está no subintervalo [p, b]
        if f(a) * fp > 0:
            a = p
        else:
            b = p
        
        # TODO: Rayssa (Issue #2) - Verificar se Erro < Es para interromper.
        
        # Controle manual temporário enquanto a Issue #2 (Critérios de Parada)
        # e a Issue #3 (Segurança/N0) não são integradas ao núcleo.
        continuar = input("\nRealizar próxima iteração? (s/n): ")
        if continuar.lower() != 's':
            break
            
    return p

if __name__ == "__main__":
    print("TRABALHO DE CÁLCULO NUMÉRICO - IFMT")
    print("DESENVOLVIMENTO: ISSUE #1 (NÚCLEO DO ALGORITMO)\n")
    
    # Entradas básicas para teste da lógica
    # TODO: Jeanderson (Issue #3) - Solicitar N0 (Máximo de iterações).
    # TODO: Rayssa (Issue #2) - Solicitar Es (Tolerância do Erro).
    
    limite_a = float(input("Digite o limite inferior (a): "))
    limite_b = float(input("Digite o limite superior (b): "))
    
    resultado = resolver_bisseccao(limite_a, limite_b)
    
    print(f"\nÚltima estimativa calculada para R: {resultado:.4f} Ohms")
