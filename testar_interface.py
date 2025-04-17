#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Script para testar a interface gráfica do Gerador de Vértices
------------------------------------------------------------
Este script executa a interface gráfica e mostra uma mensagem de boas-vindas.
"""

import sys
import os
from PyQt5.QtWidgets import QApplication, QMessageBox

def main():
    """Função principal."""
    # Verificar se o arquivo app_interface.py existe
    if not os.path.exists('app_interface.py'):
        print("Erro: O arquivo app_interface.py não foi encontrado.")
        print("Certifique-se de estar no diretório correto.")
        return 1
    
    # Importar o módulo app_interface
    try:
        from app_interface import GeradorVerticesApp
    except ImportError as e:
        print(f"Erro ao importar o módulo app_interface: {e}")
        return 1
    
    # Iniciar a aplicação
    app = QApplication(sys.argv)
    
    # Mostrar mensagem de boas-vindas
    QMessageBox.information(
        None,
        "Teste da Interface",
        "Bem-vindo ao Gerador de Vértices!\n\n"
        "Este é um teste da interface gráfica.\n"
        "A interface será iniciada em seguida."
    )
    
    # Criar e exibir a janela principal
    window = GeradorVerticesApp()
    window.show()
    
    # Executar o loop de eventos
    return app.exec_()

if __name__ == "__main__":
    sys.exit(main())
