"""
---------------------------------------------------
----------------- MÓDULO: images ------------------
---------------------------------------------------
Neste módulo, serão desenvolvidos códigos responsáveis
pela requisição de imagens de jogadores ativos da
NBA através do site oficial de estatísticas.

Table of Contents
---------------------------------------------------
1. Configurações Iniciais
    1.1 Importando bibliotecas
    1.2 Configurando logs
2. Funções de requisição
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

# Módulos auxiliares da biblioteca NBA
from nba_api.stats.endpoints import commonallplayers
from nba_api.stats.static import players
from nbaflow.utils import get_players_info

# Pacotes python padrão
import requests
import pandas as pd
from datetime import datetime
import os
import shutil

# Logging
import logging
from nbaflow.utils import log_config


"""
---------------------------------------------------
------------ 1. CONFIGURAÇÕES INICIAIS ------------
               1.2 Configurando logs
---------------------------------------------------
"""

# Instanciando e configurando objeto de log
logger = logging.getLogger(__file__)
logger = log_config(logger)


"""
---------------------------------------------------
------------- 2. IMAGENS DE JOGADORES -------------
               2.1 Classe encapsulada
---------------------------------------------------
"""

class NBAPlayersImage():
    """
    """

    def __init__(self, static_url='https://cdn.nba.com/headshots/nba/latest/1040x760/<player_id>.png'):
        self.static_url = static_url

    def get_player_image(self, player_id, timeout=30):
        """
        """
        url = self.static_url.replace('<player_id>', str(player_id))
        img = requests.get(url, timeout=timeout)

        return img.content

