"""
---------------------------------------------------
----------- SCRIPTS: all_players_images -----------
---------------------------------------------------
Script responsável por realizar múltiplas requisições
no site oficial de estatísticas da NBA para extração
de imagens de jogadores ativos da liga. Ao final do
processamento, os arquivos em formato png serão
salvos em diretório definido pelo usuário no
sistema operacional de uso.

Table of Contents
---------------------------------------------------
1. Configurações Iniciais
    1.1 Importando bibliotecas
    1.2 Definindo variáveis e configurando log
2. Imagens de jogadores
    2.1 Extração completa
---------------------------------------------------
"""

# Author: Thiago Panini
# Date: 09/07/2021


"""
---------------------------------------------------
------------ 1. CONFIGURAÇÕES INICIAIS ------------
            1.1 Importando bibliotecas
---------------------------------------------------
"""

# Funções para extração de imagens de jogadores
from core.images import get_players_images
import os
import pandas as pd

# Definindo parâmetros de consulta e de filtros
STATIC_IMG_URL = 'https://ak-static.cms.nba.com/wp-content/uploads/headshots/nba/team_id/2020/260x190/player_id'
PLAYER_REF = 'player_name'
PROJECT_PATH = os.getcwd()
TEMPLATE_IMG_PATH = os.path.join(PROJECT_PATH, 'data/unknown_player_template.png')
GAMELOG_PATH = os.path.join(PROJECT_PATH, 'data/all_players_gamelog.csv')
IMGS_PATH = os.path.join(PROJECT_PATH, 'data/images/')


"""
---------------------------------------------------
--------- 2. IMAGENS DE JOGADORES DA NBA ----------
---------------------------------------------------
Nesta task, será proposta a extração de todas as
imagens disponíveis no site oficial da NBA para
os jogadores ativos da liga.
"""

# Salvando imagens de jogadores
success_requests, fail_requests = get_players_images(static_url=STATIC_IMG_URL, 
                                                     imgs_path=IMGS_PATH,
                                                     player_name_code_col=PLAYER_REF,
                                                     template_img_path=TEMPLATE_IMG_PATH)

# Deletando imagens baixadas de jogadores não presentes na base
gamelog = pd.read_csv(GAMELOG_PATH)
players = sorted(gamelog[PLAYER_REF].unique())
players_imgs = os.listdir(IMGS_PATH)

print(f'Jogadores únicos na base de gamelog: {len(players)}')
print(f'Imagens totais baixadas: {len(players_imgs)}')

# Iterando sobre as imagens baixadas
for img in players_imgs:
    img_split = img[:-4]
    if img_split not in players:
        # Removendo imagem caso jogador inexistente na base
        os.remove(os.path.join(IMGS_PATH, img))
        
# Verificando números finais
print(f'Total de imagens após a remoção: {len(os.listdir(IMGS_PATH))}')