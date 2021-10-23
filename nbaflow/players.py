"""
---------------------------------------------------
----------------- MÓDULO: players -----------------
---------------------------------------------------
Funcionalidades representadas por classes e funções
responsáveis por centralizar análises e extrações 
de dados referentes a jogadores da NBA. Como 
principal fonte, a biblioteca nba_api será consumida 
de modo a consultar informações contidas em seu 
módulo nba_api.stats.endpoints.

Table of Contents
---------------------------------------------------
1. Configurações Iniciais
    1.1 Importando bibliotecas
    1.2 Configurando logs e definindo parâmetros
2. Funcionalidades Úteis
3. Classe encapsulada de jogadores
---------------------------------------------------
"""

# Author: Thiago Panini
# Date: 20/10/2021


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
from time import sleep
import requests
from requests.exceptions import ReadTimeout
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
    Coleta de informações gerais e completas dos jogadores
    da NBA a partir do endpoint commonallplayers da
    biblioteca nba_api. Além de fornecer informações de
    identificação dos jogadores, o endpoint proporciona
    informações sobre ano de início e fim da carreira na NBA
    e também dos times atuais de cada jogador.

    Parâmetros
    ----------
    :param timeout:
        Tempo máximo de espera da requisição.
        [type: int, default=30]

    :param active:
        Flag para retorno de dados apenas de jogadores
        considerados ativos na NBA. Em caso positivo,
        a coluna "to_year" é utilizada como principal
        proxy para definição de atividade de um dado
        jogador da NBA, visto que esta contém informações
        de seu último ano de atividade. A regra aplicada é:
        caso o ano atual (datetime.now().year) seja igual
        ao valor do ano contido em "to_year", trata-se
        de um jogador ativo na liga.
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
    Coleta em memória de imagem oficial de jogador da NBA
    a partir de url referente ao site oficial de estatísticas.
    Ao fornecer um id de jogador (player_id), a biblioteca
    requests é utilizada para aplicar um get na url base
    de modo a retornar o conteúdo da imagem (bytes) em
    memória.

    Parâmetros
    ----------
    :param player_id:
        Identificação do jogador alvo
        [type: int]
    
    :param timeout:
        Tempo máximo de espera da requisição.
        [type: int, default=30]

    :param static_url:
        Rota estática de busca de imagem do jogador referenciada
        no site oficial da NBA. Como parâmetro de filtragem,
        foi definido o coringa <player_id> ao final da url 
        para que, dessa forma, a informação passada em
        "player_id" possa ser substituída na url e a consulta
        correta possa ser estipulada.
        [type: str, default=*consultar variável IMG_STATIC_URL]

    Retorno
    -------
    :return img.content:
        Conteúdo da imagem retornada após a requisição
        [type: bytes]
    """

    # Definindo url de pesquisa e aplicando método GET
    url = static_url.replace('<player_id>', str(player_id))
    img = requests.get(url, timeout=timeout)

    return img.content

# Função para extração de gamelog de jogador único em temporada única
def get_player_gamelog(player_id, season, season_type='Regular Season', timeout=30):
    """
    Coleta de histórico departidas de um determinado jogador
    em uma determinada temporada, considerando ainda um
    tipo específico de temporada (pré-season, temporada regular
    ou playoffs).

    Parâmetros
    ----------
    :param player_id:
        Identificação do jogador alvo
        [type: int]

    :param season:
        Temporada alvo de análise
        [type: str, exemplo: "2020-21"]

    :param season_type:
        Tipo específico de temporada aceito pelo endpoint
        [type: str, default='Regular Season']

    :param timeout:
        Tempo máximo de espera da requisição.
        [type: int, default=30]

    Retorno
    -------
    :return df_gamelog:
        Base de dados com informações específicas e detalhadas
        sobre o histórico de partidas extraído do jogador.
        Informações sobre o conteúdo desta base de retorno
        podem ser encontradas na documentação oficial do
        endpoint playergamelog.
        [type: pd.DataFrame]
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

class PlayerFeatures:
    """
    Classe responsável por centralizar requisições e 
    obtenção de dados referentes a jogadores da NBA.
    Adicionalmente, foi implementada uma regra de 
    reprocessamento de requisições falhas por conta
    de erros de timeout, garantindo que novas tentativas
    sempre serão realizadas nesses casos e aumentando
    as chances de retorno do dado solicitado.

    A lógica de reprocessamento de requisições que
    sofreram com erros de timeout se dá a partir da
    definição do método "handle_timeout_errors()" que,
    por sua vez recebe uma função como parâmetro e 
    seus respectivos argumentos em formato de dicionário.
    Possuindo a opção de executar a determinada função
    de maneira infinita até que o dado seja retornado ou
    então por um número finito de tentativas, o método
    garante que erros de timeout não mais impactem o
    fluxo de processamento do dado em scripts externos
    que desejam esse tipo de comportamento.

    Atributos da classe
    -------------------
    :param recursive_request:
        Flag que define a lógica de reprocessamento de
        requisições com erros de timeout. Se True,
        a função alvo será executada novamente dentro de
        um laço infinito de repetição até que o dado seja
        retornado ou até que um erro diferente de timeout
        seja obtido (nesse caso, o método retorna vazio).
        Se False, o atributo "max_attempts" é utilizado
        na lógica de reprocessamento de requisições como
        o número máximo de tentativas, em um laço for de
        repetição, até que o dado solicitado seja retornado
        ou até que um erro diferente de timeout seja
        obtido. Caso o número de tentativas se esgote, 
        o método retorna vazio.
        [type: bool, default=True]

    :param max_attempts:
        Número máximo de tentativas de reprocessamento de
        funções ou requisições em caso de erros de timeout.
        Este atributo é considerado na classe somente se
        o atributo "recursive_requests" for igual a False.
        [type: bool, default=False]

    :param timeout_increase:
        Incremento de timeout a cada nova tentativa de
        requisição em caso de erros de timeout. Na prática,
        se uma função retornou erro de timeout considerando
        um tempo t, a lógica da classe garante que a
        próxima tentativa de execução da função será dada
        com um timeout t + timeout_increase.
        [type: int, default=5]

    :param timesleep:
        Tempo, em segundos, de sleep do código a cada nova
        requisição realizada durante o reprocessamento de
        funções em erros de timeout.
        [type: int, default=3]
    """

    def __init__(self, recursive_request=True, max_attempts=10, 
                 timeout_increase=5, timesleep=3):
        self.recursive_request = recursive_request
        self.max_attempts = max_attempts
        self.timeout_increase = timeout_increase
        self.timesleep = timesleep

    def handle_timeout_errors(self, function, function_args):
        """
        Gerencia o repressamento de funções que obtiveram erros
        de timeout em suas tentativas iniciais de execução. Para
        isso, este método recebe uma função pura e seus resepectivos
        argumentos em formato de dicionário que, passados com o
        coringa **, garantem que a função "function" sempre tenha
        seus devidos **function_args como parâmetros.

        Utilizando os atributos da classe self.recursive_request 
        e self.max_attempt, este método gerencia a lógica de novas
        tentativas de execução, seja esta configurada para um laço
        infinito de repetição ou então por tentativas finitas.

        Parâmetros
        ----------
        :param function:
            Função a ser executada em caso de erro de timeout.
            [type: function]

        :param function_args:
            Argumentos da função a ser executada.
            [type: dict]

        Retorno
        -------
        :return: 
            O retorno deste método é definido simplesmente pelo
            retorno da função alvo passada como argumento.
        """

        if self.recursive_request:
            # Requisitando dados em um laço infinto para tratar possíveis erros de timeout
            i = 0
            while True:
                try:
                    return function(**function_args)
                except ReadTimeout as rto:
                    logger.warning(f'Erro de timeout na requisição {function.__name__}() com os argumentos: {function_args}. Nova tentativa com +{self.timeout_increase} de timeout')
                    function_args['timeout'] += self.timeout_increase
                    sleep(self.timesleep)
                except Exception as e:
                    logger.error(f'Erro genérico na requisição {function.__name__}() com os argumentos: {function_args}. Retornando vazio. Exception: {e}')
                    return None
                
        else:
            # Requisitando dados em um número finito de tentativas
            for i in range(self.max_attempts):
                try:
                    return function(**function_args)
                except ReadTimeout as rto:
                    logger.warning(f'Erro de timeout na requisição {function.__name__}() com os argumentos: {function_args}. Iniciando tentativa {i+1}/{self.max_attempts} com +{self.timeout_increase} de timeout')
                    function_args['timeout'] += self.timeout_increase
                except Exception as e:
                    logger.error(f'Erro genérico na requisição {function.__name__}() com os argumentos: {function_args}. Retornando vazio')
                    return None
            
            logger.error('Tentativas esgotadas de requisição sem resposta obtida')
            return None

    def get_players_info(self, timeout=30, active=True):
        """
        Coleta de informações gerais e completas dos jogadores
        da NBA a partir do endpoint commonallplayers da
        biblioteca nba_api. Além de fornecer informações de
        identificação dos jogadores, o endpoint proporciona
        informações sobre ano de início e fim da carreira na NBA
        e também dos times atuais de cada jogador.

        Parâmetros
        ----------
        :param timeout:
            Tempo máximo de espera da requisição.
            [type: int, default=30]

        :param active:
            Flag para retorno de dados apenas de jogadores
            considerados ativos na NBA. Em caso positivo,
            a coluna "to_year" é utilizada como principal
            proxy para definição de atividade de um dado
            jogador da NBA, visto que esta contém informações
            de seu último ano de atividade. A regra aplicada é:
            caso o ano atual (datetime.now().year) seja igual
            ao valor do ano contido em "to_year", trata-se
            de um jogador ativo na liga.
            [type: bool, default=True]

        Retorno
        -------
        :return players_info:
            DataFrame do pandas contendo todas as informações 
            dos jogadores presentes no endpoint commonallplayers
            [type: pd.DataFrame]
        """
        function_args = {'timeout': timeout, 'active': active}
        return self.handle_timeout_errors(function=get_players_info, function_args=function_args)

    def get_player_gamelog(self, player_id, season, season_type='Regular Season', timeout=30):
        """
        Coleta de histórico departidas de um determinado jogador
        em uma determinada temporada, considerando ainda um
        tipo específico de temporada (pré-season, temporada regular
        ou playoffs).

        Parâmetros
        ----------
        :param player_id:
            Identificação do jogador alvo
            [type: int]

        :param season:
            Temporada alvo de análise
            [type: str, exemplo: "2020-21"]

        :param season_type:
            Tipo específico de temporada aceito pelo endpoint
            [type: str, default='Regular Season']

        :param timeout:
            Tempo máximo de espera da requisição.
            [type: int, default=30]

        Retorno
        -------
        :return df_gamelog:
            Base de dados com informações específicas e detalhadas
            sobre o histórico de partidas extraído do jogador.
            Informações sobre o conteúdo desta base de retorno
            podem ser encontradas na documentação oficial do
            endpoint playergamelog.
            [type: pd.DataFrame]
        """
        function_args = {'player_id': player_id, 'season': season, 'season_type': season_type, 'timeout': timeout}
        return self.handle_timeout_errors(function=get_player_gamelog, function_args=function_args)

