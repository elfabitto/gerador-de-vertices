# Gerador de Vértices

Um aplicativo completo para converter arquivos shapefile de pontos em tabelas Excel com coordenadas geográficas e UTM, e gerar novos shapefiles com pontos renomeados.

![Interface do Aplicativo](resources/app_screenshot.png)

## Funcionalidades

- Lê um arquivo shapefile de pontos
- Extrai as coordenadas dos pontos
- Converte as coordenadas para formato geográfico (latitude/longitude) e UTM
- Cria uma tabela Excel com as colunas: PONTO, LATITUDE, LONGITUDE, NORTE UTM, LESTE UTM, FUSO
- Gera um novo shapefile com os pontos renomeados como "P-01", "P-02", etc. e com as coordenadas na tabela de atributos
- Interface gráfica moderna e intuitiva
- Versão instalável para Windows

## Instalação

### Opção 1: Instalador para Windows

1. Baixe o instalador `GeradorVertices_Setup_1.0.0.exe` da [página de releases](https://github.com/seu-usuario/gerador-vertices/releases)
2. Execute o instalador e siga as instruções na tela
3. O aplicativo será instalado e atalhos serão criados no Menu Iniciar e na Área de Trabalho

### Opção 2: Instalação a partir do código-fonte

1. Clone ou baixe este repositório
2. Instale as dependências necessárias:

```bash
pip install -r requirements.txt
```

3. Execute o aplicativo:

```bash
python app_main.py
```

## Requisitos

- Python 3.6 ou superior
- Bibliotecas Python:
  - pandas
  - geopandas
  - pyproj
  - openpyxl
  - numpy
  - shapely
  - PyQt5 (para a interface gráfica)

## Uso

### Interface Gráfica

A maneira mais fácil de usar o aplicativo é através da interface gráfica moderna:

```bash
python app_main.py --gui
```

Ou simplesmente execute o aplicativo sem argumentos e selecione a opção 1:

```bash
python app_main.py
```

A interface permite:
- Selecionar o arquivo shapefile de entrada
- Definir o caminho para o arquivo Excel de saída
- Definir o caminho para o novo shapefile de saída
- Visualizar o log de processamento em tempo real

### Linha de Comando

Também é possível usar o aplicativo diretamente pela linha de comando:

```bash
python app_main.py --shapefile caminho/para/arquivo.shp --excel saida.xlsx --saida novo.shp
```

Onde:
- `--shapefile`: Caminho para o arquivo shapefile de entrada (obrigatório)
- `--excel`: Caminho para salvar o arquivo Excel de saída (opcional)
- `--saida`: Caminho para salvar o novo shapefile (opcional)

Se os caminhos de saída não forem fornecidos, serão gerados automaticamente com base no nome do arquivo de entrada.

### Criando um Shapefile de Exemplo

Para testar o aplicativo sem ter um shapefile real, você pode gerar um shapefile com pontos aleatórios:

```bash
python app_main.py --criar-exemplo --saida pontos_exemplo.shp --pontos 20 --regiao recife
```

Parâmetros:
- `--saida`: Caminho para salvar o shapefile (padrão: pontos_exemplo.shp)
- `--pontos`: Número de pontos a serem criados (padrão: 10)
- `--regiao`: Região para gerar os pontos (opções: recife, sao_paulo, rio, brasilia)

## Criando seu próprio instalador

Se você quiser criar seu próprio instalador para Windows, siga estas etapas:

1. Instale o PyInstaller e o NSIS (Nullsoft Scriptable Install System)
2. Execute o script de construção:

```bash
python build_app.py
```

Este script irá:
- Criar um ícone para o aplicativo
- Gerar um executável usando PyInstaller
- Criar um script de instalação para o NSIS
- Se o NSIS estiver instalado, criar o instalador automaticamente

O instalador será gerado em `installer/GeradorVertices_Setup_1.0.0.exe`.

## Exemplo de Saída

### Tabela Excel

A tabela Excel gerada terá o seguinte formato:

| PONTO | LATITUDE | LONGITUDE | LATITUDE_GMS | LONGITUDE_GMS | NORTE UTM | LESTE UTM | FUSO |
|-------|----------|-----------|--------------|---------------|-----------|-----------|------|
| P-01  | -8.05000 | -34.90000 | -08° 03' 00.00000" | -34° 54' 00.00000" | 9110000.0 | 290000.0  | 25   |
| P-02  | -8.05500 | -34.90500 | -08° 03' 18.00000" | -34° 54' 18.00000" | 9109000.0 | 289000.0  | 25   |
| ...   | ...      | ...       | ...          | ...           | ...       | ...       | ...  |

### Shapefile

O novo shapefile terá os mesmos pontos do shapefile original, mas com:
- Pontos renomeados no formato "P-01", "P-02", etc.
- Atributos adicionais com as coordenadas geográficas e UTM

## Como Funciona

1. O script lê o shapefile de entrada usando a biblioteca GeoPandas
2. Para cada ponto no shapefile:
   - Extrai as coordenadas x, y no sistema de coordenadas original
   - Converte para coordenadas geográficas (latitude, longitude)
   - Determina o fuso UTM com base na longitude
   - Converte para coordenadas UTM
   - Cria um nome de ponto no formato P-XX
3. Cria um DataFrame pandas com todos os dados
4. Salva o DataFrame como um arquivo Excel
5. Cria um novo GeoDataFrame com os pontos originais e os novos atributos
6. Salva o novo GeoDataFrame como um shapefile

## Licença

Este projeto é distribuído sob a licença MIT.
