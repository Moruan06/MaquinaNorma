import os
from typing import NamedTuple

# 1. Definição da Estrutura da Instrução (Como uma Struct)
class Instrucao(NamedTuple):
    rotulo: str
    operacao: str
    registrador: str
    desvios: list

# Inicialização dos 8 registradores padrão solicitados pelo PDF
registradores = {"A": 0, "B": 0, "C": 0, "D": 0, "E": 0, "F": 0, "G": 0, "H": 0}

def inicializar_registradores():
    """Permite ao usuário definir os valores iniciais dos registradores limpando resíduos anteriores"""
    print("\n--- INICIALIZAÇÃO DOS REGISTRADORES ---")
    
    # Reseta o lixo da macro anterior antes de pedir os novos inputs
    for reg in registradores.keys():
        registradores[reg] = 0
        
    for reg in registradores.keys():
        while True:
            try:
                val = input(f"Defina o valor inicial para {reg} (padrão 0): ").strip()
                if val == "":
                    break  # Mantém o zero definido no reset acima
                val_int = int(val)
                if val_int >= 0:
                    registradores[reg] = val_int
                    break
                else:
                    print("A Máquina Norma só aceita números inteiros não-negativos (naturais).")
            except ValueError:
                print("Por favor, digite um número inteiro válido.")
    print("\nRegistradores inicializados com sucesso!")

def carregar_programa(caminho_arquivo):
    """Faz o parse das instruções do arquivo texto informado"""
    if not caminho_arquivo or not os.path.exists(caminho_arquivo):
        print(f"\n[ERRO] O arquivo '{caminho_arquivo}' não foi encontrado.")
        print("Certifique-se de que a pasta 'Códigos' existe e contém o arquivo com o nome correto.")
        return None, None

    programa = {}
    primeiro_rotulo = None

    try:
        with open(caminho_arquivo, "r", encoding="utf-8") as arquivo:
            for linha in arquivo:
                linha_limpa = linha.strip()
                if not linha_limpa or linha_limpa.startswith("#"):
                    continue
                
                partes = linha_limpa.split()
                if len(partes) < 4:
                    continue
                
                rotulo = partes[0]
                operacao = partes[1].upper()
                registrador = partes[2].upper()
                desvios = partes[3:]
                
                if primeiro_rotulo is None:
                    primeiro_rotulo = rotulo
                
                programa[rotulo] = Instrucao(rotulo, operacao, registrador, desvios)
                
        return programa, primeiro_rotulo
    except Exception as e:
        print(f"Erro ao ler o arquivo: {e}")
        return None, None

def exibir_menu():
    print("\n=========================================")
    print("        MENU DE SELEÇÃO DE MACROS        ")
    print("=========================================")
    print("1) Soma (A := A + B)")
    print("2) Multiplicação (A := A * B)")
    print("3) Fatorial (A!)")
    print("4) Teste Menor que (A < B)")
    print("5) Teste Mod (A % B == 0)")
    print("6) Teste Primo")
    print("7) Potência (C := A ^ B)")
    print("8) Fibonacci Iterativo")
    print("9) Divisão Inteira com Resto")
    print("10) MDC (Algoritmo de Euclides)")
    print("11) Coeficiente Binomial C(n, k)")
    print("0) Sair do Simulador")
    print("=========================================")
    return input("Escolha qual macro deseja rodar: ").strip()

# Funções das Operações Básicas da Máquina Norma
def op_add(registrador, desvios):
    registradores[registrador] += 1
    return desvios[0]

def op_sub(registrador, desvios):
    if registradores[registrador] > 0:
        registradores[registrador] -= 1
    return desvios[0]

def op_zer(registrador, desvios):
    if registradores[registrador] == 0:
        return desvios[0]
    else:
        return desvios[1]

# Interpretador / Motor de Execução
def executar_simulador(programa, rotulo_inicial):
    if not programa or not rotulo_inicial:
        return

    rotulo_atual = rotulo_inicial
    valores_iniciais = tuple(registradores.values())
    print(f"\n{valores_iniciais}, M) Entrada de Dados")
    
    while rotulo_atual in programa:
        cmd = programa[rotulo_atual]
        valores_regs = tuple(registradores.values())
        
        if cmd.operacao == "ZER":
            texto_instrucao = f"SE ZER ({cmd.registrador}) ENTAO VA_PARA {cmd.desvios[0]} SENAO VA_PARA {cmd.desvios[1]}"
        elif cmd.operacao == "ADD":
            texto_instrucao = f"FACA ADD ({cmd.registrador}) VA_PARA {cmd.desvios[0]}"
        elif cmd.operacao == "SUB":
            texto_instrucao = f"FACA SUB ({cmd.registrador}) VA_PARA {cmd.desvios[0]}"
        else:
            texto_instrucao = f"{cmd.operacao} {cmd.registrador} {' '.join(cmd.desvios)}"

        print(f"{valores_regs}, {cmd.rotulo}) {texto_instrucao}")
        
        if cmd.operacao == "ADD":
            proximo_rotulo = op_add(cmd.registrador, cmd.desvios)
        elif cmd.operacao == "SUB":
            proximo_rotulo = op_sub(cmd.registrador, cmd.desvios)
        elif cmd.operacao == "ZER":
            proximo_rotulo = op_zer(cmd.registrador, cmd.desvios)
        else:
            print(f"Erro: Operação desconhecida '{cmd.operacao}' na linha {cmd.rotulo}.")
            break
            
        rotulo_atual = proximo_rotulo

    valores_finais = tuple(registradores.values())
    print(f"\n[FIM DA EXECUÇÃO] Linha de parada atingida. Linha tentada: {rotulo_atual}")
    print(f"Estado Final dos Registradores: {valores_finais}")

if __name__ == "__main__":
    mapeamento_arquivos = {
        "1": "soma.txt",
        "2": "multiplicacao.txt",
        "3": "fatorial.txt",
        "4": "AmenorqueB.txt",
        "5": "Divisao.txt",
        "6": "primo.txt",
        "7": "potencia.txt",
        "8": "fibonacci.txt",
        "9": "resto.txt",
        "10": "mdc.txt",
        "11": "coeficiente_binomial.txt"
    }
    
    while True:
        opcao = exibir_menu()
        
        if opcao == "0":
            print("\nEncerrando o simulador.")
            break
            
        if opcao in mapeamento_arquivos:
            caminho_escolhido = os.path.join("Códigos", mapeamento_arquivos[opcao])
            programa_carregado, rotulo_inicial = carregar_programa(caminho_escolhido)
            
            if programa_carregado:
                inicializar_registradores()
                executar_simulador(programa_carregado, rotulo_inicial)
                input("\nPressione ENTER para voltar ao menu...")
        else:
            print("\nOpção inválida! Selecione um número de 0 a 11.")