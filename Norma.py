import tkinter as tk
from tkinter import filedialog
from typing import NamedTuple

# 1. Definição da Estrutura da Instrução (Como uma Struct)
class Instrucao(NamedTuple):
    rotulo: str
    operacao: str
    registrador: str
    desvios: list

# 2. Inicialização dos 8 registradores padrão solicitados pelo PDF
registradores = {"A": 0, "B": 0, "C": 0, "D": 0, "E": 0, "F": 0, "G": 0, "H": 0}

def inicializar_registradores():
    """Permite ao usuário definir os valores iniciais dos registradores"""
    print("--- INICIALIZAcsO DOS REGISTRADORES ---")
    for reg in registradores.keys():
        while True:
            try:
                val = input(f"Defina o valor inicial para {reg} (padrão 0): ").strip()
                if val == "":
                    registradores[reg] = 0
                    break
                val_int = int(val)
                if val_int >= 0:
                    registradores[reg] = val_int
                    break
                else:
                    print("A Máquina Norma só aceita números inteiros não-negativos (naturais).")
            except ValueError:
                print("Por favor, digite um número inteiro válido.")
    print("\nRegistradores inicializados com sucesso!")

def selecionar_e_ler_arquivo():
    """Abre a janela para selecionar o arquivo .txt e faz o parse das instruções"""
    root = tk.Tk()
    root.withdraw() # Oculta a janela principal do tkinter
    
    caminho_arquivo = filedialog.askopenfilename(
        title="Selecione o arquivo da Macro (Instruções Rotuladas)",
        filetypes=[("Arquivos de Texto", "*.txt"), ("Todos os arquivos", "*.*")]
    )
    
    if not caminho_arquivo:
        print("Nenhum arquivo foi selecionado. Encerrando simulador.")
        return None, None

    programa = {}
    primeiro_rotulo = None

    try:
        with open(caminho_arquivo, "r", encoding="utf-8") as arquivo:
            for linha in arquivo:
                linha_limpa = linha.strip()
                # Ignora linhas vazias ou comentários
                if not linha_limpa or linha_limpa.startswith("#"):
                    continue
                
                partes = linha_limpa.split()
                if len(partes) < 4:
                    # Instruções válidas precisam de pelo menos: Rótulo Operação Registrador Desvio
                    continue
                
                rotulo = partes[0]
                operacao = partes[1].upper()
                registrador = partes[2].upper()
                desvios = partes[3:]
                
                # Guarda o primeiro rótulo encontrado para saber por onde o programa começa
                if primeiro_rotulo is None:
                    primeiro_rotulo = rotulo
                
                # Salva na estrutura indexada pelo rótulo da linha
                programa[rotulo] = Instrucao(rotulo, operacao, registrador, desvios)
                
        return programa, primeiro_rotulo
    except Exception as e:
        print(f"Erro ao ler o arquivo: {e}")
        return None, None

# 3. Funções das Operações Básicas da Máquina Norma
def op_add(registrador, desvios):
    registradores[registrador] += 1
    return desvios[0] # ADD possui apenas 1 desvio incondicional

def op_sub(registrador, desvios):
    # Garante a propriedade de não ficar menor que zero
    if registradores[registrador] > 0:
        registradores[registrador] -= 1
    return desvios[0] # SUB possui apenas 1 desvio incondicional

def op_zer(registrador, desvios):
    if registradores[registrador] == 0:
        return desvios[0] # Se for zero, vai para o primeiro desvio
    else:
        return desvios[1] # Se não for zero, vai para o segundo desvio

# 4. Interpretador / Função Principal de Execução
def executar_simulador(programa, rotulo_inicial):
    if not programa or not rotulo_inicial:
        return

    rotulo_atual = rotulo_inicial
    
    # Formata a tupla com os valores atuais para o log inicial
    valores_iniciais = tuple(registradores.values())
    print(f"\n{valores_iniciais}, M) Entrada de Dados")
    
    # O loop roda enquanto o rótulo de destino apontar para uma linha válida do arquivo
    while rotulo_atual in programa:
        cmd = programa[rotulo_atual]
        valores_regs = tuple(registradores.values())
        
        # Traduz a exibição do Log para bater com o padrão visual do PDF (Páginas 5 e 6)
        if cmd.operacao == "ZER":
            texto_instrucao = f"SE ZER ({cmd.registrador}) ENTAO VA_PARA {cmd.desvios[0]} SENAO VA_PARA {cmd.desvios[1]}"
        elif cmd.operacao == "ADD":
            texto_instrucao = f"FACA ADD ({cmd.registrador}) VA_PARA {cmd.desvios[0]}"
        elif cmd.operacao == "SUB":
            texto_instrucao = f"FACA SUB ({cmd.registrador}) VA_PARA {cmd.desvios[0]}"
        else:
            texto_instrucao = f"{cmd.operacao} {cmd.registrador} {' '.join(cmd.desvios)}"

        # Printa o log atualizado antes de executar a instrução da linha
        print(f"{valores_regs}, {cmd.rotulo}) {texto_instrucao}")
        
        # Executa a operação lógica correspondente
        if cmd.operacao == "ADD":
            proximo_rotulo = op_add(cmd.registrador, cmd.desvios)
        elif cmd.operacao == "SUB":
            proximo_rotulo = op_sub(cmd.registrador, cmd.desvios)
        elif cmd.operacao == "ZER":
            proximo_rotulo = op_zer(cmd.registrador, cmd.desvios)
        else:
            print(f"Erro: Operação desconhecida '{cmd.operacao}' na linha {cmd.rotulo}.")
            break
            
        # Atualiza o ponteiro de execução para a próxima iteração
        rotulo_atual = proximo_rotulo

    # O desvio para um rótulo inexistente encerra o loop e finaliza a máquina
    valores_finais = tuple(registradores.values())
    print(f"\n[FIM DA EXECUÇÃO] Linha de parada atingida. Linha tentada: {rotulo_atual}")
    print(f"Estado Final dos Registradores: {valores_finais}")

# 5. Inicialização do script
if __name__ == "__main__":
    print("=========================================")
    print(" SIMULADOR MAQUINA NORMA - PYTHON V1.0 ")
    print("=========================================\n")
    
    # Passo 1: Usuário seta os valores dos registradores
    inicializar_registradores()
    
    print("\nPor favor, escolha o arquivo .txt com os comandos da macro...")
    # Passo 2: Seleção e leitura do arquivo limpo (.txt)
    programa_carregado, rotulo_inicial = selecionar_e_ler_arquivo()
    
    # Passo 3: Execução das instruções com logs formatados
    if programa_carregado:
        executar_simulador(programa_carregado, rotulo_inicial)