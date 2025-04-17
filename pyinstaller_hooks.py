#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Hooks para o PyInstaller
-----------------------
Este arquivo contém hooks e configurações para o PyInstaller
garantir que todas as dependências sejam incluídas corretamente no executável.
"""

import os

# Lista de módulos ocultos que precisam ser incluídos explicitamente
hiddenimports = [
    'pandas',
    'geopandas',
    'pyproj',
    'openpyxl',
    'numpy',
    'shapely',
    'shapely.geometry',
    'PyQt5',
    'PyQt5.QtCore',
    'PyQt5.QtGui',
    'PyQt5.QtWidgets',
]

# Dados adicionais que precisam ser incluídos
datas = [
    ('resources', 'resources'),
    ('LICENSE', '.'),
    ('README_NOVO.md', '.'),
    ('requirements.txt', '.'),
]

# Binários adicionais que precisam ser incluídos
binaries = []

# Excluir módulos desnecessários para reduzir o tamanho do executável
excludes = [
    'tkinter',
    'matplotlib',
    'scipy',
    'pytest',
    'black',
    'flake8',
    'doctest',
    'pydoc',
    'unittest',
]

# Função para ser chamada pelo PyInstaller para obter as configurações
def get_hook_config():
    return {
        'hiddenimports': hiddenimports,
        'datas': datas,
        'binaries': binaries,
        'excludes': excludes,
    }

# Função para modificar o arquivo .spec gerado pelo PyInstaller
def modify_spec_file(spec_file, app_name, icon_path=None):
    """
    Modifica o arquivo .spec gerado pelo PyInstaller para incluir configurações adicionais.
    
    Args:
        spec_file (str): Caminho para o arquivo .spec
        app_name (str): Nome do aplicativo
        icon_path (str, opcional): Caminho para o ícone do aplicativo. Se None, usa o ícone padrão.
    """
    # Se o caminho do ícone não for fornecido, usar o ícone personalizado
    if not icon_path:
        if os.path.exists('resources/planeta.ico'):
            icon_path = 'resources/planeta.ico'
    with open(spec_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Adicionar configurações adicionais
    content = content.replace(
        "hiddenimports=[]",
        f"hiddenimports={hiddenimports}"
    )
    
    content = content.replace(
        "datas=[]",
        f"datas={datas}"
    )
    
    content = content.replace(
        "excludes=[]",
        f"excludes={excludes}"
    )
    
    # Adicionar ícone
    if icon_path:
        content = content.replace(
            "icon=None",
            f"icon='{icon_path}'"
        )
    
    # Salvar o arquivo modificado
    with open(spec_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"Arquivo .spec modificado: {spec_file}")
