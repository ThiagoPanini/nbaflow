"""
---------------------------------------------------
------------- SCRIPTS: players_images -------------
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

# Módulos auxiliares da biblioteca NBA
from nba_api.stats.endpoints import commonallplayers

# Pacotes python padrão
import requests
import pandas as pd
from datetime import datetime
import logging
import os
from os import makedirs
from os.path import isdir

# Definindo parâmetros de consulta e de filtros
STATIC_IMG_URL = 'https://ak-static.cms.nba.com/wp-content/uploads/headshots/nba/team_id/2020/260x190/player_id'


"""
---------------------------------------------------
--------- 2. IMAGENS DE JOGADORES DA NBA ----------
---------------------------------------------------
Nesta task, será proposta a extração de todas as
imagens disponíveis no site oficial da NBA para
os jogadores ativos da liga.
"""

# Salvando imagens de jogadores
success_requests, fail_requests = get_players_images(static_url=STATIC_IMG_URL)