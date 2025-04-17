# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['app_main.py'],
    pathex=[],
    binaries=[],
    datas=[
        # Arquivos do projeto
        ('resources', 'resources'), 
        ('LICENSE', '.'), 
        ('README_NOVO.md', '.'), 
        ('requirements.txt', '.'), 
        ('app_interface.py', '.'), 
        ('gerador_vertices.py', '.'),
        
        # Diretórios de dados do pyogrio
        ('venv/Lib/site-packages/pyogrio/gdal_data', 'pyogrio/gdal_data'),
        ('venv/Lib/site-packages/pyogrio/proj_data', 'pyogrio/proj_data'),
        
        # Diretórios de dados do fiona
        ('venv/Lib/site-packages/fiona/gdal_data', 'fiona/gdal_data'),
        ('venv/Lib/site-packages/fiona/proj_data', 'fiona/proj_data'),
    ],
    hiddenimports=[
        # Dependências principais
        'pandas', 'geopandas', 'pyproj', 'openpyxl', 'numpy', 'shapely', 'shapely.geometry',
        
        # Interface gráfica
        'PyQt5', 'PyQt5.QtCore', 'PyQt5.QtGui', 'PyQt5.QtWidgets',
        
        # Módulos para leitura de shapefile
        'pyogrio', 'pyogrio._geometry', 'pyogrio._io', 'pyogrio._ogr', 'pyogrio._vsi', 'pyogrio.raw', 'pyogrio.geopandas',
        'fiona', 'fiona.collection', 'fiona.env', 'fiona._env', 'fiona.schema', 'fiona.ogrext',
        
        # Dependências do fiona
        'click', 'click_plugins', 'cligj', 'attrs',
        
        # Outros módulos que podem ser necessários
        'certifi', 'packaging'
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['tkinter', 'matplotlib', 'scipy', 'pytest', 'black', 'flake8', 'doctest', 'pydoc', 'unittest'],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='GeradorVertices',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    icon='resources/planeta.ico',
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='GeradorVertices',
)
