"""
---------------------------------------------------
------------------ MÓDULO: utils ------------------
---------------------------------------------------
Módulo de funções úteis utilizadas para auxiliar o
desenvolvimento das funcionalidades alocadas nos 
demais módulos nbaflow

Table of Contents
---------------------------------------------------
1. Configurações iniciais
    1.1 Importando bibliotecas e definindo parâmetros
2. Funcionalidades úteis
    2.1 Logs
---------------------------------------------------
"""

# Author: Thiago Panini
# Date: 15/10/2021


"""
---------------------------------------------------
------------ 1. CONFIGURAÇÕES INICIAIS ------------
 1.1 Importando bibliotecas e definindo parâmetros
---------------------------------------------------
"""

# Bibliotecas python
import os
import logging
from datetime import datetime
from nba_api.stats.endpoints import commonallplayers

# Parâmetros de log
LOG_LEVEL = logging.DEBUG
LOG_FORMAT = '%(levelname)s;%(asctime)s;%(filename)s;%(module)s;%(lineno)d;%(message)s'
LOG_FILE = os.path.join(os.getcwd(), 'log/execution_log.log')
LOG_DATEFMT = '%Y-%m-%d %H:%M:%S'


"""
---------------------------------------------------
------------ 2. FUNCIONALIDADES ÚTEIS -------------
                    2.1 Logs
---------------------------------------------------
"""

# Definindo função para configurar objeto de log do código
def log_config(logger, level=LOG_LEVEL, format=LOG_FORMAT, datefmt=LOG_DATEFMT, 
               file=LOG_FILE, stream_handler=True, file_handler=False, filemode='a'):
    """
    Função auxiliar que recebe um objeto logger instanciado externamente
    e propõe configurações customizadas como, por exemplo, a adição de 
    um level padrão, formato especificado da mensagem, configuração de
    handlers de arquivo ou stream no terminal ou mesmo o tipo de 
    armazenamento dos logs.

    Parâmetros
    ----------
    :param logger:
        Objeto logger criado a partir da biblioteca nativa logging
        [type: logging.logger]

    :param level:
        Level padrão do logger a ser configurado.
        * Opções: DEBUG, INFO, WARNING, ERROR
        [type: logger.Level, default=logger.DEBUG]

    :param format:
        Formato da mensagem de log mostrada ou armazenada em arquivo
        [type: str, 
        default='%(levelname)s;%(asctime)s;%(filename)s;%(module)s;%(lineno)d;%(message)s']

    :param datefmt:
        Formato padrão de datas considerado na mensagens de log
        [type: str, default='%Y-%m-%d %H:%M:%S']

    :param file:
        Caminho do arquivo de log a ser opcionalmente armazenado
        [type: str, default=os.path.join(os.getcwd(), 'log/execution_log.log')]
    
    :param stream_handler:
        Handler para mostrar mensagens de log no terminal
        [type: bool, default=True]

    :param file_handler:
        Handler para armazenamento de log em arquivo
        [type: bool, default=False]

    :param filemode:
        Modo de armazenamento de arquivo de log
        [type: str, default='a'] (append)

    Para mais informações, consultar: https://docs.python.org/3/library/logging.html

    Return
    ------
    :return logger:
        Objeto logging devidamente configurado de acordo com os 
        parâmetros fornecidos pelo usuário
        [type: logging.logger]
    """

    # Configurando level do objeto de log
    logger.setLevel(level)

    # Definindo formatação do objeto de log
    formatter = logging.Formatter(format, datefmt=datefmt)

    # Criando e configurando stream handler
    if stream_handler:
        s_handler = logging.StreamHandler()
        s_handler.setFormatter(formatter)
        logger.addHandler(s_handler)

    # Criando e configurando file handler
    if file_handler:
        log_dir = os.path.dirname(file)
        if not os.path.isdir(log_dir):
            os.makedirs(log_dir)
        
        f_handler = logging.FileHandler(file, mode=filemode, encoding='utf-8')
        f_handler.setFormatter(formatter)
        logger.addHandler(f_handler)

    return logger


"""
---------------------------------------------------
------------ 2. FUNCIONALIDADES ÚTEIS -------------
                  2.3 Jogadores
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

    