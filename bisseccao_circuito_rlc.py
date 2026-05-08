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
    Núcleo do algoritmo do Método da Bissecção.
    [ISSUE #4] - Agora grava os resultados automaticamente em resultados_tabela.txt.
    """
    # 1. Validação de Segurança Inicial
    fa = f(a)
    fb = f(b)
    
    if fa * fb >= 0:
        msg_erro = (
            "\n" + "!"*85 + "\n" +
            f"ERRO DE ENTRADA: f({a}) * f({b}) = {fa*fb:.6f}\n" +
            "O Método da Bissecção requer que a função mude de sinal no intervalo [a, b].\n" +
            "Tente um intervalo diferente onde f(a) * f(b) < 0.\n" +
            "!"*85 + "\n"
        )
        print(msg_erro)
        return None
    
    # Preparação para gravação em arquivo (Issue #4)
    linhas_log = []
    
    cabecalho_tab = "\n" + "="*85 + "\n"
    cabecalho_tab += f"{'Iter':<5} | {'a':<12} | {'b':<12} | {'p':<12} | {'f(p)':<12} | {'Erro (%)':<10}\n"
    cabecalho_tab += "-" * 85
    
    print(cabecalho_tab)
    linhas_log.append(cabecalho_tab)

    p_velho = None

    # 2. Laço de repetição com trava de segurança N0
    for iteracao in range(1, n0 + 1):
        p = (a + b) / 2
        fp = f(p)
        
        ea = 0
        erro_str = "---"
        if p_velho is not None:
            ea = abs((p - p_velho) / p) * 100
            erro_str = f"{ea:.6f}%"

        linha = f"{iteracao:<5} | {a:<12.6f} | {b:<12.6f} | {p:<12.6f} | {fp:<12.6f} | {erro_str:<10}"
        print(linha)
        linhas_log.append(linha)

        # 3. Critério de Parada por Erro
        if p_velho is not None and ea < es:
            msg_parada = "-" * 85 + "\n"
            msg_parada += f"Critério de parada atingido: Ea ({ea:.6f}%) < Es ({es:.6f}%)"
            print(msg_parada)
            linhas_log.append(msg_parada)
            
            # Salvar no arquivo (Issue #4)
            salvar_resultados(linhas_log, p)
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
    return p

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
    
    try:
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
