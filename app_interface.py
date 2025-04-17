#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Interface Gráfica Moderna para o Gerador de Vértices
---------------------------------------------------
Interface gráfica baseada em PyQt5 para o Gerador de Vértices
"""

import os
import sys
import threading
import traceback
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                            QLabel, QLineEdit, QPushButton, QFileDialog, QTextEdit, 
                            QProgressBar, QMessageBox, QGroupBox, QGridLayout, QSplashScreen)
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QSize
from PyQt5.QtGui import QIcon, QPixmap, QFont

# Importar o módulo gerador_vertices
try:
    from gerador_vertices import processar_shapefile
except ImportError:
    print("Erro: Não foi possível importar o módulo gerador_vertices.py")
    sys.exit(1)

class ProcessadorThread(QThread):
    """Thread para processar o shapefile sem bloquear a interface."""
    concluido = pyqtSignal(bool, str)  # Sinal para indicar conclusão (sucesso, mensagem)
    progresso = pyqtSignal(str)  # Sinal para atualizar o progresso

    def __init__(self, caminho_shapefile, caminho_saida_excel, caminho_saida_shapefile):
        super().__init__()
        self.caminho_shapefile = caminho_shapefile
        self.caminho_saida_excel = caminho_saida_excel
        self.caminho_saida_shapefile = caminho_saida_shapefile
        self.mensagem = ""
        self.cancelado = False

    def run(self):
        """Executa o processamento do shapefile."""
        try:
            # Verificar se o arquivo existe
            if not os.path.exists(self.caminho_shapefile):
                raise FileNotFoundError(f"O arquivo {self.caminho_shapefile} não foi encontrado.")
            
            # Verificar se é um arquivo shapefile
            if not self.caminho_shapefile.lower().endswith('.shp'):
                self.progresso.emit(f"Aviso: O arquivo {self.caminho_shapefile} não tem extensão .shp")
            
            # Emitir mensagem de início
            self.progresso.emit(f"Iniciando processamento do shapefile: {self.caminho_shapefile}")
            
            # Processar o shapefile
            processar_shapefile(self.caminho_shapefile, self.caminho_saida_excel, self.caminho_saida_shapefile)
            
            # Verificar se os arquivos de saída foram criados
            if self.caminho_saida_excel and not os.path.exists(self.caminho_saida_excel):
                self.progresso.emit(f"Aviso: O arquivo Excel de saída não foi criado: {self.caminho_saida_excel}")
            
            if self.caminho_saida_shapefile and not os.path.exists(self.caminho_saida_shapefile):
                self.progresso.emit(f"Aviso: O shapefile de saída não foi criado: {self.caminho_saida_shapefile}")
            
            # Emitir sinal de conclusão com sucesso
            self.concluido.emit(True, "Processamento concluído com sucesso!")
        except Exception as e:
            # Capturar o erro
            traceback_str = traceback.format_exc()
            self.mensagem = f"Erro: {e}\n{traceback_str}"
            
            # Emitir mensagem de erro para o log
            self.progresso.emit(f"ERRO: {str(e)}")
            
            # Emitir sinal de conclusão com falha
            self.concluido.emit(False, self.mensagem)


class RedirecionadorSaida:
    """Classe para redirecionar a saída do console para um widget QTextEdit."""

    def __init__(self, text_widget):
        self.text_widget = text_widget
        self.buffer = ""

    def write(self, texto):
        self.buffer += texto
        self.text_widget.append(texto)
        # Rolar para o final
        cursor = self.text_widget.textCursor()
        cursor.movePosition(cursor.End)
        self.text_widget.setTextCursor(cursor)

    def flush(self):
        pass


class GeradorVerticesApp(QMainWindow):
    """Aplicativo principal do Gerador de Vértices."""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gerador de Vértices")
        self.setMinimumSize(800, 600)
        
        # Definir o ícone da janela
        icone_path = "resources/planeta.ico"
        if os.path.exists(icone_path):
            self.setWindowIcon(QIcon(icone_path))
        
        # Configurar a interface
        self.setup_ui()
        
        # Centralizar a janela
        self.centralizar_janela()
        
        # Redirecionar a saída padrão para o widget de texto
        self.redirecionador = RedirecionadorSaida(self.log_text)
        sys.stdout = self.redirecionador

    def setup_ui(self):
        """Configura a interface do usuário."""
        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Layout principal
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)
        
        # Título
        titulo_label = QLabel("Gerador de Vértices")
        titulo_label.setAlignment(Qt.AlignCenter)
        titulo_font = QFont()
        titulo_font.setPointSize(16)
        titulo_font.setBold(True)
        titulo_label.setFont(titulo_font)
        main_layout.addWidget(titulo_label)
        
        # Descrição
        descricao_label = QLabel("Converte shapefile de pontos em tabela Excel e gera novo shapefile com pontos renomeados")
        descricao_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(descricao_label)
        
        # Grupo de arquivos
        arquivos_group = QGroupBox("Arquivos")
        arquivos_layout = QGridLayout()
        arquivos_group.setLayout(arquivos_layout)
        
        # Shapefile de entrada
        arquivos_layout.addWidget(QLabel("Shapefile de entrada:"), 0, 0)
        self.entrada_shapefile = QLineEdit()
        arquivos_layout.addWidget(self.entrada_shapefile, 0, 1)
        btn_entrada = QPushButton("Procurar...")
        btn_entrada.clicked.connect(self.selecionar_shapefile_entrada)
        arquivos_layout.addWidget(btn_entrada, 0, 2)
        
        # Excel de saída
        arquivos_layout.addWidget(QLabel("Excel de saída:"), 1, 0)
        self.saida_excel = QLineEdit()
        arquivos_layout.addWidget(self.saida_excel, 1, 1)
        btn_excel = QPushButton("Procurar...")
        btn_excel.clicked.connect(self.selecionar_excel_saida)
        arquivos_layout.addWidget(btn_excel, 1, 2)
        
        # Shapefile de saída
        arquivos_layout.addWidget(QLabel("Shapefile de saída:"), 2, 0)
        self.saida_shapefile = QLineEdit()
        arquivos_layout.addWidget(self.saida_shapefile, 2, 1)
        btn_saida = QPushButton("Procurar...")
        btn_saida.clicked.connect(self.selecionar_shapefile_saida)
        arquivos_layout.addWidget(btn_saida, 2, 2)
        
        main_layout.addWidget(arquivos_group)
        
        # Botões de ação
        botoes_layout = QHBoxLayout()
        botoes_layout.addStretch()
        
        self.btn_processar = QPushButton("Processar")
        self.btn_processar.setMinimumWidth(120)
        self.btn_processar.clicked.connect(self.processar)
        botoes_layout.addWidget(self.btn_processar)
        
        main_layout.addLayout(botoes_layout)
        
        # Barra de progresso
        self.progresso = QProgressBar()
        self.progresso.setTextVisible(False)
        main_layout.addWidget(self.progresso)
        
        # Grupo de log
        log_group = QGroupBox("Log de Processamento")
        log_layout = QVBoxLayout()
        log_group.setLayout(log_layout)
        
        # Área de texto para o log
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        log_layout.addWidget(self.log_text)
        
        main_layout.addWidget(log_group, 1)  # Stretch factor 1 para expandir

    def centralizar_janela(self):
        """Centraliza a janela na tela."""
        frame_geometry = self.frameGeometry()
        screen_center = QApplication.desktop().availableGeometry().center()
        frame_geometry.moveCenter(screen_center)
        self.move(frame_geometry.topLeft())

    def selecionar_shapefile_entrada(self):
        """Abre um diálogo para selecionar o shapefile de entrada."""
        arquivo, _ = QFileDialog.getOpenFileName(
            self,
            "Selecionar Shapefile de Entrada",
            "",
            "Shapefile (*.shp);;Todos os arquivos (*.*)"
        )
        if arquivo:
            self.entrada_shapefile.setText(arquivo)
            
            # Sugerir nomes para os arquivos de saída
            nome_base = os.path.splitext(os.path.basename(arquivo))[0]
            diretorio = os.path.dirname(arquivo)
            
            excel_sugerido = os.path.join(diretorio, f"{nome_base}_coordenadas.xlsx")
            self.saida_excel.setText(excel_sugerido)
            
            shapefile_sugerido = os.path.join(diretorio, f"{nome_base}_renomeado.shp")
            self.saida_shapefile.setText(shapefile_sugerido)

    def selecionar_excel_saida(self):
        """Abre um diálogo para selecionar o arquivo Excel de saída."""
        arquivo, _ = QFileDialog.getSaveFileName(
            self,
            "Salvar Arquivo Excel",
            "",
            "Excel (*.xlsx);;Todos os arquivos (*.*)"
        )
        if arquivo:
            self.saida_excel.setText(arquivo)

    def selecionar_shapefile_saida(self):
        """Abre um diálogo para selecionar o shapefile de saída."""
        arquivo, _ = QFileDialog.getSaveFileName(
            self,
            "Salvar Shapefile",
            "",
            "Shapefile (*.shp);;Todos os arquivos (*.*)"
        )
        if arquivo:
            self.saida_shapefile.setText(arquivo)

    def processar(self):
        """Processa o shapefile em uma thread separada."""
        try:
            # Verificar se o shapefile de entrada foi selecionado
            caminho_shapefile = self.entrada_shapefile.text().strip()
            if not caminho_shapefile:
                QMessageBox.critical(self, "Erro", "Selecione um shapefile de entrada.")
                return
            
            # Verificar se o arquivo existe
            if not os.path.exists(caminho_shapefile):
                QMessageBox.critical(self, "Erro", f"O arquivo {caminho_shapefile} não existe.")
                return
            
            # Verificar se é um arquivo shapefile
            if not caminho_shapefile.lower().endswith('.shp'):
                resposta = QMessageBox.question(
                    self, 
                    "Confirmar", 
                    f"O arquivo selecionado não parece ser um shapefile (.shp). Deseja continuar mesmo assim?",
                    QMessageBox.Yes | QMessageBox.No,
                    QMessageBox.No
                )
                if resposta == QMessageBox.No:
                    return
            
            # Obter os caminhos de saída
            caminho_saida_excel = self.saida_excel.text().strip() or None
            caminho_saida_shapefile = self.saida_shapefile.text().strip() or None
            
            # Desabilitar os controles durante o processamento
            self.btn_processar.setEnabled(False)
            self.progresso.setRange(0, 0)  # Modo indeterminado
            
            # Limpar o log
            self.log_text.clear()
            
            # Iniciar o processamento em uma thread separada
            self.thread = ProcessadorThread(caminho_shapefile, caminho_saida_excel, caminho_saida_shapefile)
            self.thread.concluido.connect(self.processamento_concluido)
            self.thread.progresso.connect(self.atualizar_progresso)
            self.thread.start()
            
            # Mostrar mensagem de processamento
            self.log_text.append("Processando shapefile, por favor aguarde...")
            
        except Exception as e:
            # Capturar qualquer exceção não tratada
            QMessageBox.critical(self, "Erro", f"Ocorreu um erro ao iniciar o processamento:\n{str(e)}")
            self.btn_processar.setEnabled(True)
            self.progresso.setRange(0, 100)
            self.progresso.setValue(0)
            
            # Registrar o erro no log
            self.log_text.append(f"ERRO: {str(e)}")
            import traceback
            self.log_text.append(traceback.format_exc())

    def atualizar_progresso(self, mensagem):
        """Atualiza o log de progresso."""
        self.log_text.append(mensagem)
        # Rolar para o final
        cursor = self.log_text.textCursor()
        cursor.movePosition(cursor.End)
        self.log_text.setTextCursor(cursor)
        # Processar eventos para atualizar a interface
        QApplication.processEvents()

    def processamento_concluido(self, sucesso, mensagem):
        """Callback chamado quando o processamento é concluído."""
        # Reabilitar os controles
        self.btn_processar.setEnabled(True)
        self.progresso.setRange(0, 100)
        self.progresso.setValue(100 if sucesso else 0)
        
        # Exibir mensagem no log
        if sucesso:
            self.log_text.append("✅ " + mensagem)
        else:
            self.log_text.append("❌ Erro durante o processamento")
            # Adicionar detalhes do erro ao log
            for linha in mensagem.split('\n'):
                if linha.strip():
                    self.log_text.append("   " + linha)
        
        # Exibir mensagem em diálogo
        if sucesso:
            QMessageBox.information(self, "Sucesso", mensagem)
        else:
            QMessageBox.critical(self, "Erro", "Ocorreu um erro durante o processamento.\nConsulte o log para mais detalhes.")


def main():
    """Função principal."""
    app = QApplication(sys.argv)
    app.setStyle('Fusion')  # Estilo moderno e consistente
    
    # Configurar estilo da aplicação
    app.setStyleSheet("""
        QMainWindow, QDialog {
            background-color: #f5f5f5;
        }
        QGroupBox {
            font-weight: bold;
            border: 1px solid #cccccc;
            border-radius: 5px;
            margin-top: 1ex;
            padding-top: 10px;
        }
        QGroupBox::title {
            subcontrol-origin: margin;
            subcontrol-position: top center;
            padding: 0 5px;
        }
        QPushButton {
            background-color: #4a86e8;
            color: white;
            border: none;
            padding: 8px 16px;
            border-radius: 4px;
        }
        QPushButton:hover {
            background-color: #3a76d8;
        }
        QPushButton:pressed {
            background-color: #2a66c8;
        }
        QPushButton:disabled {
            background-color: #cccccc;
        }
        QLineEdit {
            padding: 6px;
            border: 1px solid #cccccc;
            border-radius: 4px;
        }
        QTextEdit {
            border: 1px solid #cccccc;
            border-radius: 4px;
        }
    """)
    
    # Criar e exibir a janela principal
    window = GeradorVerticesApp()
    window.show()
    
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
