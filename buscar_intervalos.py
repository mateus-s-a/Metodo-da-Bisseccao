"""
buscar_intervalos.py
--------------------
Script auxiliar que encontra aleatoriamente 5 intervalos [a, b] válidos
para o Método da Bissecção, onde:
  - Ambos os valores são menores que a raíz positiva (~328 Ohms)
  - A condição f(a) * f(b) < 0 é satisfeita

Importa diretamente a função f(R) do script principal, evitando
duplicação de lógica.
"""

import random
import sys
import os

# Importa a função f(R) do script principal
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from bisseccao_circuito_rlc import f

# =============================================================================
# LIMITES DO DOMÍNIO (com base na análise do sinal de f(R))
# =============================================================================
RAIZ_POSITIVA  = 328.0    # Limite superior: ambos a e b devem ser menores que isso
RAIZ_NEGATIVA  = -318.677 # Raiz negativa real (fronteira de troca de sinal)
LIMITE_FISICO  = 446.0    # Limite supercrítico: |R| > sqrt(200000) ≈ 447 → f = inf

# Regiões de sinal de f(R):
#  Região A [f > 0]: -LIMITE_FISICO < R < RAIZ_NEGATIVA  (ex: -445 a -319)
#  Região B [f < 0]: RAIZ_NEGATIVA < R < RAIZ_POSITIVA  (ex: 0 a +327)
#
# Para garantir a > 0: 'a' vem sempre da Região B (positivo, f < 0)
#                       'b' vem sempre da Região A (negativo, f > 0)

def buscar_intervalos(quantidade: int = 5) -> list:
    """
    Busca aleatoriamente intervalos válidos [a, b] onde f(a) * f(b) < 0
    e ambos os valores são menores que a raíz positiva real (~328 Ohms).

    Estratégia:
        Para garantir troca de sinal, um valor é sorteado da Região A (f > 0)
        e outro da Região B (f < 0). Ambas as regiões têm R < 328.
    """
    encontrados = []

    while len(encontrados) < quantidade:
        # 'a' sempre positivo: sorteado da Região B (0 a +327.5), onde f(R) < 0
        a = random.uniform(0.5, RAIZ_POSITIVA - 0.5)

        # 'b' sempre negativo: sorteado da Região A (-445 a -319.2), onde f(R) > 0
        b = random.uniform(-LIMITE_FISICO + 1, RAIZ_NEGATIVA - 0.5)

        fa = f(a)
        fb = f(b)

        # Verificação explícita da condição (segurança extra)
        if fa == float('inf') or fb == float('inf'):
            continue

        if fa * fb < 0:
            # Mantém a ordem: a (positivo) e b (negativo), sem reordenar por tamanho
            encontrados.append((a, b, fa, fb))

    return encontrados


def main():
    print("\n" + "=" * 72)
    print("  BUSCADOR ALEATÓRIO DE INTERVALOS VÁLIDOS — MÉTODO DA BISSECÇÃO")
    print(f"  Restrição: a < {RAIZ_POSITIVA} e b < {RAIZ_POSITIVA} | f(a)×f(b) < 0")
    print("=" * 72)

    intervalos = buscar_intervalos(5)

    print(f"\n  {'#':<4} {'a':>14} {'b':>14} {'f(a)':>14} {'f(b)':>12}")
    print("  " + "-" * 62)

    for i, (a, b, fa, fb) in enumerate(intervalos, 1):
        print(f"  {i:<4} {a:>14.4f} {b:>14.4f} {fa:>14.6f} {fb:>12.6f}")

    print("  " + "-" * 62)
    print(f"  Todos os intervalos satisfazem: f(a) × f(b) < 0 ✓")
    print(f"  'a' é sempre positivo (a > 0) ✓")
    print(f"  Todos os valores são menores que a raíz positiva (~328 Ohms) ✓\n")


if __name__ == "__main__":
    main()
