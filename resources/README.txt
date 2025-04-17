# Recursos do Aplicativo Gerador de Vértices

## Captura de Tela do Aplicativo

Para adicionar uma captura de tela do aplicativo ao README.md, siga estas etapas:

1. Execute o aplicativo usando o comando:
   ```
   python app_main.py --gui
   ```

2. Quando a interface estiver aberta, faça uma captura de tela da janela do aplicativo.
   - No Windows: Pressione Alt+Print Screen para capturar apenas a janela ativa
   - No macOS: Pressione Command+Shift+4, depois espaço, e clique na janela
   - No Linux: Use a ferramenta de captura de tela do seu ambiente de desktop

3. Salve a imagem como "app_screenshot.png" neste diretório (resources/)

4. A imagem será automaticamente exibida no README.md através do link:
   ```
   ![Interface do Aplicativo](resources/app_screenshot.png)
   ```

## Ícone do Aplicativo

O ícone do aplicativo será gerado automaticamente pelo script build_app.py quando você criar o instalador. O script irá:

1. Criar um ícone simples com um círculo branco em fundo azul
2. Salvar o ícone como "app_icon.ico" para Windows e "app_icon.png" para outras plataformas
3. Usar o ícone no executável e no instalador

Se você quiser usar seu próprio ícone, substitua os arquivos gerados pelos seus próprios arquivos de ícone com os mesmos nomes.
