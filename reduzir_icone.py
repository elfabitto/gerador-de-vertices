#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Script para reduzir o tamanho do ícone
-------------------------------------
Este script reduz o tamanho do ícone para um tamanho normal de ícone de área de trabalho.
"""

import os
from PIL import Image

def reduzir_icone(caminho_icone, caminho_saida=None, tamanhos=[16, 32, 48, 64]):
    """
    Reduz o tamanho do ícone para os tamanhos especificados.
    
    Args:
        caminho_icone (str): Caminho para o ícone original
        caminho_saida (str, opcional): Caminho para salvar o novo ícone. Se None, sobrescreve o original.
        tamanhos (list, opcional): Lista de tamanhos para o ícone. Padrão é [16, 32, 48, 64].
    """
    if caminho_saida is None:
        caminho_saida = caminho_icone
    
    # Verificar se o arquivo existe
    if not os.path.exists(caminho_icone):
        print(f"Erro: O arquivo {caminho_icone} não existe.")
        return False
    
    try:
        # Abrir o ícone original
        img = Image.open(caminho_icone)
        
        # Mostrar informações do ícone original
        print(f"Ícone original: {caminho_icone}")
        print(f"Formato: {img.format}")
        print(f"Tamanho: {img.size}")
        print(f"Modo: {img.mode}")
        
        # Criar imagens redimensionadas
        imagens = []
        for tamanho in tamanhos:
            # Redimensionar a imagem
            img_redimensionada = img.resize((tamanho, tamanho), Image.LANCZOS)
            imagens.append(img_redimensionada)
        
        # Salvar como .ico
        imagens[0].save(
            caminho_saida,
            format='ICO',
            sizes=[(tamanho, tamanho) for tamanho in tamanhos],
            optimize=True
        )
        
        print(f"\nÍcone reduzido salvo em: {caminho_saida}")
        print(f"Tamanhos: {tamanhos}")
        
        return True
    except Exception as e:
        print(f"Erro ao reduzir o ícone: {e}")
        return False

def main():
    """Função principal."""
    # Caminho para o ícone
    caminho_icone = os.path.join('resources', 'planeta.ico')
    
    # Reduzir o ícone
    sucesso = reduzir_icone(caminho_icone)
    
    if sucesso:
        print("\nÍcone reduzido com sucesso!")
    else:
        print("\nFalha ao reduzir o ícone.")
    
    input("\nPressione Enter para sair...")

if __name__ == "__main__":
    main()
