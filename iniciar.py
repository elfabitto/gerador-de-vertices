#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Inicializador do Gerador de Vértices
-----------------------------------
Script para iniciar o Gerador de Vértices, permitindo escolher
entre a interface gráfica ou a linha de comando.
"""

import os
import sys
import argparse

def verificar_tkinter_disponivel():
    """Verifica se o Tkinter está disponível."""
    try:
        import tkinter
        return True
    except ImportError:
        return False
    except Exception as e:
        print(f"Erro ao importar Tkinter: {e}")
        return False

def main():
    """Função principal."""
    parser = argparse.ArgumentParser(
        description="Gerador de Vértices - Converte shapefile de pontos em tabela Excel e gera novo shapefile com pontos renomeados."
    )
    
    # Adicionar argumentos
    parser.add_argument("--gui", action="store_true", help="Iniciar a interface gráfica")
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
        # Nenhum argumento fornecido, mostrar menu interativo
        mostrar_menu()
        return
    
    # Processar argumentos
    if args.criar_exemplo:
        # Importar o módulo de criação de shapefile de exemplo
        try:
            from criar_shapefile_exemplo import criar_shapefile_exemplo
            caminho_saida = args.saida or "pontos_exemplo.shp"
            criar_shapefile_exemplo(caminho_saida, args.pontos, args.regiao)
        except ImportError:
            print("Erro: Não foi possível importar o módulo criar_shapefile_exemplo.py")
            sys.exit(1)
    elif args.gui:
        # Verificar se o Tkinter está disponível
        if not verificar_tkinter_disponivel():
            print("Erro: Tkinter não está disponível. A interface gráfica não pode ser iniciada.")
            print("Possíveis soluções:")
            print("1. Verifique se o Tkinter está instalado no seu sistema.")
            print("2. Em sistemas Windows, verifique se o Tcl/Tk está instalado corretamente.")
            print("3. Em sistemas Linux, instale o pacote python3-tk (ex: sudo apt-get install python3-tk).")
            print("\nAlternativamente, você pode usar a versão de linha de comando:")
            print("python gerador_vertices.py <caminho_shapefile> [caminho_saida_excel] [caminho_saida_shapefile]")
            sys.exit(1)
        
        # Iniciar a interface gráfica
        try:
            from interface_grafica import main as iniciar_gui
            iniciar_gui()
        except ImportError:
            print("Erro: Não foi possível importar o módulo interface_grafica.py")
            sys.exit(1)
        except Exception as e:
            print(f"Erro ao iniciar a interface gráfica: {e}")
            import traceback
            print(traceback.format_exc())
            sys.exit(1)
    elif args.shapefile:
        # Processar o shapefile via linha de comando
        try:
            from gerador_vertices import processar_shapefile
            processar_shapefile(args.shapefile, args.excel, args.saida)
        except ImportError:
            print("Erro: Não foi possível importar o módulo gerador_vertices.py")
            sys.exit(1)
    else:
        # Nenhuma ação específica, mostrar ajuda
        parser.print_help()

def mostrar_menu():
    """Mostra um menu interativo para o usuário."""
    while True:
        print("\n" + "=" * 50)
        print("GERADOR DE VÉRTICES".center(50))
        print("=" * 50)
        print("\nEscolha uma opção:")
        print("1. Iniciar Interface Gráfica")
        print("2. Processar Shapefile via Linha de Comando")
        print("3. Criar Shapefile de Exemplo")
        print("4. Sair")
        
        try:
            opcao = int(input("\nOpção: "))
        except ValueError:
            print("Opção inválida. Por favor, digite um número.")
            continue
        
        if opcao == 1:
            # Verificar se o Tkinter está disponível
            if not verificar_tkinter_disponivel():
                print("Erro: Tkinter não está disponível. A interface gráfica não pode ser iniciada.")
                print("Possíveis soluções:")
                print("1. Verifique se o Tkinter está instalado no seu sistema.")
                print("2. Em sistemas Windows, verifique se o Tcl/Tk está instalado corretamente.")
                print("3. Em sistemas Linux, instale o pacote python3-tk (ex: sudo apt-get install python3-tk).")
                print("\nAlternativamente, você pode usar a versão de linha de comando (opção 2).")
                continue
            
            # Iniciar a interface gráfica
            try:
                from interface_grafica import main as iniciar_gui
                codigo_saida = iniciar_gui()
                if codigo_saida != 0:
                    print("A interface gráfica não pôde ser iniciada. Usando a versão de linha de comando.")
                    continue
                break
            except ImportError:
                print("Erro: Não foi possível importar o módulo interface_grafica.py")
                continue
            except Exception as e:
                print(f"Erro ao iniciar a interface gráfica: {e}")
                import traceback
                print(traceback.format_exc())
                continue
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
            
            try:
                from gerador_vertices import processar_shapefile
                processar_shapefile(shapefile, excel, saida)
                break
            except ImportError:
                print("Erro: Não foi possível importar o módulo gerador_vertices.py")
                continue
            except Exception as e:
                print(f"Erro ao processar o shapefile: {e}")
                continue
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
            
            try:
                from criar_shapefile_exemplo import criar_shapefile_exemplo
                criar_shapefile_exemplo(saida, pontos, regiao)
                break
            except ImportError:
                print("Erro: Não foi possível importar o módulo criar_shapefile_exemplo.py")
                continue
            except Exception as e:
                print(f"Erro ao criar o shapefile de exemplo: {e}")
                continue
        elif opcao == 4:
            # Sair
            print("Saindo...")
            break
        else:
            print("Opção inválida. Por favor, escolha uma opção válida.")

if __name__ == "__main__":
    main()
