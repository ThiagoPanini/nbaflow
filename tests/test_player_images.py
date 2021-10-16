"""
---------------------------------------------------
-------------- TESTS: player_images ---------------
---------------------------------------------------
Testes de funcionalidades associadas à extração de
imagens de jogadores da NBA a partir de requisições
realizadas diretamente ao site de estatísticas da
NBA.

Table of Contents
---------------------------------------------------
1. Configurações Iniciais
    1.1 Importando bibliotecas
    1.2 Definindo parâmetros
2. Testes de funcionalidades
    2.1 Imagem de um único jogador
    2.2 Imagem de todos os jogadores
---------------------------------------------------
"""

# Author: Thiago Panini
# Date: 15/10/2021

"""
---------------------------------------------------
------------ 1. CONFIGURAÇÕES INICIAIS ------------
            1.1 Importando bibliotecas
---------------------------------------------------
"""

# Funcionalidades nbaflow
from nba_api.stats.endpoints import commonallplayers
from nbaflow.images import get_players_images, get_players_info
from nbaflow.utils import log_config

# Funcionalidades nba_api
from nba_api.stats.static import players

# Bibliotecas padrão
import logging
from pandas import DataFrame



"""
---------------------------------------------------
------------ 1. CONFIGURAÇÕES INICIAIS ------------
             1.2 Definindo parâmetros
---------------------------------------------------
"""

# Instanciando e configurando objeto de log
logger = logging.getLogger(__file__)
logger = log_config(logger)



"""
---------------------------------------------------
---------- 2. TESTES DE FUNCIONALIDADES -----------
       2.1 Jogador único em temporada única
---------------------------------------------------
"""

players_info = get_players_info()
print(players_info)
print(DataFrame(players.get_active_players()))
print(commonallplayers.CommonAllPlayers().common_all_players.get_data_frame())