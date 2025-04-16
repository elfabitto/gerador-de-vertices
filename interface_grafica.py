#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Interface Gráfica para o Gerador de Vértices
--------------------------------------------
Interface gráfica para facilitar o uso do script gerador_vertices.py
"""

import os
import sys
import threading
import traceback

# Verificar se o Tkinter está disponível
TKINTER_DISPONIVEL = True
try:
    import tkinter as tk
    from tkinter import filedialog, messagebox, ttk
except ImportError:
    TKINTER_DISPONIVEL = False
except Exception as e:
    print(f"Erro ao importar Tkinter: {e}")
    TKINTER_DISPONIVEL = False

# Importar o módulo gerador_vertices
try:
    from gerador_vertices import processar_shapefile
except ImportError:
    if TKINTER_DISPONIVEL:
        messagebox.showerror("Erro", "Não foi possível importar o módulo gerador_vertices.py")
    else:
        print("Erro: Não foi possível importar o módulo gerador_vertices.py")
    sys.exit(1)

class RedirecionadorSaida:
    """Classe para redirecionar a saída do console para um widget Text."""
    
    def __init__(self, text_widget):
        self.text_widget = text_widget
        self.buffer = ""
    
    def write(self, texto):
        self.buffer += texto
        self.text_widget.config(state=tk.NORMAL)
        self.text_widget.insert(tk.END, texto)
        self.text_widget.see(tk.END)
        self.text_widget.config(state=tk.DISABLED)
    
    def flush(self):
        pass

class AplicativoGeradorVertices:
    """Aplicativo de interface gráfica para o Gerador de Vértices."""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Gerador de Vértices")
        self.root.geometry("700x500")
        self.root.minsize(600, 400)
        
        # Configurar o estilo
        self.configurar_estilo()
        
        # Criar os widgets
        self.criar_widgets()
        
        # Centralizar a janela
        self.centralizar_janela()
    
    def configurar_estilo(self):
        """Configura o estilo da interface."""
        self.style = ttk.Style()
        self.style.configure("TButton", padding=6, relief="flat", background="#ccc")
        self.style.configure("TLabel", padding=6)
        self.style.configure("TFrame", padding=10)
    
    def criar_widgets(self):
        """Cria os widgets da interface."""
        # Frame principal
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Frame para os campos de entrada
        input_frame = ttk.LabelFrame(main_frame, text="Arquivos")
        input_frame.pack(fill=tk.X, pady=5)
        
        # Shapefile de entrada
        ttk.Label(input_frame, text="Shapefile de entrada:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.entrada_shapefile = ttk.Entry(input_frame, width=50)
        self.entrada_shapefile.grid(row=0, column=1, padx=5, pady=5, sticky=tk.W+tk.E)
        ttk.Button(input_frame, text="Procurar...", command=self.selecionar_shapefile_entrada).grid(row=0, column=2, padx=5, pady=5)
        
        # Excel de saída
        ttk.Label(input_frame, text="Excel de saída:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.saida_excel = ttk.Entry(input_frame, width=50)
        self.saida_excel.grid(row=1, column=1, padx=5, pady=5, sticky=tk.W+tk.E)
        ttk.Button(input_frame, text="Procurar...", command=self.selecionar_excel_saida).grid(row=1, column=2, padx=5, pady=5)
        
        # Shapefile de saída
        ttk.Label(input_frame, text="Shapefile de saída:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.saida_shapefile = ttk.Entry(input_frame, width=50)
        self.saida_shapefile.grid(row=2, column=1, padx=5, pady=5, sticky=tk.W+tk.E)
        ttk.Button(input_frame, text="Procurar...", command=self.selecionar_shapefile_saida).grid(row=2, column=2, padx=5, pady=5)
        
        # Configurar o grid para expandir
        input_frame.columnconfigure(1, weight=1)
        
        # Frame para os botões
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=10)
        
        # Botão de processar
        self.btn_processar = ttk.Button(button_frame, text="Processar", command=self.processar)
        self.btn_processar.pack(side=tk.RIGHT, padx=5)
        
        # Barra de progresso
        self.progresso = ttk.Progressbar(main_frame, orient=tk.HORIZONTAL, length=100, mode='indeterminate')
        self.progresso.pack(fill=tk.X, pady=5)
        
        # Frame para a saída de log
        log_frame = ttk.LabelFrame(main_frame, text="Log")
        log_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # Área de texto para o log
        self.log_text = tk.Text(log_frame, wrap=tk.WORD, state=tk.DISABLED)
        self.log_text.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)
        
        # Scrollbar para o log
        scrollbar = ttk.Scrollbar(log_frame, command=self.log_text.yview)
        scrollbar.pack(fill=tk.Y, side=tk.RIGHT)
        self.log_text.config(yscrollcommand=scrollbar.set)
        
        # Redirecionar a saída padrão para o widget de texto
        self.redirecionador = RedirecionadorSaida(self.log_text)
        sys.stdout = self.redirecionador
    
    def centralizar_janela(self):
        """Centraliza a janela na tela."""
        self.root.update_idletasks()
        largura = self.root.winfo_width()
        altura = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (largura // 2)
        y = (self.root.winfo_screenheight() // 2) - (altura // 2)
        self.root.geometry(f"{largura}x{altura}+{x}+{y}")
    
    def selecionar_shapefile_entrada(self):
        """Abre um diálogo para selecionar o shapefile de entrada."""
        arquivo = filedialog.askopenfilename(
            title="Selecionar Shapefile de Entrada",
            filetypes=[("Shapefile", "*.shp"), ("Todos os arquivos", "*.*")]
        )
        if arquivo:
            self.entrada_shapefile.delete(0, tk.END)
            self.entrada_shapefile.insert(0, arquivo)
            
            # Sugerir nomes para os arquivos de saída
            nome_base = os.path.splitext(os.path.basename(arquivo))[0]
            diretorio = os.path.dirname(arquivo)
            
            excel_sugerido = os.path.join(diretorio, f"{nome_base}_coordenadas.xlsx")
            self.saida_excel.delete(0, tk.END)
            self.saida_excel.insert(0, excel_sugerido)
            
            shapefile_sugerido = os.path.join(diretorio, f"{nome_base}_renomeado.shp")
            self.saida_shapefile.delete(0, tk.END)
            self.saida_shapefile.insert(0, shapefile_sugerido)
    
    def selecionar_excel_saida(self):
        """Abre um diálogo para selecionar o arquivo Excel de saída."""
        arquivo = filedialog.asksaveasfilename(
            title="Salvar Arquivo Excel",
            defaultextension=".xlsx",
            filetypes=[("Excel", "*.xlsx"), ("Todos os arquivos", "*.*")]
        )
        if arquivo:
            self.saida_excel.delete(0, tk.END)
            self.saida_excel.insert(0, arquivo)
    
    def selecionar_shapefile_saida(self):
        """Abre um diálogo para selecionar o shapefile de saída."""
        arquivo = filedialog.asksaveasfilename(
            title="Salvar Shapefile",
            defaultextension=".shp",
            filetypes=[("Shapefile", "*.shp"), ("Todos os arquivos", "*.*")]
        )
        if arquivo:
            self.saida_shapefile.delete(0, tk.END)
            self.saida_shapefile.insert(0, arquivo)
    
    def processar(self):
        """Processa o shapefile em uma thread separada."""
        # Verificar se o shapefile de entrada foi selecionado
        caminho_shapefile = self.entrada_shapefile.get().strip()
        if not caminho_shapefile:
            messagebox.showerror("Erro", "Selecione um shapefile de entrada.")
            return
        
        # Obter os caminhos de saída
        caminho_saida_excel = self.saida_excel.get().strip() or None
        caminho_saida_shapefile = self.saida_shapefile.get().strip() or None
        
        # Desabilitar os controles durante o processamento
        self.btn_processar.config(state=tk.DISABLED)
        self.progresso.start()
        
        # Limpar o log
        self.log_text.config(state=tk.NORMAL)
        self.log_text.delete(1.0, tk.END)
        self.log_text.config(state=tk.DISABLED)
        
        # Iniciar o processamento em uma thread separada
        threading.Thread(
            target=self.executar_processamento,
            args=(caminho_shapefile, caminho_saida_excel, caminho_saida_shapefile),
            daemon=True
        ).start()
    
    def executar_processamento(self, caminho_shapefile, caminho_saida_excel, caminho_saida_shapefile):
        """Executa o processamento do shapefile."""
        try:
            # Processar o shapefile
            processar_shapefile(caminho_shapefile, caminho_saida_excel, caminho_saida_shapefile)
            
            # Exibir mensagem de sucesso
            self.root.after(0, lambda: messagebox.showinfo("Sucesso", "Processamento concluído com sucesso!"))
        except Exception as e:
            # Exibir mensagem de erro
            traceback_str = traceback.format_exc()
            print(f"Erro: {e}\n{traceback_str}")
            self.root.after(0, lambda: messagebox.showerror("Erro", f"Ocorreu um erro durante o processamento:\n{e}"))
        finally:
            # Reabilitar os controles
            self.root.after(0, lambda: self.btn_processar.config(state=tk.NORMAL))
            self.root.after(0, lambda: self.progresso.stop())

def verificar_tkinter():
    """Verifica se o Tkinter está disponível e configurado corretamente."""
    if not TKINTER_DISPONIVEL:
        print("Erro: Tkinter não está disponível. A interface gráfica não pode ser iniciada.")
        print("Possíveis soluções:")
        print("1. Verifique se o Tkinter está instalado no seu sistema.")
        print("2. Em sistemas Windows, verifique se o Tcl/Tk está instalado corretamente.")
        print("3. Em sistemas Linux, instale o pacote python3-tk (ex: sudo apt-get install python3-tk).")
        print("\nAlternativamente, você pode usar a versão de linha de comando:")
        print("python gerador_vertices.py <caminho_shapefile> [caminho_saida_excel] [caminho_saida_shapefile]")
        return False
    return True

def main():
    """Função principal."""
    if not verificar_tkinter():
        return 1
    
    try:
        root = tk.Tk()
        app = AplicativoGeradorVertices(root)
        root.mainloop()
        return 0
    except Exception as e:
        print(f"Erro ao iniciar a interface gráfica: {e}")
        print(traceback.format_exc())
        print("\nAlternativamente, você pode usar a versão de linha de comando:")
        print("python gerador_vertices.py <caminho_shapefile> [caminho_saida_excel] [caminho_saida_shapefile]")
        return 1

if __name__ == "__main__":
    sys.exit(main())
