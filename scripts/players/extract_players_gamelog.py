"""
---------------------------------------------------
-------- SCRIPTS: extract_players_gamelog ---------
---------------------------------------------------
Script responsável por extrair o histórico de partidas
de uma determinada temporada para todos os jogadores
atualmente ativos na liga. O código leva em 
consideração um parâmetro que define a temporada alvo

Table of Contents
---------------------------------------------------
1. Configurações Iniciais
    1.1 Importando bibliotecas
    1.2 Definindo parâmetros
2. Extração de histórico de partidas
    2.1 Iterando sobre jogadores ativos
    2.2 Preparando base e salvando dados
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
from requests import exceptions
from nbaflow.players import PlayerFeatures, get_players_info, get_player_gamelog

# Funcionalidades cloudgeass
from cloudgeass.aws.s3 import JimmyBuckets

# Bibliotecas python
from datetime import datetime
import os
import pandas as pd

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

# Definindo parâmetros de temporada
SEASON_OFFSET = 0
CURRENT_YEAR = datetime.now().year - SEASON_OFFSET
SEASON = str(CURRENT_YEAR - 1) + '-' + str(CURRENT_YEAR)[-2:]
SEASON_TYPES = ['Regular Season', 'Playoffs']

# Definindo parâmetros de dados resultantes
PLAYERS_INFO_COLS = ['person_id', 'display_first_last', 'team_city', 'team_name', 'team_abbreviation']
GAMELOG_COLS = ['player_id', 'player_name', 'player_team', 'player_team_abbrev',        
                'season_id', 'season', 'season_type', 'game_id', 'game_date', 'matchup',
                'wl', 'min', 'fgm', 'fga', 'fg_pct', 'fg3m', 'fg3a', 'fg3_pct', 'ftm',  
                'fta', 'ft_pct', 'oreb', 'dreb', 'reb', 'ast', 'stl', 'blk', 'tov',     
                'pf', 'pts', 'plus_minus', 'video_available']

# Definindo parâmetros de output dos resultados
OUTPUT = 'local'

# Instanciando objeto de extração de dados
player_extractor = PlayerFeatures(
    recursive_request=True,
    timeout_increase=5,
    timesleep=3
)

"""
---------------------------------------------------
------ 2. EXTRAÇÃO DE HISTÓRICO DE PARTIDAS -------
       2.1 Iterando sobre jogadores ativos
---------------------------------------------------
"""

# Iterando sobre jogadores ativos da liga
logger.debug(f'Obtendo base de jogadores ativos da liga')
players_info = player_extractor.get_players_info()

# Definindo variáveis adicionais
i = 1
total_players = len(players_info)
players_gamelog = pd.DataFrame()

logger.debug(f'Extraindo histórico dos {total_players} jogadores na temporada {SEASON}')
for idx, row in players_info.iterrows():
    for season_type in SEASON_TYPES:
        season_gamelog = player_extractor.get_player_gamelog(
            player_id=row['person_id'],
            season=SEASON,
            season_type=season_type
        )
        # Unindo dados
        players_gamelog = players_gamelog.append(season_gamelog)

    # Comunicando andamento
    if i % 100 == 0:
        logger.debug(f'{i}/{total_players} requisições realizadas ({round(100 * (i / total_players), 1)}% concluído)')
    i += 1


"""
---------------------------------------------------
------ 2. EXTRAÇÃO DE HISTÓRICO DE PARTIDAS -------
       2.2 Preparando base e salvando dados
---------------------------------------------------
"""

logger.debug(f'Preparando e enriquecendo base de gamelog extraída')
try:
    # Preparando atributos adicionais de base comum de jogadores
    players_info_filtered = players_info.loc[:, PLAYERS_INFO_COLS]
    players_info_filtered['player_team'] = players_info_filtered['team_city'] + ' ' + players_info_filtered['team_name']
    players_info_filtered.drop(['team_city', 'team_name'], axis=1, inplace=True)
    players_info_filtered.columns = ['player_id', 'player_name', 'player_team_abbrev', 'player_team']

    # Cruzando com gamelog
    players_gamelog = players_gamelog.merge(players_info_filtered, how='left', on='player_id')
    players_gamelog = players_gamelog.loc[:, GAMELOG_COLS]
except Exception as e:
    logger.error(f'Erro ao preparar base de gamelog extraída.\n')
    raise e

logger.debug(f'Salvando arquivo de gamelog extraído')
# Salvamento local
if OUTPUT == 'local':
    try:
        gamelog_path = os.path.join(PROJECT_PATH, f'data/players_gamelog_{SEASON}.csv')
        players_gamelog.to_csv(gamelog_path, index=False)
    except Exception as e:
        logger.error(f'Erro ao salvar arquivo de gamelog em diretório local\n')
        raise e

# Salvamento em bucket s3
elif OUTPUT == 's3':
    try:
        jbuckets = JimmyBuckets()
        jbuckets.upload_object(
            file=players_gamelog,
            bucket_name='nbaflow',
            key=f'gamelog/players_gamelog_{SEASON}.csv'
        )
    except Exception as e:
        logger.error(f'Erro ao realizar upload de gamelog em bucket s3\n')
        raise e

