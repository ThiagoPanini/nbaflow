"""
---------------------------------------------------
----------------- MÓDULO: images ------------------
---------------------------------------------------
Neste módulo, serão desenvolvidos códigos responsáveis
pela requisição de imagens de jogadores ativos da
NBA através do site oficial de estatísticas.

Table of Contents
---------------------------------------------------
1. Configurações Iniciais
    1.1 Importando bibliotecas
    1.2 Configurando logs
2. Funções de requisição
---------------------------------------------------
"""

# Author: Thiago Panini
# Date: 09/07/2021


"""
---------------------------------------------------
------------ 1. CONFIGURAÇÕES INICIAIS ------------
            1.1 Importando bibliotecas
---------------------------------------------------
"""

# Módulos auxiliares da biblioteca NBA
from nba_api.stats.endpoints import commonallplayers

# Pacotes python padrão
import requests
import pandas as pd
from datetime import datetime
import logging
import os
from os import makedirs
from os.path import isdir
import shutil


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
------------ 2. FUNÇÕES DE REQUISIÇÃO -------------
---------------------------------------------------
"""

# Definindo função para coleta de informações detalhadas de jogadores alvo
def get_players_info(timeout=30, error_strategy='infinity', **kwargs):
    """
    Utiliza o endpoint commonallplayers da biblioteca nba_api para
    providenciar informações detalhadas de todos os jogadores da
    NBA (ativos e aposentados). Em seu background, essa implementação
    realiza consultas diretamente à API e, portanto, pontos de
    reprocessamentos de requisição foram adicionados para garantir
    o retorno da informação de acordo com uma estratégia de erro
    definida pelo usuário. Assim, é possível configurar a função
    para realizar tentativas infinitamente até que o dado seja
    retornado ou então por um número finito de tentativas.

    Parâmetros
    ----------
    :param timeout:
            Limite de tempo, em segundos, a ser considerado para
            cada requisição.
            [type: int, default=30]

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
        
    **kwargs
    --------
    :arg error_verbose:
        Tentaivas necessárias até que se tenha uma comunicação
        com o usuário via logger.
        [type: int, default=5]
    
    :arg num_attempts:
        Número de tentativas de reprocessamento em caso de 
        error_strategy='attempts'. Ao final de cada tentativa,
        a base de erros é atualizada e verificada. Em caso de
        sucesso, a execução é interrompida. Caso as tentativas
        se esgotem e ainda existam errors, os dados faltantes
        são desconsiderados do retorno final.
        [type: int, default=11]

    :arg timeout_increase:
        Número inteiro utilizado para incrementar o timeout da
        requisição a cada tentativa, propondo assim uma maior
        tolerância e uma maior chance de retorno dos dados a 
        cada nova requisição.
        [type: int, default=5]
    
    :arg current_year:
        Referência do ano de início da temporada atual da NBA
        para aplicação de filtro em base geral de jogadores.
        O objetivo deste parâmetro é servir como filtro de
        retorno para jogadores ativos, ou seja, jogadores
        que jogaram até a referência current_year
        [type: string, default=str(datetime.now().year - 1)]
        
    Retorno
    -------
    :return players_info:
        Base de dados com informações detalhadas de jogadores
        da NBA.
        [type: pd.DataFrame]
    """
    
    # Variáveis de controle
    i = 1
    error_verbose = kwargs['error_verbose'] if 'error_verbose' in kwargs else 5
    timeout_increase = kwargs['timeout_increase'] if 'timeout_increase' in kwargs else 5
    logger.debug(f'Extraindo base com informações detalhadas de jogadores da NBA')
    
    # Iniciando laço infinito de tentativas
    if error_strategy == 'infinity':
        while True:          
            try:
                players_info = commonallplayers.CommonAllPlayers(timeout=timeout).common_all_players.get_data_frame()             
                break
            except Exception as e:
                # Comunicando usuário sobre tentativas
                if i % error_verbose == 0:
                    logger.warning(f'{i}° timeout na requisição de informações de jogadores. Iniciando tentativa número {i+1}')
                i += 1
                
                # Incrementando timeout para próxima requisição
                timeout += timeout_increase
                continue
    
    # Iniciando laço finito de tentativas de retorno
    elif error_strategy == 'attempts':
        num_attempts = kwargs['num_attempts'] if 'num_attempts' in kwargs else 11
        success_flag = 0
        for j in range(num_attempts):
            try:
                players_info = commonallplayers.CommonAllPlayers(timeout=timeout).common_all_players.get_data_frame()
                success_flag = 1
                break
            except Exception as e:
                # Incrementando timeout para próxima requisição
                timeout += timeout_increase
                
                # Comunicando usuário sobre tentativas
                if i % error_verbose == 0:
                    logger.warning(f'{i}° timeout na requisição de informações de jogadores. Iniciando tentativa número {i+1} com timeout igual a {timeout}')
                i += 1
                
                continue
                
        if success_flag == 0:
            logger.error(f'Tentativas esgotadas sem sucesso no retorno das informações. Tente aumentar o parâmetro "num_attempts" ou mudar o parâmetro "error_strategy" para "infinity"')
            return
    
    # Argumento error_strategy incorreto
    else:
        logger.error(f'Estratégia de reprocessamento inválida. Selecione entre "infinity" ou "attempts"')
        return
    
    # Aplicando formatações e filtros na base de jogadores extraída
    current_year = kwargs['current_year'] if 'current_year' in kwargs else str(datetime.now().year - 1)
    players_info = players_info.query('TO_YEAR == @current_year and TEAM_ID > 0')
    
    # Filtrando colunas e dropando index
    players_info = players_info.loc[:, ['PERSON_ID', 'DISPLAY_FIRST_LAST', 'PLAYER_SLUG', 'TEAM_ID']]
    players_info.columns = ['player_id', 'player_name', 'player_name_code', 'team_id']
    players_info.reset_index(drop=True, inplace=True)
    
    return players_info

# Definindo função para extração e salvamento local de imagens de jogadores
def get_players_images(static_url, img_format='.png', team_id_col='team_id', player_id_col='player_id',
                       player_name_code_col='player_name_code', imgs_path='../data/images/', timeout=30, 
                       assign_template_img=True, template_img_path=os.path.join(os.getcwd(), 'template_img.png'),
                       **kwargs):
    
    """
    Realiza a extração de uma base de jogadores alvo que tiveram
    partidas registradas até a temporada atual e utiliza informações
    chave dessa base (como id do jogador e id do time) para montar
    uma string de requisição responsável por extrair imagens de
    cada um dos jogadores. Essa função executa a função
    get_players_info() para coletar a base de jogadores alvo e
    utiliza o módulo requests para requisitar e salvar o conteúdo
    das imagens originalmente disponíveis na url do site oficial
    de estatísticas da NBA.

    Parâmetros
    ----------
    :param static_url:
        Template estático de url de captura das imagens disponível
        no site oficial de estatísticas da NBA. No estado atual
        de construção dessa função, o template de url tem o formato
        "https://ak-static.cms.nba.com/wp-content/uploads/headshots/nba/team_id/2020/260x190/player_id",
        sendo de responsabilidade do código aqui encapsulado
        substituir os parâmetros "team_id" e "player_id" da url
        de requisição de modo a extrair corretamente as imagens
        requisitadas.
        
    :param img_format:
        Formato da imagem a ser salva localmente em diretório local
        do sistema operacional de uso.
        [type: string, default='.png']
        
    :param team_id_col:
        Referência de coluna contendo o id do time para substituição
        no template estático de url. Essa informação é extraída
        da base gerada pela função get_players_info().
        [type: string, default='team_id']
        
    :param player_id_col:
        Referência de coluna contendo o id do jogador para substituição
        no template estático de url. Essa informação é extraída
        da base gerada pela função get_players_info().
        [type: string, default='player_id']
        
    :param player_name_code_col:
        Referência de coluna contendo o nome tratado do jogador
        para posterior salvamento de arquivo com referência
        exclusiva ao jogador em questão. Essa informação é extraída
        da base gerada pela função get_players_info().
        [type: string, default='player_name_code']
        
    :param imgs_path:
        Referência de diretório local alvo de salvamento das imagens
        requisitadas. Como observação, é válido citar que, em caso
        de inexistência do diretório, a função irá criar um com
        a referência contida neste parâmetro.
        [type: string, default='../images/']
    
    :param timeout:
        Limite de tempo, em segundos, a ser considerado para
        cada requisição.
        [type: int, default=30]
            
    :param assign_template_img:
        Define a designação de um template padrão para o jogador
        caso sua imagem não seja encontrada no site (código de 
        retorno da requisição diferente de 200). A imagem
        template considera uma "sombra" genérica de um jogador
        contendo uma interrogação ("?") no centro. Caso este
        flag seja configurado como True, essa foto genérica
        será salva com o nome do jogador cujo código retorno
        da requisição obtido ser diferente de 200.
        [type: bool, default=True]
        
    :param template_img_path:
        Define o caminho padrão de armazenamento da imagem de
        template a ser utilizada em casos de erros na requisição.
        Ao validar o sucesso do código de retorno da requisição,
        esse parâmetro é utilizado para buscar, ler e salvar
        uma nova imagem para o jogador em questão.
        [type: string, default=os.path.join(os.getcwd(), 'template_img.png']
    
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
        
    :arg error_verbose:
        Tentaivas necessárias até que se tenha uma comunicação
        com o usuário via logger.
        [type: int, default=5]
    
    :arg num_attempts:
        Número de tentativas de reprocessamento em caso de 
        error_strategy='attempts'. Ao final de cada tentativa,
        a base de erros é atualizada e verificada. Em caso de
        sucesso, a execução é interrompida. Caso as tentativas
        se esgotem e ainda existam errors, os dados faltantes
        são desconsiderados do retorno final.
        [type: int, default=11]

    :arg timeout_increase:
        Número inteiro utilizado para incrementar o timeout da
        requisição a cada tentativa, propondo assim uma maior
        tolerância e uma maior chance de retorno dos dados a 
        cada nova requisição.
        [type: int, default=5]
    
    :arg current_year:
        Referência do ano de início da temporada atual da NBA
        para aplicação de filtro em base geral de jogadores.
        O objetivo deste parâmetro é servir como filtro de
        retorno para jogadores ativos, ou seja, jogadores
        que jogaram até a referência current_year
        [type: string, default=str(datetime.now().year - 1)]
        
    Retorno
    -------
    :return success_requests:
        Base de dados com informações detalhadas de jogadores
        cuja requisição de imagens foi obtida com sucesso.
        [type: pd.DataFrame]
        
    :return fail_requests:
        Base de dados com informações detalhadas de jogadores
        cuja requisição de imagens foi obtida com falha.
        [type: pd.DataFrame]
    """
    
    # Extraindo argumentos adicionais para retorno de base alvo de jogadores
    error_strategy = kwargs['error_strategy'] if 'error_strategy' in kwargs else 'infinity'
    error_verbose = kwargs['error_verbose'] if 'error_verbose' in kwargs else 5
    timeout_increase = kwargs['timeout_increase'] if 'timeout_increase' in kwargs else 5
    num_attempts = kwargs['num_attempts'] if 'num_attempts' in kwargs else 11
    current_year = kwargs['current_year'] if 'current_year' in kwargs else str(datetime.now().year - 1)
    
    # Coletando base de jogadores alvo
    target_players = get_players_info(timeout=timeout, error_strategy=error_strategy, error_verbose=error_verbose,
                                      timeout_increase=timeout_increase, num_attempts=num_attempts, 
                                      current_year=current_year)   
    if target_players is None:
        return None, None
    
    # Criando coluna com a url de pesquisa para cada jogador
    target_players['img_url'] = target_players.apply(lambda x: static_url.replace('team_id', str(x[team_id_col])).replace('player_id', str(x[player_id_col])) + img_format, axis=1)
    
    # Gerando referência de arquivo a ser salvo
    target_players['player_name_img'] = target_players[player_name_code_col].astype(str) + img_format
    
    # Definindo parâmetros de controle
    success, errors, i = 0, 0, 0
    fail_requests = []
    success_requests = []
    
    # Iterando sobre base de dados com informações de jogadores
    logger.debug(f'Iniciando extração de imagens para jogadores da NBA')
    for index, row in target_players.iterrows():
        
        # Requisitando imagem
        i += 1
        img = requests.get(row['img_url'], timeout=timeout)
        if img.status_code != 200:
            errors += 1
            fail_requests.append(row)
            
            # Copiando imagem template com nome do jogador
            if assign_template_img:
                shutil.copy(src=template_img_path, dst=imgs_path + row["player_name_img"])
                
            continue

        # Salvando imagem em diretório local
        try:
            with open(f'{imgs_path + row["player_name_img"]}', 'wb') as f:
                f.write(img.content)
        except FileNotFoundError as fe:
            # Diretório não existente. Criando um e salvando arquivo
            os.makedirs(imgs_path)
            with open(f'{imgs_path + row["player_name_img"]}', 'wb') as f:
                f.write(img.content)

        # Comunicando usuário
        success += 1
        success_requests.append(row)
        if i % 50 == 0:
            logger.debug(f'{i} requisições realizadas, sendo {success} com sucesso e {errors} com falhas')
    
    logger.info(f'Processo encerrado com {i} requisições, sendo {success} com sucesso e {errors} com falhas')
    return pd.DataFrame(success_requests), pd.DataFrame(fail_requests)
