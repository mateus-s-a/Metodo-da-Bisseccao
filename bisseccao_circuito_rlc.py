import math
import os

# Tentar importar bibliotecas de visualização
try:
    # pyrefly: ignore [missing-import]
    import matplotlib.pyplot as plt
    # pyrefly: ignore [missing-import]
    import numpy as np
    VISUALIZACAO_DISPONIVEL = True
except ImportError:
    VISUALIZACAO_DISPONIVEL = False

# =============================================================================
# CONSTANTES E FUNÇÃO DO CIRCUITO RLC
# =============================================================================
L = 5.0      # Indutância (H)
C = 1e-4     # Capacitância (F)
T = 0.05     # Tempo de dissipação (s)
ALVO = 0.01  # q(t)/q0 = 1%

def f(R):
    """
    Calcula o valor da função f(R) baseada na equação do circuito RLC.
    """
    termo_exponencial = math.exp(-(R / (2 * L)) * T)
    
    # Proteção contra valores de R que tornariam a frequência imaginária
    frequencia_interna = (1 / (L * C)) - (R / (2 * L))**2
    if frequencia_interna < 0:
        return float('inf')
        
    frequencia = math.sqrt(frequencia_interna)
    return termo_exponencial * math.cos(frequencia * T) - ALVO

def resolver_bisseccao(a, b, es, n0):
    """
    Núcleo do algoritmo do Método da Bissecção.
    [ISSUE #4] - Agora grava os resultados automaticamente em resultados_tabela.txt.
    """
    # 1. Validação de Segurança Inicial
    fa = f(a)
    fb = f(b)
    
    if fa * fb >= 0:
        msg_erro = (
            "\n" + "!"*120 + "\n" +
            f"ERRO DE ENTRADA: f({a}) * f({b}) = {fa*fb:.9f}\n" +
            "O Método da Bissecção requer que a função mude de sinal no intervalo [a, b].\n" +
            "Tente um intervalo diferente onde f(a) * f(b) < 0.\n" +
            "!"*120 + "\n"
        )
        print(msg_erro)
        return None
    
    # Preparação para gravação em arquivo e gráfico
    linhas_log = []
    historico_p = []
    historico_fp = []
    
    cabecalho_tab = "\n" + "="*120 + "\n"
    cabecalho_tab += f"{'Iter':<5} | {'a':<13} | {'b':<13} | {'p':<13} | {'f(a)':<13} | {'f(b)':<11} | {'f(p)':<12} | {'Erro (%)':<11}\n"
    cabecalho_tab += "-" * 120
    
    print(cabecalho_tab)
    linhas_log.append(cabecalho_tab)

    p_velho = None

    # 2. Laço de repetição com trava de segurança N0
    for iteracao in range(1, n0 + 1):
        p = (a + b) / 2
        fa = f(a)
        fb = f(b)
        fp = f(p)
        
        # Coleta de dados para o gráfico
        historico_p.append(p)
        historico_fp.append(fp)
        
        # 3. Cálculo do erro percentual aproximado (ea)
        ea = 0
        erro_str = "---"
        if p_velho is not None:
            # |(p - p_velho) / p| × 100
            ea = abs((p - p_velho) / p) * 100
            erro_str = f"{ea:.9f}%"

        # 4. Formatação da Linha da Tabela
        linha = f"{iteracao:<5} | {a:<12.9f} | {b:<12.9f} | {p:<12.9f} | {fa:<12.9f} | {fb:<12.9f} | {fp:<12.9f} | {erro_str:<10}"
        print(linha)
        linhas_log.append(linha)

        # 5. Critério de Parada por Erro
        if p_velho is not None and ea < es:
            msg_parada = "-" * 120 + "\n"
            msg_parada += f"Critério de parada atingido: Ea ({ea:.9f}%) < Es ({es:.9f}%)"
            print(msg_parada)
            linhas_log.append(msg_parada)
            
            # Salvar no arquivo (Issue #4)
            salvar_resultados(linhas_log, p)
            if VISUALIZACAO_DISPONIVEL:
                gerar_grafico(historico_p, historico_fp, p)
            return p

        # Lógica de substituição
        if f(a) * fp > 0:
            a = p
        else:
            b = p
        
        p_velho = p

    # Caso atinja N0 sem atingir Es
    msg_aviso = "-" * 85 + "\n"
    msg_aviso += f"AVISO: O limite máximo de {n0} iterações foi atingido sem satisfazer a tolerância Es."
    print(msg_aviso)
    linhas_log.append(msg_aviso)
    
    # Salvar no arquivo mesmo se não atingir Es (Issue #4)
    salvar_resultados(linhas_log, p)
    if VISUALIZACAO_DISPONIVEL:
        gerar_grafico(historico_p, historico_fp, p)
    return p

def gerar_grafico(historico_p, historico_fp, raiz_final):
    """
    Gera o gráfico de convergência (PNG).
    """
    print("\n[INFO] Gerando gráfico de convergência...")
    
    p_min, p_max = min(historico_p), max(historico_p)
    margem = (p_max - p_min) * 0.5 if p_max != p_min else 10
    r_range = np.linspace(p_min - margem, p_max + margem, 500)
    
    f_vec = np.vectorize(f)
    y_range = f_vec(r_range)
    
    plt.figure(figsize=(10, 6))
    plt.plot(r_range, y_range, label='f(R)', color='#2c3e50', linewidth=2)
    plt.axhline(0, color='red', linestyle='--', alpha=0.5)
    
    # Plotar os pontos de cada iteração
    plt.scatter(historico_p, historico_fp, color='#3498db', alpha=0.6, label='Pontos Médios (p)')
    
    # Destacar a raiz final
    plt.scatter([raiz_final], [f(raiz_final)], color='#e74c3c', s=120, marker='*', label=f'Raiz Final: {raiz_final:.4f} Ohms', zorder=5)
    
    plt.title('Visualização Técnica: Método da Bissecção (Circuito RLC)')
    plt.xlabel('Resistência R (Ohms)')
    plt.ylabel('Valor de f(R)')
    plt.grid(True, linestyle=':', alpha=0.6)
    plt.legend()
    
    plt.savefig("grafico_convergencia.png")
    plt.close()
    print("[INFO] Arquivo 'grafico_convergencia.png' gerado com sucesso.")

def salvar_resultados(linhas, resultado_final):
    """
    Função auxiliar para gravar os resultados em arquivo (Issue #4).
    """
    try:
        with open("resultados_tabela.txt", "w", encoding="utf-8") as f_out:
            f_out.write("RELATÓRIO DE EXECUÇÃO - MÉTODO DA BISSECÇÃO\n")
            f_out.write("PROJETO CIRCUITO RLC - CÁLCULO NUMÉRICO\n")
            f_out.write("\n".join(linhas))
            f_out.write("\n" + "=" * 85 + "\n")
            f_out.write(f"Resultado final aproximado para R: {resultado_final:.6f} Ohms\n")
            f_out.write("=" * 85 + "\n")
        print(f"\n[INFO] Resultados salvos com sucesso em 'resultados_tabela.txt'")
    except Exception as e:
        print(f"\n[ERRO] Falha ao salvar o arquivo de resultados: {e}")

if __name__ == "__main__":
    print("TRABALHO DE CÁLCULO NUMÉRICO - IFMT")
    print("MÉTODO DA BISSECÇÃO - CIRCUITO RLC\n")
    
    if not VISUALIZACAO_DISPONIVEL:
        print("[AVISO] Bibliotecas de visualização não encontradas. O gráfico não será gerado.\n")
    
    try:
        limite_a = float(input("Digite o limite inferior (a): "))
        limite_b = float(input("Digite o limite superior (b): "))
        tolerancia_es = float(input("Digite a tolerância desejada (Es %): "))
        max_iter_n0 = int(input("Digite o número máximo de iterações (N0): "))
        
        resultado = resolver_bisseccao(limite_a, limite_b, tolerancia_es, max_iter_n0)
        
        if resultado is not None:
            print("=" * 85)
            print(f"Resultado final aproximado para R: {resultado:.9f} Ohms")
            print("=" * 85)
            
    except ValueError:
        print("\nErro: Por favor, insira apenas valores numéricos válidos.")
