@echo off
echo ===================================================
echo           GERADOR DE VERTICES - INICIANDO
echo ===================================================
echo.

REM Verificar se o Python está instalado
python --version > nul 2>&1
if %errorlevel% neq 0 (
    echo ERRO: Python nao encontrado!
    echo.
    echo Por favor, instale o Python 3.6 ou superior:
    echo https://www.python.org/downloads/
    echo.
    echo Certifique-se de marcar a opcao "Add Python to PATH"
    echo durante a instalacao.
    echo.
    pause
    exit /b 1
)

REM Verificar se o ambiente virtual existe
if not exist venv (
    echo Criando ambiente virtual...
    python -m venv venv
    if %errorlevel% neq 0 (
        echo ERRO: Falha ao criar ambiente virtual!
        pause
        exit /b 1
    )
)

REM Ativar o ambiente virtual
echo Ativando ambiente virtual...
call venv\Scripts\activate.bat

REM Verificar se as dependências estão instaladas
echo Verificando dependencias...
pip show pandas geopandas pyproj openpyxl numpy shapely PyQt5 > nul 2>&1
if %errorlevel% neq 0 (
    echo Instalando dependencias...
    pip install -r requirements.txt
    if %errorlevel% neq 0 (
        echo ERRO: Falha ao instalar dependencias!
        pause
        exit /b 1
    )
)

REM Iniciar o aplicativo
echo.
echo Iniciando o aplicativo...
echo.
python app_main.py

REM Desativar o ambiente virtual
call venv\Scripts\deactivate.bat

echo.
echo Aplicativo encerrado.
pause
