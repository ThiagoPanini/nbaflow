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
from nbaflow.players import get_players_info, get_player_gamelog

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
CURRENT_YEAR = datetime.now().year
SEASON = str(CURRENT_YEAR - 1) + '-' + str(CURRENT_YEAR)[-2:]
SEASON_TYPES = ['Regular Season', 'Playoffs']

# Definindo parâmetros de dados resultantes
PLAYERS_INFO_COLS = ['person_id', 'display_first_last', 'team_city', 'team_name', 'team_abbreviation']
GAMELOG_COLS = ['player_id', 'player_name', 'player_team', 'player_team_abbrev',        
                'season_id', 'season', 'season_type', 'game_id', 'game_date', 'matchup',
                'wl', 'min', 'fgm', 'fga', 'fg_pct', 'fg3m', 'fg3a', 'fg3_pct', 'ftm',  
                'fta', 'ft_pct', 'oreb', 'dreb', 'reb', 'ast', 'stl', 'blk', 'tov',     
                'pf', 'pts', 'plus_minus', 'video_available']

TMP_COLS = ['season_id', 'player_id', 'game_id', 'game_date', 'matchup', 'wl',
            'min', 'fgm', 'fga', 'fg_pct', 'fg3m', 'fg3a', 'fg3_pct', 'ftm', 'fta',
            'ft_pct', 'oreb', 'dreb', 'reb', 'ast', 'stl', 'blk', 'tov', 'pf',
            'pts', 'plus_minus', 'video_available', 'season', 'season_type']

all_gamelog = pd.read_csv(os.path.join(PROJECT_PATH, 'data/all_players_gamelog.csv'))


"""
---------------------------------------------------
------ 2. EXTRAÇÃO DE HISTÓRICO DE PARTIDAS -------
       2.1 Iterando sobre jogadores ativos
---------------------------------------------------
"""

# Iterando sobre jogadores ativos da liga
logger.debug(f'Obtendo base de jogadores ativos da liga')
players_info = get_players_info()

# Definindo variáveis adicionais
i = 1
total_players = len(players_info)
players_gamelog = pd.DataFrame()

logger.debug(f'Iterando sobre os {total_players} jogadores ativos para cada tipo de temporada ({SEASON_TYPES})')
for idx, row in players_info.head().iterrows():
    for season_type in SEASON_TYPES:
        season_gamelog = get_player_gamelog(
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

logger.debug(f'Enriquecendo base de gamelog com dados adicionais dos jogadores')
players_info_filtered = players_info.loc[:, PLAYERS_INFO_COLS]
players_info_filtered['player_team'] = players_info_filtered['team_city'] + ' ' + players_info_filtered['team_name']
players_info_filtered.drop(['team_city', 'team_name'], axis=1, inplace=True)
players_info_filtered.columns = ['player_id', 'player_name', 'player_team_abbrev', 'player_team']

players_gamelog = players_gamelog.merge(players_info_filtered, how='left', on='player_id')
players_gamelog = players_gamelog.loc[:, GAMELOG_COLS]

print(players_gamelog.columns)
print(players_gamelog.columns == all_gamelog.columns)
#players_gamelog.to_csv('gamelog_test.csv', index=False)

"""
TODO
* Adicionar try/except em pontos estratégicos do código
* Inserir lógica de armazenamento de arquivo processado (local, db ou s3)
    - Gerar arquivo por season (prefixo: players_gamelog_2020_21.csv, players_gamelog_2021_22.csv, etc...)
* [OPCIONAL] Inserir lógica de união de arquivo histórico com processamento atual
    - Isso pode ser um processo apartado caso decida-se pelo armazenamento de arquivo por season
"""