"""
---------------------------------------------------
--------- SCRIPTS: player_gamelog_from_db ---------
---------------------------------------------------
Neste script, é proposto o fornecimento de alguns
parâmetros de consulta por parte do usuário para
que o código realiza uma consulta em um banco de
dados local com o histórico de partidas de todos
os jogadores da NBA já armazenados previamente.

Diferente de alguns scripts contidos neste 
repositório onde a geração dos dados provém de
consultas a APIs, neste caso os dados já estão
disponbilizados em um banco de dados PostgreSQL.

Table of Contents
---------------------------------------------------
1. Configurações Iniciais
    1.1 Importando bibliotecas
2. Histórico de Partidas da NBA
    2.1 Extração completa
---------------------------------------------------
"""

# Author: Thiago Panini
# Date: 18/08/2021


"""
---------------------------------------------------
------------ 1. CONFIGURAÇÕES INICIAIS ------------
            1.1 Importando bibliotecas
---------------------------------------------------
"""

# Importando classe encapsulada
from core.database import DatabaseConnection

# Pacotes python padrão
import pandas as pd
from datetime import datetime
import os
from dotenv import find_dotenv, load_dotenv

# Logging
import logging


"""
---------------------------------------------------
------------ 1. CONFIGURAÇÕES INICIAIS ------------
               1.2 Configurando log
---------------------------------------------------
"""

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
-------- 2. ESTATÍSTICA DE JOGADOR DA NBA ---------
       2.1 Coleta de Parâmetros do usuário
---------------------------------------------------
Nesta task, o usuário fornece alguns parâmetros
essenciais para a realização da consulta no
banco de dados
"""

# Coletando jogador alvo da análise
print('-' * 57)
print(' Indicadores estatísticos de um jogador em uma temporada')
print('-' * 57)
player_name = input('\nDigite o nome do jogador: \n')

# Coletando temporada alvo da análise
current_year = datetime.now().year
season_ex = str(current_year - 1) + '-' + str(current_year)[-2:]
season = input(f'\nDigite a temporada a ser analisada (ex: {season_ex}): \n')
print()

# Validando input de temporada
if len(season) != 7:
    logger.error(f'Temporada "{season}" incorreta. Por favor, utilize o formato yyyy-yy (ex: {season_ex})')
    exit()


"""
---------------------------------------------------
-------- 2. ESTATÍSTICA DE JOGADOR DA NBA ---------
  2.2 Construindo e executando consulta no banco
---------------------------------------------------
Nesta task, será proposta a criação de uma instância
de conexão ao banco de dados, a construção da query
de consulta e a agregação dos indicadores estatíticos
retornados em um formato DataFrame.
"""

# Construindo query
query = f"""
    SELECT
        player_name,
        season,
        season_type,
        count(1) AS matches,
        sum(case when wl = 'W' then 1 else 0 end) AS wins,
        round(avg(min), 1) AS avg_mins,
        round(avg(pts), 1) AS avg_pts,
        round(100 * avg(fg_pct), 1) AS avg_fg_pct,
        round(100 * avg(fg3_pct), 1) AS avg_fg3_pct,
        round(100 * avg(ft_pct), 1) AS avg_ft_pct,
        round(avg(reb), 1) AS avg_reb,
        round(avg(ast), 1) AS avg_ast,
        round(avg(stl), 1) AS avg_stl,
        round(avg(blk), 1) AS avg_blk,
        round(avg(ast), 1) AS avg_ast
        
    FROM nba_players_gamelog
    
    WHERE player_name = '{player_name}' 
        AND season = '{season}'
        
    GROUP BY
        player_name,
        player_team,
        season,
        season_type
        
    ORDER BY
        season DESC,
        season_type DESC       
"""

# Instanciando objeto de conexão ao banco
load_dotenv(find_dotenv())
db = DatabaseConnection(host='localhost', 
                        database='nbaflow_local', 
                        user='postgres',
                        password=os.getenv('DB_PWD'))

# Definindo parâmetros de retorno e executando consulta
result_columns = ['player_name', 'season', 'season_type', 'matches', 'wins', 'avg_mins',
                  'avg_pts', 'avg_fg_pct', 'avg_fg3_pct', 'avg_ft_pct', 'avg_reb', 
                  'avg_ast', 'avg_stl', 'avg_blk', 'avg_ast']
player_stats = db.select_values(query, columns=result_columns)

# Validando resultado
if player_stats is None:
    logger.error(f'Nenhum resultado retornado para os filtros de jogador {player_name} e season {season}')
    exit()