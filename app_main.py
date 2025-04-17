#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Aplicativo Gerador de Vértices
-----------------------------
Ponto de entrada principal para o aplicativo Gerador de Vértices.
Suporta interface gráfica moderna e modo de linha de comando.
"""

import os
import sys
import argparse
import traceback

def verificar_dependencias():
    """Verifica se todas as dependências necessárias estão instaladas."""
    dependencias_faltando = []
    
    # Verificar dependências principais
    try:
        import pandas
    except ImportError:
        dependencias_faltando.append("pandas")
    
    try:
        import geopandas
    except ImportError:
        dependencias_faltando.append("geopandas")
    
    try:
        import pyproj
    except ImportError:
        dependencias_faltando.append("pyproj")
    
    try:
        import openpyxl
    except ImportError:
        dependencias_faltando.append("openpyxl")
    
    try:
        import numpy
    except ImportError:
        dependencias_faltando.append("numpy")
    
    try:
        import shapely
    except ImportError:
        dependencias_faltando.append("shapely")
    
    # Verificar PyQt5 para a interface gráfica
    try:
        import PyQt5
    except ImportError:
        dependencias_faltando.append("PyQt5")
    
    return dependencias_faltando

def instalar_dependencias(dependencias):
    """Tenta instalar as dependências faltantes."""
    print("Tentando instalar dependências faltantes...")
    
    try:
        import pip
        for dep in dependencias:
            print(f"Instalando {dep}...")
            pip.main(['install', dep])
        
        print("Dependências instaladas com sucesso!")
        return True
    except Exception as e:
        print(f"Erro ao instalar dependências: {e}")
        return False

def iniciar_interface_grafica():
    """Inicia a interface gráfica moderna."""
    try:
        from app_interface import main as iniciar_gui
        return iniciar_gui()
    except ImportError:
        print("Erro: Não foi possível importar o módulo app_interface.py")
        return 1
    except Exception as e:
        print(f"Erro ao iniciar a interface gráfica: {e}")
        print(traceback.format_exc())
        return 1

def processar_via_linha_comando(args):
    """Processa o shapefile via linha de comando."""
    try:
        from gerador_vertices import processar_shapefile
        processar_shapefile(args.shapefile, args.excel, args.saida)
        return 0
    except ImportError:
        print("Erro: Não foi possível importar o módulo gerador_vertices.py")
        return 1
    except Exception as e:
        print(f"Erro ao processar o shapefile: {e}")
        print(traceback.format_exc())
        return 1

def criar_shapefile_exemplo(args):
    """Cria um shapefile de exemplo."""
    try:
        from criar_shapefile_exemplo import criar_shapefile_exemplo
        criar_shapefile_exemplo(args.saida, args.pontos, args.regiao)
        return 0
    except ImportError:
        print("Erro: Não foi possível importar o módulo criar_shapefile_exemplo.py")
        return 1
    except Exception as e:
        print(f"Erro ao criar o shapefile de exemplo: {e}")
        print(traceback.format_exc())
        return 1

def mostrar_menu_interativo():
    """Mostra um menu interativo para o usuário."""
    while True:
        print("\n" + "=" * 50)
        print("GERADOR DE VÉRTICES".center(50))
        print("=" * 50)
        print("\nEscolha uma opção:")
        print("1. Iniciar Interface Gráfica Moderna")
        print("2. Processar Shapefile via Linha de Comando")
        print("3. Criar Shapefile de Exemplo")
        print("4. Sair")
        
        try:
            opcao = int(input("\nOpção: "))
        except ValueError:
            print("Opção inválida. Por favor digite um número.")
            continue
        
        if opcao == 1:
            # Iniciar a interface gráfica
            return iniciar_interface_grafica()
        elif opcao == 2:
            # Processar shapefile via linha de comando
            shapefile = input("Caminho para o shapefile de entrada: ")
            if not shapefile:
                print("Caminho do shapefile é obrigatório.")
                continue
            
            excel = input("Caminho para o arquivo Excel de saída (opcional): ")
            if not excel:
                excel = None
            
            saida = input("Caminho para o shapefile de saída (opcional): ")
            if not saida:
                saida = None
            
            # Criar um objeto args simulado
            class Args:
                pass
            
            args = Args()
            args.shapefile = shapefile
            args.excel = excel
            args.saida = saida
            
            return processar_via_linha_comando(args)
        elif opcao == 3:
            # Criar shapefile de exemplo
            saida = input("Caminho para salvar o shapefile de exemplo (padrão: pontos_exemplo.shp): ")
            if not saida:
                saida = "pontos_exemplo.shp"
            
            try:
                pontos = int(input("Número de pontos (padrão: 10): "))
            except ValueError:
                pontos = 10
            
            regiao = input("Região (recife, sao_paulo, rio, brasilia) (padrão: recife): ")
            if not regiao or regiao not in ["recife", "sao_paulo", "rio", "brasilia"]:
                regiao = "recife"
            
            # Criar um objeto args simulado
            class Args:
                pass
            
            args = Args()
            args.saida = saida
            args.pontos = pontos
            args.regiao = regiao
            
            return criar_shapefile_exemplo(args)
        elif opcao == 4:
            # Sair
            print("Saindo...")
            return 0
        else:
            print("Opção inválida. Por favor escolha uma opção válida.")

def main():
    """Função principal."""
    # Verificar se estamos executando como um executável empacotado
    executavel_empacotado = getattr(sys, 'frozen', False)
    
    # Se for um executável empacotado, iniciar diretamente a interface gráfica
    if executavel_empacotado:
        return iniciar_interface_grafica()
    
    # Verificar dependências apenas se não for um executável empacotado
    if not executavel_empacotado:
        dependencias_faltando = verificar_dependencias()
        if dependencias_faltando:
            print("Algumas dependências estão faltando:")
            for dep in dependencias_faltando:
                print(f"- {dep}")
            
            resposta = input("Deseja tentar instalar as dependências faltantes? (s/n): ")
            if resposta.lower() == 's':
                if not instalar_dependencias(dependencias_faltando):
                    print("Não foi possível instalar todas as dependências.")
                    print("Por favor, instale manualmente usando:")
                    print(f"pip install {' '.join(dependencias_faltando)}")
                    return 1
            else:
                print("Por favor, instale as dependências manualmente usando:")
                print(f"pip install {' '.join(dependencias_faltando)}")
                return 1
    
    # Configurar o parser de argumentos
    parser = argparse.ArgumentParser(
        description="Gerador de Vértices - Converte shapefile de pontos em tabela Excel e gera novo shapefile com pontos renomeados."
    )
    
    # Adicionar argumentos
    parser.add_argument("--gui", action="store_true", help="Iniciar a interface gráfica moderna")
    parser.add_argument("--criar-exemplo", action="store_true", help="Criar um shapefile de exemplo")
    parser.add_argument("--shapefile", help="Caminho para o shapefile de entrada")
    parser.add_argument("--excel", help="Caminho para o arquivo Excel de saída")
    parser.add_argument("--saida", help="Caminho para o shapefile de saída")
    parser.add_argument("--pontos", type=int, default=10, help="Número de pontos para o shapefile de exemplo")
    parser.add_argument("--regiao", default="recife",
                        choices=["recife", "sao_paulo", "rio", "brasilia"],
                        help="Região para gerar os pontos do shapefile de exemplo")
    
    # Analisar argumentos
    args = parser.parse_args()
    
    # Verificar se o usuário forneceu algum argumento
    if len(sys.argv) == 1:
        # Nenhum argumento fornecido, iniciar interface gráfica por padrão
        return iniciar_interface_grafica()
    
    # Processar argumentos
    if args.gui:
        # Iniciar a interface gráfica
        return iniciar_interface_grafica()
    elif args.criar_exemplo:
        # Criar shapefile de exemplo
        return criar_shapefile_exemplo(args)
    elif args.shapefile:
        # Processar o shapefile via linha de comando
        return processar_via_linha_comando(args)
    else:
        # Nenhuma ação específica, mostrar ajuda
        parser.print_help()
        return 0

if __name__ == "__main__":
    sys.exit(main())
