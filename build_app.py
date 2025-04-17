#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Script para empacotar o Gerador de Vértices em um executável
-----------------------------------------------------------
Utiliza PyInstaller para criar um executável standalone
"""

import os
import sys
import shutil
import subprocess
import platform

def obter_icone():
    """Obtém o caminho para o ícone do aplicativo."""
    # Verificar se o ícone personalizado existe
    icone_personalizado = 'resources/planeta.ico'
    if os.path.exists(icone_personalizado):
        print(f"Usando ícone personalizado: {icone_personalizado}")
        return icone_personalizado
    
    # Se não existir, retornar None
    print("Ícone personalizado não encontrado. O executável não terá um ícone personalizado.")
    return None

def criar_arquivo_spec(nome_app, icone_path):
    """Cria um arquivo .spec personalizado para o PyInstaller."""
    # Executar PyInstaller para gerar o arquivo .spec básico
    import subprocess
    subprocess.run([
        "pyinstaller",
        "--name", nome_app,
        "--windowed",  # Sem console
        "--onedir",    # Diretório único
        "--clean",     # Limpar cache
        "--specpath", ".",  # Salvar .spec no diretório atual
        "app_main.py"  # Ponto de entrada principal
    ], check=True)
    
    # Modificar o arquivo .spec usando os hooks
    try:
        from pyinstaller_hooks import modify_spec_file
        modify_spec_file(f"{nome_app}.spec", nome_app, icone_path)
    except ImportError:
        print("Aviso: pyinstaller_hooks.py não encontrado. O arquivo .spec não será modificado.")
    except Exception as e:
        print(f"Erro ao modificar o arquivo .spec: {e}")
    
    return f"{nome_app}.spec"

def criar_instalador_windows(nome_app, versao):
    """Cria um script para o NSIS (Nullsoft Scriptable Install System) para Windows."""
    # Verificar se o diretório installer existe
    if not os.path.exists('installer'):
        os.makedirs('installer')
    
    conteudo = f"""
; Script de instalação para o {nome_app}
; Gerado automaticamente

!include "MUI2.nsh"

; Informações gerais
Name "{nome_app}"
OutFile "installer\\{nome_app}_Setup_{versao}.exe"
InstallDir "$PROGRAMFILES\\{nome_app}"
InstallDirRegKey HKCU "Software\\{nome_app}" ""
RequestExecutionLevel admin

; Interface
!define MUI_ABORTWARNING
!define MUI_ICON "resources\\planeta.ico"

; Páginas
!insertmacro MUI_PAGE_WELCOME
!insertmacro MUI_PAGE_DIRECTORY
!insertmacro MUI_PAGE_INSTFILES
!insertmacro MUI_PAGE_FINISH

; Idiomas
!insertmacro MUI_LANGUAGE "PortugueseBR"

; Seção de instalação
Section "Instalar" SecInstall
  SetOutPath "$INSTDIR"
  
  ; Arquivos do aplicativo
  File /r "dist\\{nome_app}\\*.*"
  
  ; Criar atalhos
  CreateDirectory "$SMPROGRAMS\\{nome_app}"
  CreateShortcut "$SMPROGRAMS\\{nome_app}\\{nome_app}.lnk" "$INSTDIR\\{nome_app}.exe"
  CreateShortcut "$DESKTOP\\{nome_app}.lnk" "$INSTDIR\\{nome_app}.exe"
  
  ; Registrar desinstalador
  WriteRegStr HKCU "Software\\{nome_app}" "" $INSTDIR
  WriteUninstaller "$INSTDIR\\Uninstall.exe"
  WriteRegStr HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\{nome_app}" "DisplayName" "{nome_app}"
  WriteRegStr HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\{nome_app}" "UninstallString" "$INSTDIR\\Uninstall.exe"
  WriteRegStr HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\{nome_app}" "DisplayIcon" "$INSTDIR\\{nome_app}.exe"
  WriteRegStr HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\{nome_app}" "DisplayVersion" "{versao}"
  WriteRegStr HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\{nome_app}" "Publisher" "Gerador de Vértices"
SectionEnd

; Seção de desinstalação
Section "Uninstall"
  ; Remover arquivos e diretórios
  RMDir /r "$INSTDIR"
  
  ; Remover atalhos
  Delete "$SMPROGRAMS\\{nome_app}\\{nome_app}.lnk"
  RMDir "$SMPROGRAMS\\{nome_app}"
  Delete "$DESKTOP\\{nome_app}.lnk"
  
  ; Remover registros
  DeleteRegKey HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\{nome_app}"
  DeleteRegKey HKCU "Software\\{nome_app}"
SectionEnd
"""
    
    with open("installer.nsi", "w", encoding="utf-8") as f:
        f.write(conteudo)
    
    return "installer.nsi"

def main():
    """Função principal."""
    # Configurações
    nome_app = "GeradorVertices"
    versao = "1.0.0"
    
    # Verificar sistema operacional
    sistema = platform.system()
    print(f"Sistema operacional detectado: {sistema}")
    
    try:
        # Obter ícone
        print("Verificando ícone do aplicativo...")
        icone_path = obter_icone()
        
        # Criar arquivo .spec
        print("Criando arquivo .spec para o PyInstaller...")
        spec_file = criar_arquivo_spec(nome_app, icone_path if icone_path else "")
        print(f"Arquivo .spec criado: {spec_file}")
        
        # Executar PyInstaller com o arquivo .spec modificado
        print("Executando PyInstaller para criar o executável...")
        subprocess.run(["pyinstaller", spec_file, "--clean", "--noconfirm"], check=True)
        print("Executável criado com sucesso!")
        
        # Criar instalador para Windows
        if sistema == "Windows":
            print("Criando script de instalação para Windows...")
            nsi_file = criar_instalador_windows(nome_app, versao)
            print(f"Script de instalação criado: {nsi_file}")
            
            # Verificar se o NSIS está instalado
            try:
                # Tentar encontrar o makensis.exe
                makensis_path = None
                possiveis_caminhos = [
                    "C:\\Program Files\\NSIS\\makensis.exe",
                    "C:\\Program Files (x86)\\NSIS\\makensis.exe"
                ]
                
                for caminho in possiveis_caminhos:
                    if os.path.exists(caminho):
                        makensis_path = caminho
                        break
                
                if makensis_path:
                    print(f"NSIS encontrado em: {makensis_path}")
                    print("Criando instalador...")
                    subprocess.run([makensis_path, nsi_file], check=True)
                    print(f"Instalador criado em: installer\\{nome_app}_Setup_{versao}.exe")
                else:
                    print("NSIS não encontrado. Você pode instalar o NSIS de https://nsis.sourceforge.io/Download")
                    print("Depois de instalar o NSIS, execute manualmente:")
                    print(f"makensis {nsi_file}")
            except Exception as e:
                print(f"Erro ao criar instalador: {e}")
                print("Você pode criar o instalador manualmente usando o NSIS e o arquivo installer.nsi")
        
        print("\nProcesso concluído!")
        print(f"O executável está disponível em: dist\\{nome_app}\\")
        
        if sistema == "Windows":
            print("Para criar um instalador, você precisa do NSIS (Nullsoft Scriptable Install System).")
            print("1. Instale o NSIS de https://nsis.sourceforge.io/Download")
            print(f"2. Execute: makensis {nsi_file}")
    
    except Exception as e:
        print(f"Erro durante o processo: {e}")
        import traceback
        print(traceback.format_exc())
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
