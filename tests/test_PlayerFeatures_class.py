"""
---------------------------------------------------
-------------- TESTS: PlayerFeatures --------------
---------------------------------------------------
O módulo "players.py" centraliza a extração de 
features e funcionalidades exclusivamente voltadas
à jogadores da NBA. Este script de testes tem a
responsabilidade de validar as ferramentas disponi-
bilizadas pela classe PlayerFeatures contida no
módulo.

Table of Contents
---------------------------------------------------
1. Configurações Iniciais
    1.1 Importando bibliotecas
    1.2 Definindo parâmetros
2. Testes de funcionalidades
    2.1 Informações gerais de jogadores
    2.2 Imagem oficial de jogador
    2.3 Extração de gamelog de jogador
---------------------------------------------------
"""

# Author: Thiago Panini
# Date: 17/10/2021


"""
---------------------------------------------------
------------ 1. CONFIGURAÇÕES INICIAIS ------------
            1.1 Importando bibliotecas
---------------------------------------------------
"""

# Funcionalidades nbaflow
from nbaflow.players import PlayerFeatures

# Bibliotecas python
import sys
from pandas import DataFrame
from datetime import datetime

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

# Parâmetros de teste
PLAYER_ID = 203081
SEASON = '2020-21'
SEASON_TYPES = ['Regular Season', 'Playoffs']

# Instanciando objeto da classe
player_extractor = PlayerFeatures(
    recursive_request=True,
    max_attempts=10,
    timeout_increase=5
)


"""
---------------------------------------------------
---------- 2. TESTES DE FUNCIONALIDADES -----------
       2.1 Informações gerais de jogadores
---------------------------------------------------
"""

# Extraindo informações de jogadores
logger.debug(f'Validando método get_players_info() para jogador único')
players_info = player_extractor.get_players_info()

# Extraindo parâmetros de validação
obj_type = type(players_info)
total_cols = players_info.shape[1]
expected_cols = ['person_id', 'display_last_comma_first', 'display_first_last',
                'rosterstatus', 'from_year', 'to_year', 'playercode', 'player_slug',
                'team_id', 'team_city', 'team_name', 'team_abbreviation', 'team_code',
                'team_slug', 'games_played_flag', 'otherleague_experience_ch']

# Validando retorno
assert obj_type == DataFrame, f'O objeto de retorno da função ({obj_type}) difere do esperado (DataFrame)'
assert total_cols == 16, f'A quantidade de colunas da base ({total_cols}) difere do esperado (16)'
assert list(players_info.columns) == expected_cols, f'As colunas resultantes na base diferem da lista de colunas esperada'


"""
---------------------------------------------------
---------- 2. TESTES DE FUNCIONALIDADES -----------
       2.2 Extração de gamelog de jogador
---------------------------------------------------
"""

# Jogador único em temporada única
logger.debug(f'Validando método get_player_gamelog() para jogador único')
player_gamelog = player_extractor.get_player_gamelog(
    player_id=PLAYER_ID,
    season=SEASON,
    season_type='Regular Season'
)

# Extraindo parâmetros de validação
obj_type = type(player_gamelog)
obj_rows = player_gamelog.shape[0]
obj_cols = player_gamelog.shape[1]
expected_cols = ['season_id', 'player_id', 'game_id', 'game_date', 'matchup', 'wl',
                'min', 'fgm', 'fga', 'fg_pct', 'fg3m', 'fg3a', 'fg3_pct', 'ftm', 'fta',
                'ft_pct', 'oreb', 'dreb', 'reb', 'ast', 'stl', 'blk', 'tov', 'pf',
                'pts', 'plus_minus', 'video_available', 'season', 'season_type']

# Validando retorno
assert obj_type == DataFrame, f'O objeto de retorno da função ({obj_type}) difere do esperado (DataFrame)'
assert obj_rows == 67, f'A quantidade de linhas da base ({obj_rows}) difere do esperado (67)'
assert obj_cols == 29, f'A quantidade de colunas da base ({obj_cols}) difere do esperado (29)'
assert list(player_gamelog.columns) == expected_cols, f'As colunas resultantes na base diferem da lista de colunas esperada'


"""
---------------------------------------------------
---------- 2. TESTES DE FUNCIONALIDADES -----------
  2.3 Extração de gamelog de múltiplos jogadores
---------------------------------------------------
"""

# Definindo variáveis adicionais
i = 1
total_players = len(players_info)
multiple_players_gamelog = DataFrame()

# Múltiplos jogadores em temporada única
logger.debug(f'Validando método get_player_gamelog() para múltiplos jogadores')

for idx, row in players_info.head(15).iterrows():
    for season_type in SEASON_TYPES:
        season_gamelog = player_extractor.get_player_gamelog(
            player_id=row['person_id'],
            season=SEASON,
            season_type=season_type
        )

        # Unindo dados
        multiple_players_gamelog = multiple_players_gamelog.append(season_gamelog)

# Extraindo parâmetros de validação
obj_type = type(multiple_players_gamelog)
obj_rows = multiple_players_gamelog.shape[0]
obj_cols = multiple_players_gamelog.shape[1]
expected_cols = ['season_id', 'player_id', 'game_id', 'game_date', 'matchup', 'wl',
                'min', 'fgm', 'fga', 'fg_pct', 'fg3m', 'fg3a', 'fg3_pct', 'ftm', 'fta',
                'ft_pct', 'oreb', 'dreb', 'reb', 'ast', 'stl', 'blk', 'tov', 'pf',
                'pts', 'plus_minus', 'video_available', 'season', 'season_type']

# Validando retorno
assert obj_type == DataFrame, f'O objeto de retorno da função ({obj_type}) difere do esperado (DataFrame)'
assert obj_rows == 751, f'A quantidade de linhas da base ({obj_rows}) difere do esperado (67)'
assert obj_cols == 29, f'A quantidade de colunas da base ({obj_cols}) difere do esperado (29)'
assert list(multiple_players_gamelog.columns) == expected_cols, f'As colunas resultantes na base diferem da lista de colunas esperada'

