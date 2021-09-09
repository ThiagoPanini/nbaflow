"""
---------------------------------------------------
-------- FEATURE: update_season_gamelog.py --------
---------------------------------------------------
Neste script, serão alocadas as funcionalidades
referentes a atualização dos dados de partidas dos
jogadores ativos da NBA, propondo assim uma atualização
em uma base histórica já existente, seja esta
armazenada em um banco de dados relacional (local
ou em nuvem) ou então como um objeto em um sistema
de armazenamento (como o s3, por exemplo).

A proposta deste script gira em torno da manutenção
dos dados de forma atualizada, permitindo assim com
que sempre exista uma fonte de dados capaz de ser
utilizada pras mais variadas análises, sempre em linha
com os acontecimentos reais da NBA. Como abordagem
inicial, será proposta uma execução mensal deste
script para que novos dados de partidas possam ser
enriquecidos dentro da fonte principal de dados. A
principal premissa dessa abordagem depende também da
periodicidade de consumo da nba_api, biblioteca 
fundamental utilizada para extração dos dados direto
do site de estatísticas avançadas da NBA.

Table of Contents
---------------------------------------------------
1. Configurações Iniciais
    1.1 Importando bibliotecas
    1.2 Definindo logs e variáveis do projeto
2. Coletando dados de partidas da NBA
    2.1 Classe estruturada para operações no s3
    2.2 Funções de utilidade geral
---------------------------------------------------
"""

# Author: Thiago Panini
# Date: 07/09/2021


"""
---------------------------------------------------
------------ 1. CONFIGURAÇÕES INICIAIS ------------
            1.1 Importando bibliotecas
---------------------------------------------------
"""

# Recursos para análise de dados da NBA
from nbaflow.gamelog import NBAGamelog
from nba_api.stats.endpoints import commonallplayers

# Recursos para operações na AWS
from cloudgeass.aws.s3 import JimmyBuckets

# Bibliotecas padrão
import pandas as pd
from datetime import datetime
from io import BytesIO

# Logging
import logging
from utils.log import log_config


"""
---------------------------------------------------
------------ 1. CONFIGURAÇÕES INICIAIS ------------
     1.2 Definindo logs e variáveis do projeto
---------------------------------------------------
"""

# Configurando objeto de logger
logger = logging.getLogger(__file__)
logger = log_config(logger)

# Definindo parâmetros de filtros de temporada
TODAY = datetime.now()
SEASON_YEAR = TODAY.year - 1 if TODAY.month < 10 else TODAY.year
SEASON_YEAR_STR = str(SEASON_YEAR)
CURRENT_SEASON = str(SEASON_YEAR) + '-' + str(SEASON_YEAR + 1)[-2:]

# Variáveis de requisição e transformação dos dados
TIMEOUT = 30
PLAYERS_COLS = ['PERSON_ID', 'DISPLAY_FIRST_LAST', 'PLAYER_TEAM', 'TEAM_ABBREVIATION',
                'FROM_YEAR', 'TO_YEAR']
NEW_PLAYERS_COLS = ['player_id', 'player_name', 'player_team', 'player_team_abbrev', 
                    'from_year', 'to_year']
GAMELOG_COLS = ['player_id', 'player_name', 'player_team', 'player_team_abbrev', 'season_id', 'season', 
                'season_type', 'game_id', 'game_date', 'matchup', 'wl', 'min', 'fgm', 'fga', 'fg_pct', 
                'fg3m', 'fg3a', 'fg3_pct', 'ftm', 'fta', 'ft_pct', 'oreb', 'dreb', 'reb', 'ast', 'stl', 
                'blk', 'tov', 'pf', 'pts', 'plus_minus', 'video_available']

# Variáveis de consulta e armazenamento de dados
AWS_REGION = 'sa-east-1'
S3_BUCKET = 'nbaflow-files'
S3_DATA_KEY = 'all_players_gamelog.csv'
LOCAL = True


"""
---------------------------------------------------
------ 2. COLETANDO DADOS DE PARTIDAS DA NBA ------
      2.1 Retornando jogadores ativos da liga
---------------------------------------------------
"""

logger.debug(f'Extraindo e preparando base com jogadores ativos da liga')
i = 0
while True:
    i += 1
    try:
        # Retornando e filtrando dados apenas de jogadores ativos
        players_info = commonallplayers.CommonAllPlayers(timeout=TIMEOUT).common_all_players.get_data_frame()
        players_info = players_info.query('TO_YEAR >= @SEASON_YEAR_STR and TEAM_ID > 0')
        break
    except Exception as e:
        TIMEOUT += 5
        if i % 5 == 0:
            logger.warning(f'Falha na consulta. Iniciando {i + 1}ª tentativa com timeout ajustado para {TIMEOUT}')
        continue

try:
    # Criando coluna de time e filtrando colunas necessárias
    players_info['PLAYER_TEAM'] = players_info['TEAM_CITY'] + ' ' + players_info['TEAM_NAME']
    players_info = players_info.loc[:, PLAYERS_COLS]
    players_info.columns = NEW_PLAYERS_COLS
    players_info.reset_index(drop=True, inplace=True)
except Exception as e:
    logger.error(f'Erro ao preparar base de jogadores ativos. Exception: {e}\n')
    raise e


"""
---------------------------------------------------
------ 2. COLETANDO DADOS DE PARTIDAS DA NBA ------
      2.2 Extraindo gamelog da temporada atual
---------------------------------------------------
"""

# Preparando elementos 
nba = NBAGamelog()
df_gamelog = pd.DataFrame()

# Iniciando consulta
#players_info = players_info.query('player_name in ("Damian Lillard", "Anthony Davis")')
logger.debug(f'Extraindo dados de partidas dos {len(players_info)} jogadores ativos da NBA em {CURRENT_SEASON}')
for idx, row in players_info.iterrows():
    player_gamelog = nba.player_gamelog_season_complete(
        player_id=row['player_id'],
        season=CURRENT_SEASON,
        timeout=TIMEOUT
    )
    df_gamelog = df_gamelog.append(player_gamelog)

try:
    # Enriquecendo base com dados adicionais do jogador
    df_gamelog = df_gamelog.merge(players_info.loc[:, ['player_id', 'player_name', 'player_team', 'player_team_abbrev']], 
                            how='left', left_on='Player_ID', right_on='player_id')
    df_gamelog.drop('player_id', axis=1, inplace=True)

    # Modificando colunas da base
    df_gamelog.columns = [col.lower() for col in df_gamelog.columns]
    df_gamelog = df_gamelog.loc[:, GAMELOG_COLS]

    # Ajustando tipos primitivos
    df_gamelog.loc[:, ['min', 'pts', 'plus_minus']] = df_gamelog.loc[:, ['min', 'pts', 'plus_minus']].astype(float)

    logger.info(f'Base final de gamelog preparada com dimensões: {df_gamelog.shape}')
except Exception as e:
    logger.error(f'Erro ao preparar base final de gamelog após extração. Exception: {e}')
    raise e


"""
---------------------------------------------------
------ 2. COLETANDO DADOS DE PARTIDAS DA NBA ------
    2.3 Consultando histórico e aplicando append
---------------------------------------------------
"""

# Consultando histórico direto do s3
jbuckets = JimmyBuckets(region=AWS_REGION)
gamelog_hist = jbuckets.object_to_df(
    bucket_name=S3_BUCKET,
    key=S3_DATA_KEY
)

# Filtrando dados para evitar duplicidade
gamelog_hist = gamelog_hist[gamelog_hist['season'].apply(lambda x: int(x[:4])) < SEASON_YEAR]
updated_gamelog = df_gamelog.append(gamelog_hist)

assert len(gamelog_hist) + len(df_gamelog) == len(updated_gamelog), f'Erro de append. Registros históricos ({len(gamelog_hist)}) somados aos registros atuais ({len(df_gamelog)}) não equivalem a quantidade de registros totais ({len(updated_gamelog)})'
assert updated_gamelog.shape[1] == gamelog_hist.shape[1] or updated_gamelog.shape[1] == df_gamelog.shape[1], f'Erro de dimensões. Colunas da base final ({updated_gamelog.shape[1]}) após o append diferem da quantidade de colunas das bases extraídas ({df_gamelog.shape[1]})'

# Realizando upload de arquivo resultante no s3
with BytesIO() as buffer:
    updated_gamelog.to_csv(buffer, index=False)
    content = buffer.getvalue()

jbuckets.upload_object(
    file=content,
    bucket_name=S3_BUCKET,
    key=S3_DATA_KEY
)
