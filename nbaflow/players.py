"""
---------------------------------------------------
----------------- MÓDULO: gamelog -----------------
---------------------------------------------------
Neste módulo, serão alocadas classes e funções com
viés de extração de detalhes de partidas de jogado-
res da NBA. Como principal fonte, a biblioteca
nba_api será consumida de modo a consultar informa-
ções contidas em seu módulo nba_api.stats.endpoints.

Table of Contents
---------------------------------------------------
1. Configurações Iniciais
    1.1 Importando bibliotecas
    1.2 Configurando logs
2. Gamelog
    2.1 Classe encapsulada
---------------------------------------------------
"""

# Author: Thiago Panini
# Date: 01/07/2021


"""
---------------------------------------------------
------------ 1. CONFIGURAÇÕES INICIAIS ------------
            1.1 Importando bibliotecas
---------------------------------------------------
"""

# Endpoints nba_api
from nba_api.stats.endpoints import commonallplayers, playergamelog

# Bibliotecas python
from datetime import datetime
import requests
import pandas as pd

# Logging
import logging
from nbaflow.utils import log_config


"""
---------------------------------------------------
------------ 1. CONFIGURAÇÕES INICIAIS ------------
    1.2 Configurando logs e definindo parâmetros
---------------------------------------------------
"""

# Instanciando e configurando objeto de log
logger = logging.getLogger(__file__)
logger = log_config(logger)

# Parâmetros de requisição de imagens
IMG_STATIC_URL = 'https://cdn.nba.com/headshots/nba/latest/1040x760/<player_id>.png'


"""
---------------------------------------------------
------------ 2. FUNCIONALIDADES ÚTEIS -------------
---------------------------------------------------
"""

# Função para coleta de informações completas de jogadores
def get_players_info(timeout=30, active=True):
    """
    Função para coleta de informações gerais e completas dos
    jogadores da NBA a partir do endpoint commonallplayers
    da biblioteca nba_api. Além de fornecer informações de
    identificação dos jogadores, o endpoint proporciona
    informações sobre ano de início e fim da carreira na NBA
    e também dos times atuais de cada jogador.

    Parâmetros
    ----------
    :param timeout:
        Tempo máximo de espera da requisição.
        [type: int, default=30]

    :param active:
        Flag para aplicação de filtro de retorno de jogadores
        ativos a partir do ano atual e a informação contida
        na coluna "to_year" da base de retorno. Caso este
        flag seja configurado como True, são retornadas
        informações apenas de jogadores que atuaram até o
        presente ano.
        [type: bool, default=True]

    Retorno
    -------
    :return players_info:
        DataFrame do pandas contendo todas as informações 
        dos jogadores presentes no endpoint commonallplayers
        [type: pd.DataFrame]
    """

    # Coletando informações e tratando colunas
    players_info = commonallplayers.CommonAllPlayers(timeout=timeout).common_all_players.get_data_frame()
    players_info.columns = [col.lower().strip() for col in players_info.columns]

    # Filtrando jogadores que participaram até o ano atual
    current_year = str(datetime.now().year)
    players_info = players_info.query('to_year == @current_year')

    return players_info

# Função para extração de imagem oficial de jogador
def get_player_image(player_id, timeout=30, static_url=IMG_STATIC_URL):
    """
    """

    url = static_url.replace('<player_id>', str(player_id))
    img = requests.get(url, timeout=timeout)

    return img.content

# Função para extração de gamelog de jogador único em temporada única
def get_player_gamelog(player_id, season, season_type='Regular Season', timeout=30):
    """
    """

    # Retornando gamelog de jogador
    player_gamelog = playergamelog.PlayerGameLog(
        player_id=player_id,
        season=season,
        season_type_all_star=season_type,
        timeout=timeout
    )

    # Transformando dados em DataFrame e adicionando informações de temporada
    df_gamelog = player_gamelog.player_game_log.get_data_frame()
    df_gamelog['SEASON'] = season
    df_gamelog['SEASON_TYPE'] = season_type

    # Transformando coluna de data na base
    df_gamelog['GAME_DATE'] = pd.to_datetime(df_gamelog['GAME_DATE'])
    df_gamelog.columns = [col.lower().strip() for col in df_gamelog.columns]

    return df_gamelog


"""
---------------------------------------------------
-------- 3. CLASSE ENCAPSULADA DE JOGADORES -------
---------------------------------------------------
"""

#class PlayerFeatures:

"""
TODO
    - Analisar centralização de gamelog e extração de imagens em um único script
    - Analisar permanência de classe ou quebra em diferentes funções
    - Analisar construção de classe apenas para consolidação de múltiplas chamadas de funções (extração para jogadores ativos)
    - Verificar como garantir o processamento das requisições com erro
"""