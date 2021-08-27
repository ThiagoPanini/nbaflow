"""
---------------------------------------------------
----------- SCRIPTS: one_season_gamelog -----------
---------------------------------------------------
Script responsável por requisitar e retornar deta-
lhes de partidas de todos os jogadores ativos da
liga em uma única temporada. Por padrão, os dados
extraídos terão, como base, a última temporada
registrada a partir do ano vigente.

Table of Contents
---------------------------------------------------
1. Configurações Iniciais
    1.1 Importando bibliotecas
    1.2 Configurando log
2. Histórico de Partidas da NBA
    2.1 Extração completa
---------------------------------------------------
"""

# Author: Thiago Panini
# Date: 08/07/2021


"""
---------------------------------------------------
------------ 1. CONFIGURAÇÕES INICIAIS ------------
            1.1 Importando bibliotecas
---------------------------------------------------
"""

# Importando classe encapsulada
from nbaflow.gamelog import NBAGamelog

# Funções auxiliares da biblioteca NBA
from nba_api.stats.endpoints import commonallplayers

# Pacotes python padrão
import pandas as pd
from datetime import datetime
import os

# Logging
import logging


"""
---------------------------------------------------
------------ 1. CONFIGURAÇÕES INICIAIS ------------
    1.2 Definindo variáveis e configurando log
---------------------------------------------------
"""

# Variáveis de diretório
PROJECT_PATH = os.getcwd()
DATA_PATH = os.path.join(PROJECT_PATH, 'dev/data/backup')

# Variáveis de filtro de temporada e colunas
CURRENT_YEAR = datetime.now().year
SEASON_STR = str(CURRENT_YEAR - 1) + '-' + str(CURRENT_YEAR)[-2:]
CURRENT_YEAR = str(CURRENT_YEAR)

PLAYERS_COLS = ['PERSON_ID', 'DISPLAY_FIRST_LAST', 'PLAYER_TEAM', 'TEAM_ABBREVIATION',
                'FROM_YEAR', 'TO_YEAR']
NEW_PLAYERS_COLS = ['player_id', 'player_name', 'player_team', 'player_team_abbrev', 
                    'from_year', 'to_year']
GAMELOG_COLS = ['player_id', 'player_name', 'player_team', 'player_team_abbrev', 'season_id', 'season', 
                'season_type', 'game_id', 'game_date', 'matchup', 'wl', 'min', 'fgm', 'fga', 'fg_pct', 
                'fg3m', 'fg3a', 'fg3_pct', 'ftm', 'fta', 'ft_pct', 'oreb', 'dreb', 'reb', 'ast', 'stl', 
                'blk', 'tov', 'pf', 'pts', 'plus_minus', 'video_available']

# Variáveis de requisição
TIMEOUT = 30

# Variáveis de controle de arquivos gerado
SEASON_GAMELOG_FILE = os.path.join(DATA_PATH, SEASON_STR + '_gamelog.csv')
APPEND_HIST = True

# Definindo função para configurar objeto de log do código
def log_config(logger, level=logging.DEBUG, 
               log_format='%(levelname)s;%(asctime)s;%(filename)s;%(module)s;%(lineno)d;%(message)s',
               log_filepath=os.path.join(os.getcwd(), 'exec_log/execution_log.log'),
               flag_file_handler=False, flag_stream_handler=True, filemode='a'):
    """
    Função que recebe um objeto logging e aplica configurações básicas ao mesmo
    
    Parâmetros
    ----------
    :param logger: objeto logger criado no escopo do módulo [type: logging.getLogger()]
    :param level: level do objeto logger criado [type: level, default=logging.DEBUG]
    :param log_format: formato do log a ser armazenado [type: string]
    :param log_filepath: caminho onde o arquivo .log será armazenado 
        [type: string, default='exec_log/execution_log.log']
    :param flag_file_handler: define se será criado um arquivo de armazenamento de log
        [type: bool, default=False]
    :param flag_stream_handler: define se as mensagens de log serão mostradas na tela
        [type: bool, default=True]
    :param filemode: tipo de escrita no arquivo de log [type: string, default='a' (append)]
    
    Retorno
    -------
    :return logger: objeto logger pré-configurado
    """

    # Setting level for the logger object
    logger.setLevel(level)

    # Creating a formatter
    formatter = logging.Formatter(log_format, datefmt='%Y-%m-%d %H:%M:%S')

    # Creating handlers
    if flag_file_handler:
        log_path = '/'.join(log_filepath.split('/')[:-1])
        if not os.path.isdir(log_path):
            os.makedirs(log_path)

        # Adding file_handler
        file_handler = logging.FileHandler(log_filepath, mode=filemode, encoding='utf-8')
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    if flag_stream_handler:
        # Adding stream_handler
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)    
        logger.addHandler(stream_handler)

    return logger

# Instanciando e configurando objeto de log
logger = logging.getLogger(__file__)
logger = log_config(logger)


"""
---------------------------------------------------
--------- 2. HISTÓRICO DE PARTIDAS DA NBA ---------
       2.1 Extraindo jogadores habilitados
---------------------------------------------------
Nesta task, será proposto levantamento de dados
de jogadores que participaram de pelo menos uma
partida no ano mais recente.
"""

# Coletando dados de jogadores ativos
logger.debug(f'Extraindo jogadores ativos da liga')
i = 0
while True:
    i += 1
    try:
        # Retornando e filtrando dados apenas de jogadores ativos
        players_info = commonallplayers.CommonAllPlayers(timeout=TIMEOUT).common_all_players.get_data_frame()
        players_info = players_info.query('TO_YEAR >= @CURRENT_YEAR and TEAM_ID > 0')
        players_info['PLAYER_TEAM'] = players_info['TEAM_CITY'] + ' ' + players_info['TEAM_NAME']

        # Filtrando colunas
        players_info = players_info.loc[:, PLAYERS_COLS]
        players_info.columns = NEW_PLAYERS_COLS
        players_info.reset_index(drop=True, inplace=True)

        break
    except Exception as e:
        TIMEOUT += 5
        if i % 5 == 0:
            logger.warning(f'Iniciando {i + 1}ª tentativa com timeout ajustado para {TIMEOUT}')
        continue

# Gerando massa de testes com apenas alguns jogadores
#players_info = players_info.query('player_name in ("Damian Lillard", "Anthony Davis")')


"""
---------------------------------------------------
--------- 2. HISTÓRICO DE PARTIDAS DA NBA ---------
          2.2 Laço de requisição de dados
---------------------------------------------------
Nesta task, considerando o sucesso dos insumos para
as requisições, será proposta a iteração em um laço
de repetição para extração do histórico de partidas
de jogadores em todas as suas temporadas válidas
na NBA.
"""

# Instanciando objeto de extração de histórico e criando DataFrame vazio
nba_gamelog = NBAGamelog()
gamelog = pd.DataFrame()

# Filtro opcional de 5 jogadorespara testes rápidos
#players_info = players_info.iloc[:5, :]

# Iterando sobre base de jogadores
logger.debug(f'Iniciando requisições de partidas para os {len(players_info)} jogadores ativos da liga')
for index, row in players_info.iterrows():    
    # Iterando sobre temporadas válidas do jogador
    logger.debug(f'Extraindo histórico de partidas de {row["player_name"]} para a temporada {SEASON_STR}')
    gamelog = gamelog.append(nba_gamelog.player_gamelog_season_complete(row['player_id'], SEASON_STR, timeout=TIMEOUT))
    
# Trazendo nome do jogador pra base
gamelog = gamelog.merge(players_info.loc[:, ['player_id', 'player_name', 'player_team', 'player_team_abbrev']], 
                        how='left', left_on='Player_ID', right_on='player_id')
gamelog.drop('player_id', axis=1, inplace=True)
    

"""
---------------------------------------------------
--------- 2. HISTÓRICO DE PARTIDAS DA NBA ---------
     2.3 Preparando base e gerando indicadores
---------------------------------------------------
Nesta etapa, serão aplicados procedimentos básicos
de preparação de dados para agregar indicadores
úteis para cálculos posteriores a serem realizados
nas etapas de visualizações de dados. Ao final, 
será gerado um arquivo csv com os dados completos
de gamelog para todos os jogadores.
"""

# Modificando colunas da base
gamelog.columns = [col.lower() for col in gamelog.columns]
gamelog = gamelog.loc[:, GAMELOG_COLS]

# Ajustando tipos primitivos
gamelog.loc[:, ['min', 'pts', 'plus_minus']] = gamelog.loc[:, ['min', 'pts', 'plus_minus']].astype(float)

# Salvando base
gamelog.to_csv(SEASON_GAMELOG_FILE, index=False)
logger.info(f'Processo finalizado com sucesso. Dimensões da base final: {gamelog.shape}')
