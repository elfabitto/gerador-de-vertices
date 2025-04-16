#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Criador de Shapefile de Exemplo
-------------------------------
Script para criar um shapefile de exemplo com pontos aleatórios
para testar o Gerador de Vértices.
"""

import os
import numpy as np
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point

def criar_shapefile_exemplo(caminho_saida="pontos_exemplo.shp", num_pontos=10, regiao="recife"):
    """
    Cria um shapefile de exemplo com pontos aleatórios.
    
    Args:
        caminho_saida (str): Caminho para salvar o shapefile
        num_pontos (int): Número de pontos a serem criados
        regiao (str): Região para gerar os pontos ('recife', 'sao_paulo', 'rio', 'brasilia')
    
    Returns:
        GeoDataFrame: O GeoDataFrame criado
    """
    # Definir limites de coordenadas para diferentes regiões
    regioes = {
        "recife": {
            "lat_min": -8.1,
            "lat_max": -7.9,
            "lon_min": -35.0,
            "lon_max": -34.8
        },
        "sao_paulo": {
            "lat_min": -23.65,
            "lat_max": -23.45,
            "lon_min": -46.8,
            "lon_max": -46.6
        },
        "rio": {
            "lat_min": -23.0,
            "lat_max": -22.8,
            "lon_min": -43.3,
            "lon_max": -43.1
        },
        "brasilia": {
            "lat_min": -15.9,
            "lat_max": -15.7,
            "lon_min": -48.0,
            "lon_max": -47.8
        }
    }
    
    # Usar a região especificada ou recife como padrão
    if regiao not in regioes:
        print(f"Região '{regiao}' não encontrada. Usando 'recife' como padrão.")
        regiao = "recife"
    
    limites = regioes[regiao]
    
    # Gerar coordenadas aleatórias
    np.random.seed(42)  # Para reprodutibilidade
    latitudes = np.random.uniform(limites["lat_min"], limites["lat_max"], num_pontos)
    longitudes = np.random.uniform(limites["lon_min"], limites["lon_max"], num_pontos)
    
    # Criar geometrias de pontos
    geometrias = [Point(lon, lat) for lon, lat in zip(longitudes, latitudes)]
    
    # Criar um GeoDataFrame
    gdf = gpd.GeoDataFrame(
        {
            "id": range(1, num_pontos + 1),
            "nome": [f"Ponto {i}" for i in range(1, num_pontos + 1)]
        },
        geometry=geometrias,
        crs="EPSG:4326"  # WGS84
    )
    
    # Salvar como shapefile
    gdf.to_file(caminho_saida)
    print(f"Shapefile de exemplo criado com {num_pontos} pontos em '{caminho_saida}'")
    
    return gdf

def main():
    """Função principal."""
    import argparse
    
    # Configurar o parser de argumentos
    parser = argparse.ArgumentParser(description="Cria um shapefile de exemplo com pontos aleatórios.")
    parser.add_argument("--saida", "-o", default="pontos_exemplo.shp", help="Caminho para salvar o shapefile")
    parser.add_argument("--pontos", "-n", type=int, default=10, help="Número de pontos a serem criados")
    parser.add_argument("--regiao", "-r", default="recife", 
                        choices=["recife", "sao_paulo", "rio", "brasilia"],
                        help="Região para gerar os pontos")
    
    # Analisar os argumentos
    args = parser.parse_args()
    
    # Criar o shapefile
    criar_shapefile_exemplo(args.saida, args.pontos, args.regiao)

if __name__ == "__main__":
    main()
