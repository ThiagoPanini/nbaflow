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

# Endpoints e módulo estático da nba api
from nba_api.stats.static import players
from nba_api.stats.endpoints import commonplayerinfo, playergamelog

# Bibliotecas padrão
import os
import pandas as pd
from datetime import datetime

# Logging
import logging


"""
---------------------------------------------------
------------ 1. CONFIGURAÇÕES INICIAIS ------------
               1.2 Configurando logs
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
        if not isdir(log_path):
            makedirs(log_path)

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
------------------- 2. GAMELOG -------------------
               2.1 Classe Encapsulada
---------------------------------------------------
"""

# Classe para gerenciamento e extração de histórico de partidas de jogadores da NBA
class NBAGamelog:
    """
    Classe responsável por representar um objeto de extração de
    histórico de partidas de jogadores da NBA. Em seu conjunto de
    métodos e atributos, é possível gerenciar requisições à nba-api
    dentro de um contexto de dados de partidas de jogadores específicos
    e em temporadas específicas (Regular ou Playoffs).
    
    A construção dos métodos dessa classe foi pensada de tal modo a 
    proporcionar que o usuário final realize requisições sob demanda
    de acordo com o propósito definido, seja este pautado pela análise
    pontual de partidas de um único jogador em uma única temporada, ou 
    então por um processo mais robusto para extrair todo o histórico
    de partidas disponíveis de todos os jogadores ativos da liga.
    
    Além disso, entre as funcionalidades implementadas em métodos
    mais robustos que envolvem um grande número de requisições, foram
    consideradas lógicas que permitem o reprocessamento dinâmico de 
    requisições com status de falha a partir de um incremento linear
    no timeout originalmente definido. Em outras palavras, ao executar
    métodos responsáveis pela extração de um grande número de partidas,
    em caso de eventuais falhas nas requisições, os dados são armazenados
    temporariamente em um atributo da classe para posterior reprocessamento,
    caso esta seja a configuração definida pelo usuário. Dessa forma, é 
    possível parametrizar os métodos para que seja garantida uma eficiência
    de 100% nas requisições realizadas à api da NBA.
    
    Atributos da classe
    -------------------
    :attr verbose: 
        Define a verbosidade dos logs ao longo dos métodos. Quanto maior seu
        valor, mais logs serão mostrados ao usuário e eventualmente armazenados.
        [type: int, default=1]
        
    :attr error_cols:
        Variáveis que guiam e definem as requisições realizadas com status
        de falha. Basicamente, definem quais informações dessas requisições
        serão armazenadas de modo a propor um reprocessamento futuro.
        [type: list, default=['player_id', 'player_name', 'season', 'season_type', 'timeout']]
        
    :attr error_data:
        Consiste em um objeto DataFrame responsável por alocar requisições
        realizadas com status de falha. Suas colunas são definidas pelo 
        atributo self.error_cols.
        [type: pd.DataFrame]
        
    :attr all_players:
        Base contendo informações básicas de todos os jogadores da NBA
        extraída diretamente do método estático players.get_players()
        importado do módulo nba_api.stats.static
        [type: pd.DataFrame]
        
    :attr active_pĺayers:
        Base contendo informações básicas de jogadores ativos na NBA
        extraída diretamente do método estático players.get_active_players()
        importado do módulo nba_api.stats.static
        [type: pd.DataFrame]
    """
    
    def __init__(self, verbose=1):
        self.error_cols = ['player_id', 'player_name', 'season', 'season_type', 'timeout']
        self.error_data = pd.DataFrame(columns=self.error_cols)
        self.all_players = pd.DataFrame(players.get_players())
        self.active_players = pd.DataFrame(players.get_active_players())
        self.verbose = verbose
         
    # Auxilia na estruturação de requisições com falhas para futuro armazenamento
    def structure_error_data(self, player_id, player_name, season, season_type, timeout):
        """
        Responsável por estruturar um dicionário ordenado com as informações
        básicas de uma requisição, este método pode ser utilizado para
        garantir o correto armazenamento de requisições com falhas, dado que
        recebe os parâmetros básicos da mesma como entrada e retorna
        um dicionário contendo as chaves corretas a serem armazenadas
        no DataFrame definido pelo atributo self.error_data
        
        Parâmetros
        ----------
        :param player_id:
            Id do jogador alvo da análise.
            [type: int]
            
        :param player_name:
            Nome do jogador alvo da análise.
            [type: string]
            
        :param season:
            Temporada definida na requisição executada.
            [type: string]
            
        :param season_type:
            Tipo de temporada na requisição executada. Normalmente definida 
            por "Regular Season" ou "Playoffs".
            [type: string]
            
        :param timeout:
            Tempo limite definido para a requisição executada.
            [type: int]
            
        Retorno
        -------
        :return error_dict:
            Dicionário estruturado com os valores dos parâmetros e chaves
            equivalentes as colunas da base armazenada de erros
            [type: dict]
        """
        
        return {'player_id': player_id, 
                'player_name': player_name, 
                'season': season, 
                'season_type': season_type,
                'timeout': timeout}
    
    # Armazenando requisições com status de falha
    def store_error_data(self, error_dict):
        """
        Utilizar um dicionário estruturado com dados de requisições
        com falhas para armazenar as informações no atributo
        self.error_data da classe. Normalmente, os métodos da classe
        estruturam requisições com falhas a partir da execução
        prévia do método self.structure_error_data para garantir
        a correta organização dos dados antes do empilhamento.
        
        Parâmetros
        ----------
        :param error_dict:
            Dicionário estruturado contendo os dados de requisições
            falhas a serem armazenadas no atributo self.error_data
            da classe. Para uma estruturação mais simples visando
            garantir a completude do processo, o método
            self.structure_error_data() pode ser executado previamente
            ao armazenamento.
            [type: dict]
        """
        
        # Verificando estrutura do dicionário
        if self.error_cols != list(error_dict.keys()):
            try:
                error_dict = {k: v for k, v in zip(self.error_cols, error_dict.values())}
            except Exception as e:
                logger.error(f'Dicionário de erro enviado de forma incorreta. Certifique-se de que a estrutura armazenada contenha as chaves definidas por "{self.error_cols}"')
                return
        
        # Construindo DataFrame com dados de requisição com falha
        try:
            request_error = pd.DataFrame(error_dict, index=[0])
            request_error.columns = self.error_cols

            # Armazenando erro e incrementando atributo da classe
            self.error_data = self.error_data.append(request_error)
        except Exception as e:
            logger.error(f'Erro ao armazenar requisição com falha. Exception: {e}')
            return        
        
    # Gerenciando reprocessamento de requisições com falhas
    def reprocess_error_requests(self, gamelog_data, error_strategy='infinity', 
                                 num_attempts=3, timeout_increase=10):
        """
        Executa e gerencia o reprocessamento de requisições com falhas
        a partir de dados armazenados no atributo self.error_data da
        classe. Como configurações adicionais deste método, é possível
        definir a forma como as requisições serão reprocessadas, seja
        através de um número finito de tentativas ou então em uma
        abordagem onde tentativas são feitas até que o sucesso
        seja obtido.
        
        Parâmetros
        ----------
        :param gamelog_data: 
            Dados de partidas extraídos a partir de requisições
            bem sucessidas à API da NBA.
            [type: pd.DataFrame]
            
        :param error_strategy:
            Define o tipo de estratégia a ser utilizada no reprocessamento
            das requisições com falhas.
            
            *strategy='infinity': as tentativas de reprocessamento são
            realizadas até que o sucesso completo seja obtido. Uma
            observação plausível a ser feita é que, nesse modo, a 
            execução do código pode demorar de forma incalculável.
            
            *strategy='attempts': é definido um limite de tentativas
            de reprocessamento dos dados. Nessa abordagem, evita-se que
            o codigo demande tempos elevados de execução, porém não
            há a garantia que todos os dados serão retornados para
            todos os jogadores.
            
            [type: string, default='infinity']
            
        :param num_attempts:
            Número de tentativas de reprocessamento em caso de 
            error_strategy='attempts'. Ao final de cada tentativa,
            a base de erros é atualizada e verificada. Em caso de
            sucesso, a execução é interrompida. Caso as tentativas
            se esgotem e ainda existam errors, os dados faltantes
            são desconsiderados do retorno final.
            [type: int, default=3]
            
        :param timeout_increase:
            Número inteiro utilizado para incrementar o timeout da
            requisição a cada tentativa, propondo assim uma maior
            tolerância e uma maior chance de retorno dos dados a 
            cada nova requisição.
            [type: int, default=10]
            
        Retorno
        -------
        :return gamelog_data:
            Base de dados com requisições atualizadas após as 
            tentativas de reprocessamento realizadas.
            [type: pd.DataFrame]
        """
        
        # Coletando requisições com falhas e resetando atributo da classe
        fail_requests = self.error_data.copy()
        self.error_data = pd.DataFrame(columns=self.error_cols)
        
        # Estratégia de reprocessamento: número finito de tentativas 
        if error_strategy == 'attempts':
            
            # Iterando sobre número finito de tentativas
            for i in range(num_attempts):
                
                # Comunicando usuário
                if self.verbose >= 1:
                    logger.debug(f'Tentativa número {i + 1} de reprocessamento')
                    
                # Iterando sobre requisições com falhas
                for index, data in fail_requests.iterrows():
                    # Incrementando base de dados
                    gamelog_data = gamelog_data.append(self.player_gamelog_season(player_id=data['player_id'],
                                                                                  season=data['season'],
                                                                                  season_type_all_star=data['season_type'],
                                                                                  timeout=data['timeout'] + timeout_increase))

                # Copiando nova base de erros e verificando sucesso
                if len(self.error_data) == 0:
                    return gamelog_data
                else:
                    fail_requests = self.error_data.copy()
                    self.error_data = pd.DataFrame(columns=self.error_cols)

            return gamelog_data
        
        # Estratégia de reprocessamento: laço infinito
        elif error_strategy == 'infinity':
            
            # Laço infinito de iteração até que o número de erros seja 0
            i = 0
            while True:
                
                # Comunicando usuário
                if self.verbose >= 1:
                    logger.debug(f'Tentativa número {i + 1} de reprocessamento')
                    
                # Iterando sobre requisições com falhas
                for index, data in fail_requests.iterrows():
                    # Incrementando base de dados
                    gamelog_data = gamelog_data.append(self.player_gamelog_season(player_id=data['player_id'],
                                                                                  season=data['season'],
                                                                                  season_type_all_star=data['season_type'],
                                                                                  timeout=data['timeout'] + timeout_increase))
                
                # Copiando nova base de erros e verificando sucesso
                if len(self.error_data) == 0:
                    return gamelog_data
                else:
                    fail_requests = self.error_data.copy()
                    self.error_data = pd.DataFrame(columns=self.error_cols)
                    i += 1

            return gamelog_data
        
    # Identificando jogadores utilizando o id
    def player_identification(self, player_id, player_id_key='full_name'):
        """
        Propõe uma identificação detalhada de um jogador a partir de seu id.
        Para isso, utiliza basicamente o método find_player_by_id() do
        atributo players do módulo estático nba_api.stats.static.
        
        Parâmetros
        ----------
        :param player_id:
            Id do jogador a ser identificado em detalhes.
            [type: int]
            
        :param player_id_key:
            Chave de identificação utilizada no dicionário de retorno
            do método find_players_by_id.
            [type: string, default='full_name']
            
        :return player_id:
            Nova identificação do usuário.
            [type: string]
        """
        
        try:
            players_dict = players.find_player_by_id(player_id=player_id)
            if player_id_key not in players_dict.keys():
                logger.warning(f'Chave "{player_id_key}" não disponível. Escolha entre as opções: {list(players_dict.keys())}. Retornando id de entrada.')
                return player_id
            else:
                return players_dict[player_id_key]
        except Exception as e:
            logger.error(f'Erro ao encontrar jogador {player_id}. Retornando id de entrada')
            return player_id
    
    # Gerando lista formatada de temporadas a serem consideradas nas extrações históricas
    def get_seasons_list(self, from_year, to_year):
        """
        Retorna uma lista formatada com um intervalo de temporadas
        a serem utilizadas em requisições históricas para um determinado
        jogador.
        
        Parâmetros
        ----------
        :param from_year: 
            Ano de início da lista histórica de temporadas.
            [type: int]
            
        :param to_year:
            Ano final da lista histórica de temporadas.
            [type: int]
            
        Retorno
        -------
        :return seasons_list:
            Lista configurada com cada temporada a ser utilizada 
            nas requisições no formato 'yyyy-yy'.
            Exemplo: ['2018-19', '2019-20', '2020-21']
            [type: list]
        """
        return [str(year - 1) + '-' + str(year)[-2:] for year in range(from_year, to_year + 1)]        
    
    # Retornando gamelog de um único jogador em uma única temporada (tipo específico)
    def player_gamelog_season(self, player_id, season, season_type_all_star='Regular Season', 
                              timeout=60, **kwargs):
        """
        Realiza uma requisição unitária de um único jogador, 
        em uma única temporada e considerando um único tipo de 
        temporada (regular ou playoffs). Eventualmente, este
        método poderá ser utilizado por outros métodos da
        classe para requisições dentro de laços de iteração.
        
        Em caso de falhas na requisição, as informações básicas
        são armazenadas no atributo self.error_data da classe.
        
        Parâmetros
        ----------
        :param player_id:
            Id do jogador alvo da requisição.
            [type: int]
            
        :param season:
            Temporada alvo da requisição.
            [type: int]
            
        :param season_type:
            Tipo de temporada alvo da extração.
            [type: string, default='Regular Season']
            
        :param timeout:
            Limite de tempo, em segundos, a ser considerado para
            cada requisição.
            [type: int, default=60]
            
        **kwargs
        --------
        :arg player_log_id:
            Identificador customizado do jogador para fins
            de armazenamento de logs e erros.
            [type: string, default=self.player_identification(player_id, 'full_name')]
            
        Retorno
        -------
        :return df_gamelog:
            Retorno da requisição unitária para o jogador alvo
            em um formato DataFrame.
            [type: pd.DataFrame]
        """
        
        try:
            # Retornando gamelog de um jogador específico em um tipo de temporada específica
            gamelog_season = playergamelog.PlayerGameLog(player_id=player_id,
                                                         season=season,
                                                         season_type_all_star=season_type_all_star,
                                                         timeout=timeout)

            # Coletando dados da requisição em formato DataFrame
            df_gamelog = gamelog_season.player_game_log.get_data_frame()
            df_gamelog['SEASON_TYPE'] = season_type_all_star

            # Transformando coluna de data na base
            df_gamelog['GAME_DATE'] = pd.to_datetime(df_gamelog['GAME_DATE'])

            return df_gamelog

        except Exception as e:
            # Extraindo informações detalhadas e armazenando no atributo da classe
            player_log_id = kwargs['player_log_id'] if 'player_log_id' in kwargs else self.player_identification(player_id, 'full_name')
            error_dict = self.structure_error_data(player_id, player_log_id, season, season_type_all_star, timeout)
            self.store_error_data(error_dict)
            
            # Comunicando log de acordo com o atributo verbose
            if self.verbose > 1:
                logger.error(f'Erro ao retornar dados do jogador {player_log_id} em {season_type_all_star} {season}. Exception: {e}')
            
            return None
    
    # Retornando gamelog de um único jogador em uma única temporada (Regular + Playoffs)
    def player_gamelog_season_complete(self, player_id, season, season_types=['Regular Season', 'Playoffs'],
                                       timeout=60):
        """
        Realiza múltiplas requições para extrair dados de um
        jogador considerando diferentes tipos de temporadas.
        Com esse método é possível, por exemplo, obter dados
        de partidas de um jogador, em uma temporada única,
        considerando dados de playoffs e temporada regular.
        
        Parâmetros
        ----------
        :param player_id:
            Id do jogador alvo da requisição.
            [type: int]
            
        :param season:
            Temporada alvo da requisição.
            [type: int]
            
        :param season_types:
            Tipos de temporada alvo da extração.
            [type: list, default=['Regular Season', 'Playoffs']]
            
        :param timeout:
            Limite de tempo, em segundos, a ser considerado para
            cada requisição.
            [type: int, default=60]
            
        Retorno
        -------
        :return df_season_gamelog:
            Retorno da requisição para o jogador alvo
            em um formato DataFrame.
            [type: pd.DataFrame]"""
        
        # Ajustando parâmetro de season em caso default - considera temporada atual
        if season == 'default':
            season = str(datetime.now().year - 1) + '-' + str(datetime.now().year)[-2:]
        
        # Inicializando variáveis de controle
        df_season_gamelog = pd.DataFrame()

        # Iterando sobre a lista de tipos de temporadas
        for season_type in season_types:
            df_season_gamelog = df_season_gamelog.append(self.player_gamelog_season(player_id=player_id, 
                                                                                    season=season,
                                                                                    season_type_all_star=season_type,
                                                                                    timeout=timeout))

        # Ordenando dados por data da partida e retornando DataFrame com índice ajustado
        df_season_gamelog.sort_values(by='GAME_DATE', ascending=False, inplace=True)
        
        return df_season_gamelog.reset_index(drop=True)
    
    # Retornando gamelog de um único jogador em todas as temporadas (tipo específico)
    def player_gamelog_all_seasons(self, player_id, player_log_key='full_name',
                                   season_type_all_star='Regular Season', timeout=60):
        
        """
        Realiza múltiplas requições para extrair dados de um
        jogador considerando todas as temporadas disponíveis
        para o mesmo em um único tipo de temporada.
        Com esse método é possível, por exemplo, obter dados
        de partidas de um jogador, em todo seu período de
        atividade na NBA, considerando um único tipo de temporada
        (regular ou playoffs).
        
        Parâmetros
        ----------
        :param player_id:
            Id do jogador alvo da requisição.
            [type: int]
            
        :param player_log_key:
            Chave de identificação utilizada no dicionário de retorno
            do método find_players_by_id.
            [type: string, default='full_name']
            
        :param season_type_all_star:
            Tipos de temporada alvo da extração.
            [type: string, default='Regular Season']
            
        :param timeout:
            Limite de tempo, em segundos, a ser considerado para
            cada requisição.
            [type: int, default=60]
            
        Retorno
        -------
        :return df_gamelog:
            Retorno da requisição para o jogador alvo
            em um formato DataFrame.
            [type: pd.DataFrame]"""
        
        # Criando DataFrame vazio para armazenar requisições
        df_gamelog = pd.DataFrame()
        player_log_id = self.player_identification(player_id=player_id, player_id_key=player_log_key)
        
        # Extraindo lista de temporadas e comunicando usuário
        attempts = 1
        while True:
            try:
                # Requisição para intervalo de temporadas válidas do jogador
                player_info = commonplayerinfo.CommonPlayerInfo(player_id, timeout=timeout).common_player_info.get_data_frame()
                from_year = player_info['FROM_YEAR'].values[0]
                to_year = player_info['TO_YEAR'].values[0]
                break
            except Exception as e:
                if attempts % 5 == 0:
                    logger.warning(f'{attempts} realizadas para extrair temporadas válidas de {player_log_id}')
                attempts += 1
                continue
            
        # Iterando sobre todas as temporadas do jogador
        logger.debug(f'Extraindo histórico de partidas de {player_log_id} em {season_type_all_star} entre {from_year} e {to_year}')
        for season in self.get_seasons_list(from_year, to_year):
            df_gamelog = df_gamelog.append(self.player_gamelog_season(player_id=player_id,
                                                                      season=season,
                                                                      season_type_all_star=season_type_all_star,
                                                                      timeout=timeout))
        return df_gamelog
          
    # Retornando gamelog de um único jogador em todas as temporadas (Regular + Playoffs)
    def player_gamelog_all_seasons_complete(self, player_id, season_types=['Regular Season', 'Playoffs'], 
                                            player_log_key='full_name', timeout=60, reprocess=True, **kwargs):
        
        """
        Realiza múltiplas requições para extrair dados de um
        jogador considerando todas as temporadas disponíveis
        para o mesmo em todos os tipos de temporadas.
        Com esse método é possível, por exemplo, obter dados
        de partidas de um jogador, em todo seu período de
        atividade na NBA, considerando temporada regular
        e playoffs.
        
        Parâmetros
        ----------
        :param player_id:
            Id do jogador alvo da requisição.
            [type: int]
            
        :param player_log_key:
            Chave de identificação utilizada no dicionário de retorno
            do método find_players_by_id.
            [type: string, default='full_name']
            
        :param season_type_all_star:
            Tipos de temporada alvo da extração.
            [type: string, default=['Regular Season', 'Playoffs']]
            
        :param timeout:
            Limite de tempo, em segundos, a ser considerado para
            cada requisição.
            [type: int, default=60]
            
        :param reprocess:
            Flag para guiar o reprocessamento dos dados
            gerados por requisições falhas.
            [type: bool, default=True]
            
        **kwargs
        --------
        :arg error_strategy:
            Define o tipo de estratégia a ser utilizada no reprocessamento
            das requisições com falhas.
            
            *strategy='infinity': as tentativas de reprocessamento são
            realizadas até que o sucesso completo seja obtido. Uma
            observação plausível a ser feita é que, nesse modo, a 
            execução do código pode demorar de forma incalculável.
            
            *strategy='attempts': é definido um limite de tentativas
            de reprocessamento dos dados. Nessa abordagem, evita-se que
            o codigo demande tempos elevados de execução, porém não
            há a garantia que todos os dados serão retornados para
            todos os jogadores.
            
            [type: string, default='infinity']
            
        :arg num_attempts:
            Número de tentativas de reprocessamento em caso de 
            error_strategy='attempts'. Ao final de cada tentativa,
            a base de erros é atualizada e verificada. Em caso de
            sucesso, a execução é interrompida. Caso as tentativas
            se esgotem e ainda existam errors, os dados faltantes
            são desconsiderados do retorno final.
            [type: int, default=3]
            
        :arg timeout_increase:
            Número inteiro utilizado para incrementar o timeout da
            requisição a cada tentativa, propondo assim uma maior
            tolerância e uma maior chance de retorno dos dados a 
            cada nova requisição.
            [type: int, default=10]
            
        Retorno
        -------
        :return df_all_seasons:
            Retorno da requisição para o jogador alvo
            em um formato DataFrame.
            [type: pd.DataFrame]"""
        
        # Inicializando variáveis de controle
        df_all_seasons = pd.DataFrame()
        player_log_id = self.player_identification(player_id=player_id, player_id_key=player_log_key)
        
        # Extraindo lista de temporadas e comunicando usuário
        attempts = 0
        while True:
            try:
                # Requisição para intervalo de temporadas válidas do jogador
                player_info = commonplayerinfo.CommonPlayerInfo(player_id, timeout=timeout).common_player_info.get_data_frame()
                from_year = player_info['FROM_YEAR'].values[0]
                to_year = player_info['TO_YEAR'].values[0]
                
                # Extraindo lista de temporadas disponíveis para o jogador
                player_seasons = self.get_seasons_list(from_year, to_year)
                break
            except Exception as e:
                attempts += 1
                if attempts % 5 == 0:
                    logger.warning(f'{attempts + 1} realizadas para extrair temporadas válidas de {player_log_id}')
                continue
            
        # Iterando sobre todas as temporadas Regualres e Playoffs
        logger.debug(f'Extraindo histórico de partidas de {player_log_id} entre {from_year} e {to_year}')
        for season in player_seasons:
            for season_type in season_types:
                df_all_seasons = df_all_seasons.append(self.player_gamelog_season(player_id=player_id,
                                                                                  player_log_id=player_log_id,
                                                                                  season=season,
                                                                                  season_type_all_star=season_type,
                                                                                  timeout=timeout))        
        
        # Extraindo argumentos adicionais e verificando necessidade de reprocessamento
        total_requests = len(player_seasons) * len(season_types)
        
        if reprocess and len(self.error_data) > 0:
            pct_success = str(round(100 * (total_requests - len(self.error_data)) / total_requests, 1)) + '%'
            logger.warning(f'Dados de {player_log_id} retornados com {pct_success} de sucesso. Iniciando reprocessamento')
            
            # Extração de parâmetros de reprocessamento
            error_strategy = kwargs['error_strategy'] if 'error_strategy' in kwargs else 'infinity'
            num_attempts = kwargs['num_attempts'] if 'num_attempts' in kwargs else 3
            timeout_increase = kwargs['timeout_increase'] if 'timeout_increase' in kwargs else 10
            
            # Atualizando DataFrame com novos dados após reprocessamento
            df_all_seasons = self.reprocess_error_requests(gamelog_data=df_all_seasons, 
                                                           error_strategy=error_strategy,
                                                           num_attempts=num_attempts,
                                                           timeout_increase=timeout_increase)
                
        # Ordenando dados por data da partida e retornando DataFrame com índice ajustado
        final_pct_success = str(round(100 * (total_requests - len(self.error_data)) / total_requests, 1)) + '%'
        logger.info(f'Processo finalizado para {player_log_id} com {final_pct_success} de sucesso')
        df_all_seasons.sort_values(by='GAME_DATE', ascending=False, inplace=True)
               
        return df_all_seasons.reset_index(drop=True)
    
    # Retornando gamelog de todos os jogadores ativos em todas as temporadas (Regular + Playoffs)
    def active_players_gamelog(self, season_types=['Regular Season', 'Playoffs'], 
                               player_log_key='full_name', timeout=60, reprocess=True, **kwargs):
        """
        Realiza múltiplas requisições para todos os jogadores ativos
        da liga para extrair histórico de partidas em todas as 
        respectivas temporadas válidas para cada jogador, considerando
        temporada regular e playoffs.
        
        Parâmetros
        ----------            
        :param player_log_key:
            Chave de identificação utilizada no dicionário de retorno
            do método find_players_by_id.
            [type: string, default='full_name']
            
        :param season_type_all_star:
            Tipos de temporada alvo da extração.
            [type: string, default=['Regular Season', 'Playoffs']]
            
        :param timeout:
            Limite de tempo, em segundos, a ser considerado para
            cada requisição.
            [type: int, default=60]
            
        :param reprocess:
            Flag para guiar o reprocessamento dos dados
            gerados por requisições falhas.
            [type: bool, default=True]
            
        **kwargs
        --------
        :arg error_strategy:
            Define o tipo de estratégia a ser utilizada no reprocessamento
            das requisições com falhas.
            
            *strategy='infinity': as tentativas de reprocessamento são
            realizadas até que o sucesso completo seja obtido. Uma
            observação plausível a ser feita é que, nesse modo, a 
            execução do código pode demorar de forma incalculável.
            
            *strategy='attempts': é definido um limite de tentativas
            de reprocessamento dos dados. Nessa abordagem, evita-se que
            o codigo demande tempos elevados de execução, porém não
            há a garantia que todos os dados serão retornados para
            todos os jogadores.
            
            [type: string, default='infinity']
            
        :arg num_attempts:
            Número de tentativas de reprocessamento em caso de 
            error_strategy='attempts'. Ao final de cada tentativa,
            a base de erros é atualizada e verificada. Em caso de
            sucesso, a execução é interrompida. Caso as tentativas
            se esgotem e ainda existam errors, os dados faltantes
            são desconsiderados do retorno final.
            [type: int, default=3]
            
        :arg timeout_increase:
            Número inteiro utilizado para incrementar o timeout da
            requisição a cada tentativa, propondo assim uma maior
            tolerância e uma maior chance de retorno dos dados a 
            cada nova requisição.
            [type: int, default=10]
            
        Retorno
        -------
        :return df_all_seasons:
            Retorno da requisição para o jogador alvo
            em um formato DataFrame.
            [type: pd.DataFrame]"""
        
        # Inicializando variáveis de controle
        complete_gamelog = pd.DataFrame()
        error_strategy = kwargs['error_strategy'] if 'error_strategy' in kwargs else 'infinity'
        num_attempts = kwargs['num_attempts'] if 'num_attempts' in kwargs else 3
        timeout_increase = kwargs['timeout_increase'] if 'timeout_increase' in kwargs else 10
        
        # Iterando sobre jogadores ativos
        for player_id in nba_gamelog.active_players['id'].values:
            player_log_id = self.player_identification(player_id=player_id, player_id_key=player_log_key)
            complete_gamelog = complete_gamelog.append(self.player_gamelog_all_seasons_complete(player_id=player_id,
                                                                                                season_types=season_types,
                                                                                                player_log_key=player_log_key,
                                                                                                timeout=timeout,
                                                                                                reprocess=reprocess,
                                                                                                error_strategy=error_strategy,
                                                                                                num_attempts=num_attempts,
                                                                                                timeout_increase=timeout_increase))
        return complete_gamelog
    