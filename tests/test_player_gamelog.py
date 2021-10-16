"""
---------------------------------------------------
-------------- TESTS: player_gamelog --------------
---------------------------------------------------
Testes de funcionalidades referentes a extração de
gamelog de partidas de jogadores da NBA. Os testes
contemplam os métodos da classe NBAPlayerGamelog
construída no módulo interno nbaflow.

Table of Contents
---------------------------------------------------
1. Configurações Iniciais
    1.1 Importando bibliotecas
    1.2 Definindo parâmetros
2. Testes de funcionalidades
    2.1 Jogador único em temporada única
    2.2 Jogador único em todas as temporadas
    2.3 Todos os jogadores em todas as temporadas
---------------------------------------------------
"""

# Author: Thiago Panini
# Date: 13/10/2021

"""
---------------------------------------------------
------------ 1. CONFIGURAÇÕES INICIAIS ------------
            1.1 Importando bibliotecas
---------------------------------------------------
"""

# Funcionalidades nbaflow
from nbaflow.gamelog import NBAPlayerGamelog
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

# Coletando infos de jogador para teste
player_name = 'Damian Lillard'
season = '2020-21'
try:
    player_info = players.find_players_by_full_name(player_name)[0]
    player_id = player_info['id']
    logger.info(f'Jogador alvo dos testes: {player_name} (id {player_id})')
except Exception as e:
    logger.error(f'Erro ao extrair informações de {player_name}. Exception: {e}\n')
    raise e

# Validações adicionais
column_list = ['SEASON_ID', 'Player_ID', 'Game_ID', 'GAME_DATE', 'MATCHUP', 'WL',     
       'MIN', 'FGM', 'FGA', 'FG_PCT', 'FG3M', 'FG3A', 'FG3_PCT', 'FTM', 'FTA',
       'FT_PCT', 'OREB', 'DREB', 'REB', 'AST', 'STL', 'BLK', 'TOV', 'PF',     
       'PTS', 'PLUS_MINUS', 'VIDEO_AVAILABLE', 'SEASON', 'SEASON_TYPE']

# Inicializando classe
gamelog = NBAPlayerGamelog(verbose=-1)


"""
---------------------------------------------------
---------- 2. TESTES DE FUNCIONALIDADES -----------
       2.1 Jogador único em temporada única
---------------------------------------------------
"""

# Histórico de partidas - temporada regular
logger.debug(f'Validando dados de {player_name} na temporada regular {season}')
player_reg_season = gamelog.player_gamelog_season(
    player_id=player_id,
    season=season,
    season_type_all_star='Regular Season'
)
dtype = type(player_reg_season)
rows = player_reg_season.shape[0]
cols =  player_reg_season.shape[1]
col_list = list(player_reg_season.columns)
assert dtype is DataFrame, f'Objeto de retorno {dtype} não é um DataFrame do pandas'
assert rows == 67, f'Quantidade de partidas retornadas ({rows}) difere do esperado (67)'
assert cols == 29, f'Quantidade de colunas retornadas ({cols}) difere do esperado (29)'
assert col_list == column_list, f'Colunas da base retornada diferem do esperado'

# Histórico de partidas - playoffs
logger.debug(f'Validando dados de {player_name} nos playoffs {season}')
player_playoffs = gamelog.player_gamelog_season(
    player_id=player_id,
    season=season,
    season_type_all_star='Playoffs'
)
rows = player_playoffs.shape[0]
matchup = player_playoffs['MATCHUP'].apply(lambda x: x[-3:]).drop_duplicates().values[0]
assert rows == 6, f'Quantidade de partidas retornadas ({rows}) difere do esperado (6)'
assert matchup == 'DEN', f'Adversário nos playoffs ({matchup}) difere do esperado (DEN)'

# Histórico de partidas - temporada completa
logger.debug(f'Validado dados de {player_name} na temporada completa {season}')
player_season = gamelog.player_gamelog_season_complete(
    player_id=player_id,
    season=season
)
rows = player_season.shape[0]
season_types = list(player_season['SEASON_TYPE'].drop_duplicates().values)
assert rows == 73, f'Quantidade de partidas retornadas ({rows}) difere do esperado (73)'
assert season_types == ['Playoffs', 'Regular Season'], f'Tipos de temporadas retornadas ({season_types}) diferem do esperado'


"""
---------------------------------------------------
---------- 2. TESTES DE FUNCIONALIDADES -----------
    2.2 Jogador único em todas as temporadas
---------------------------------------------------
"""

# Histórico de partidas de todas as temporadas disponíveis
player_all_seasons = gamelog.player_gamelog_all_seasons_complete(
    player_id=player_id
)
rows = player_all_seasons.shape[0]
season_types = list(player_all_seasons['SEASON_TYPE'].drop_duplicates().values)
assert rows == 743, f'Quantidade de partidas retornadas ({rows}) difere do esperado (743)'
assert season_types == ['Playoffs', 'Regular Season'], f'Tipos de temporadas retornadas ({season_types}) diferem do esperado'


"""
---------------------------------------------------
---------- 2. TESTES DE FUNCIONALIDADES -----------
   2.3 Todos os jogadores em única temporada
---------------------------------------------------
"""

# Extraindo gamelog completo de jogadores ativos da NBA
season_gamelog = DataFrame()
active_players = gamelog.active_players
i = 1
for id in active_players['id'].values:
    if i % 100 == 0:
        pct_done = int(round(100 *  (i / len(active_players)), 0))
        logger.debug(f'{i} requisições realizadas ({pct_done}% concluído)')
    
    # Enriquecendo base
    season_gamelog = season_gamelog.append(gamelog.player_gamelog_season_complete(
        player_id=id,
        season=season
    ))
    i += 1

rows = season_gamelog.shape[0]
season_result = matchup = season_gamelog['SEASON'].drop_duplicates().values[0]
assert rows == 21409, f'Quantidade de partidas retornadas ({rows}) difere do esperado (21409)'
assert season == season_result, f'A temporada extraída ({season_result}) difere da temporada esperada ({season})'

logger.info(f'Validações da classe gamelog finalizada com sucesso')