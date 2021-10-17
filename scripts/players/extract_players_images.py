"""
---------------------------------------------------
--------- SCRIPTS: extract_players_images ---------
---------------------------------------------------
Script responsável por extrair e salvar todas as
imagens oficiais de jogadores ativos da NBA a
partir das funcionalidades disponíveis no módulo
players do pacote nbaflow

Table of Contents
---------------------------------------------------
1. Configurações Iniciais
    1.1 Importando bibliotecas
    1.2 Definindo parâmetros
2. Extração de imagens
    2.1 Iterando sobre jogadores ativos
---------------------------------------------------
"""

# Author: Thiago Panini
# Date: 16/10/2021


"""
---------------------------------------------------
------------ 1. CONFIGURAÇÕES INICIAIS ------------
            1.1 Importando bibliotecas
---------------------------------------------------
"""

# Funcionalidades nbaflow
from nbaflow.players import get_players_info, get_player_image

# Bibliotecas python
import os

# Logging
import logging
from nbaflow.utils import log_config


"""
---------------------------------------------------
------------ 1. CONFIGURAÇÕES INICIAIS ------------
    1.2 Configurando log e definindo parâmetros
---------------------------------------------------
"""

# Configurando log
logger = logging.getLogger(__file__)
logger = log_config(logger)

# Definindo parâmetros de diretório
PROJECT_PATH = os.getcwd()
IMGS_PATH = os.path.join(PROJECT_PATH, 'data/images/players')

# Criando diretório (caso inexistente)
if not os.path.isdir(IMGS_PATH):
    os.makedirs(IMGS_PATH)


"""
---------------------------------------------------
------------- 2. EXTRAÇÃO DE IMAGENS --------------
       2.1 Iterando sobre jogadores ativos
---------------------------------------------------
"""

# Iterando sobre jogadores ativos da liga
logger.debug(f'Obtendo base de jogadores ativos da liga')
players_info = get_players_info()

logger.debug(f'Iterando sobre os dados e iniciando as requisições')
i = 1
total_players = len(players_info)
for idx, row in players_info.iterrows():
    img = get_player_image(player_id=row['person_id'])
    
    # Salvando iamgem
    img_filename = os.path.join(IMGS_PATH, row['playercode'] + '.png')
    with open(img_filename, 'wb') as f:
        f.write(img)

    # Comunicando andamento
    if i % 100 == 0:
        logger.debug(f'{i}/{total_players} requisições realizadas ({round(100 * (i / total_players), 1)}% concluído)')
    i += 1

logger.info(f'Processo de extração de imagens finalizado')


