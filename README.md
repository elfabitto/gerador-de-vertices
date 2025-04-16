# Gerador de Vértices

Um aplicativo Python para converter arquivos shapefile de pontos em tabelas Excel com coordenadas geográficas e UTM, e gerar novos shapefiles com pontos renomeados.

## Funcionalidades

- Lê um arquivo shapefile de pontos
- Extrai as coordenadas dos pontos
- Converte as coordenadas para formato geográfico (latitude/longitude) e UTM
- Cria uma tabela Excel com as colunas: PONTO, LATITUDE, LONGITUDE, NORTE UTM, LESTE UTM, FUSO
- Gera um novo shapefile com os pontos renomeados como "P-01", "P-02", etc. e com as coordenadas na tabela de atributos

## Requisitos

- Python 3.6 ou superior
- Bibliotecas Python:
  - pandas
  - geopandas
  - pyproj
  - openpyxl
  - numpy
  - shapely
  - tkinter (para a interface gráfica)

### Nota sobre o Tkinter

A interface gráfica requer o Tkinter, que geralmente vem instalado com o Python. No entanto, em alguns sistemas, pode ser necessário instalá-lo separadamente:

- **Windows**: Se você encontrar erros relacionados ao Tcl/Tk, verifique se o Python foi instalado com a opção "tcl/tk and IDLE" marcada. Caso contrário, reinstale o Python com essa opção.
- **Linux**: Instale o pacote python3-tk:
  ```bash
  sudo apt-get install python3-tk  # Para distribuições baseadas em Debian/Ubuntu
  sudo dnf install python3-tkinter  # Para distribuições baseadas em Fedora
  ```
- **macOS**: Instale o Tcl/Tk via Homebrew:
  ```bash
  brew install python-tk
  ```

Se você não conseguir instalar o Tkinter, ainda poderá usar o aplicativo através da linha de comando.

## Instalação

1. Clone ou baixe este repositório
2. Instale as dependências necessárias usando o arquivo requirements.txt:

```bash
pip install -r requirements.txt
```

Alternativamente, você pode instalar as dependências manualmente:

```bash
pip install pandas geopandas openpyxl pyproj numpy shapely
```

## Uso

### Inicialização Rápida

A maneira mais fácil de começar é usar o script de inicialização, que oferece um menu interativo:

```bash
python iniciar.py
```

Este script permite:
- Iniciar a interface gráfica
- Processar um shapefile via linha de comando
- Criar um shapefile de exemplo
- Sair do programa

Você também pode usar argumentos de linha de comando com o script de inicialização:

```bash
# Iniciar a interface gráfica
python iniciar.py --gui

# Processar um shapefile
python iniciar.py --shapefile caminho/para/arquivo.shp --excel saida.xlsx --saida novo.shp

# Criar um shapefile de exemplo
python iniciar.py --criar-exemplo --saida exemplo.shp --pontos 15 --regiao sao_paulo
```

### Criando um Shapefile de Exemplo

Para testar o aplicativo sem ter um shapefile real, você pode usar o script `criar_shapefile_exemplo.py` para gerar um shapefile com pontos aleatórios:

```bash
python criar_shapefile_exemplo.py --saida pontos_exemplo.shp --pontos 20 --regiao recife
```

Parâmetros:
- `--saida` ou `-o`: Caminho para salvar o shapefile (padrão: pontos_exemplo.shp)
- `--pontos` ou `-n`: Número de pontos a serem criados (padrão: 10)
- `--regiao` ou `-r`: Região para gerar os pontos (opções: recife, sao_paulo, rio, brasilia)

### Interface Gráfica

A maneira mais fácil de usar o aplicativo é através da interface gráfica:

```bash
python interface_grafica.py
```

A interface permite:
- Selecionar o arquivo shapefile de entrada
- Definir o caminho para o arquivo Excel de saída
- Definir o caminho para o novo shapefile de saída
- Visualizar o log de processamento em tempo real

### Linha de Comando

Também é possível usar o script diretamente pela linha de comando:

```bash
python gerador_vertices.py <caminho_shapefile> [caminho_saida_excel] [caminho_saida_shapefile]
```

Onde:
- `<caminho_shapefile>`: Caminho para o arquivo shapefile de entrada (obrigatório)
- `[caminho_saida_excel]`: Caminho para salvar o arquivo Excel de saída (opcional)
- `[caminho_saida_shapefile]`: Caminho para salvar o novo shapefile (opcional)

Se os caminhos de saída não forem fornecidos, serão gerados automaticamente com base no nome do arquivo de entrada.

## Exemplo de Saída

### Tabela Excel

A tabela Excel gerada terá o seguinte formato:

| PONTO | LATITUDE | LONGITUDE | NORTE UTM | LESTE UTM | FUSO |
|-------|----------|-----------|-----------|-----------|------|
| P-01  | -8.05000 | -34.90000 | 9110000.0 | 290000.0  | 25   |
| P-02  | -8.05500 | -34.90500 | 9109000.0 | 289000.0  | 25   |
| ...   | ...      | ...       | ...       | ...       | ...  |

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
