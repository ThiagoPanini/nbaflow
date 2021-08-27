"""
---------------------------------------------------
---------- SCRIPTS: insert_gamelog_data -----------
---------------------------------------------------
O objetivo deste script é propor uma forma rápida e
direta de realizar a ingestão de dados já processados
de partidas de jogadores da NBA em uma tabela de
um banco de dados existente em um servidor.

Os dados estão previamente disponíveis em um arquivo
csv e, como premissa adicional, deve-se garantir a
existência de um servidor PostgreSQL disponível para
receber as demandas de SQL. Basicamente, os comandos
a serem executados giram em torno da criação de uma
tabela com base no layout do arquivo csv e, 
posteriormente, a ingestão dos dados lidos nesta 
tabela.

Table of Contents
---------------------------------------------------
1. Configurações Iniciais
    1.1 Importando bibliotecas
    1.2 Configurando log e definindo variáveis
2. Realizando ingestão de dados
    2.1 Lendo arquivo csv do repositório
    2.2 Conectando ao banco e inserindo dados
---------------------------------------------------
"""

# Author: Thiago Panini
# Date: 19/08/2021


"""
---------------------------------------------------
------------ 1. CONFIGURAÇÕES INICIAIS ------------
            1.1 Importando bibliotecas
---------------------------------------------------
"""

# Importando classe encapsulada
from nbaflow.database import DatabaseConnection

# Pacotes python padrão
import pandas as pd
import os
from dotenv import find_dotenv, load_dotenv

# Logging
import logging


"""
---------------------------------------------------
------------ 1. CONFIGURAÇÕES INICIAIS ------------
    1.2 Configurando log e definindo variáveis
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

# Definindo variáveis de diretório
PROJECT_PATH = os.getcwd()
DATA_PATH = os.path.join(PROJECT_PATH, 'dev/data')
FILENAME = 'all_players_gamelog.csv'
DB_TABLE = 'nba_players_gamelog'


"""
---------------------------------------------------
-------- 2. REALIZANDO INGESTÃO DE DADOS ----------
       2.1 Lendo arquivo csv do repositório
---------------------------------------------------
Leitura de arquivo csv disponível localmente a 
partir de processamentos já realizados previamente
"""

# Banner
banner = """
███╗   ██╗██████╗  █████╗ ███████╗██╗      ██████╗ ██╗    ██╗
████╗  ██║██╔══██╗██╔══██╗██╔════╝██║     ██╔═══██╗██║    ██║
██╔██╗ ██║██████╔╝███████║█████╗  ██║     ██║   ██║██║ █╗ ██║
██║╚██╗██║██╔══██╗██╔══██║██╔══╝  ██║     ██║   ██║██║███╗██║
██║ ╚████║██████╔╝██║  ██║██║     ███████╗╚██████╔╝╚███╔███╔╝
╚═╝  ╚═══╝╚═════╝ ╚═╝  ╚═╝╚═╝     ╚══════╝ ╚═════╝  ╚══╝╚══╝ 
"""
# Banner gerado pelo site: https://patorjk.com/software/taag/#p=display&f=ANSI%20Shadow&t=NBAflow

# Iniciando programa
print('-' * 62)
print(banner)
print('-' * 62)
print('   Ingestão de histórico pré-processado de partidas da NBA')
print('-' * 62)

# Lendo arquivo
try:
    df = pd.read_csv(os.path.join(DATA_PATH, FILENAME))
    logger.info(f'Arquivo de histórico de partidas da NBA lido com sucesso. Dimensões: {df.shape}')
except Exception as e:
    logger.error(f'Erro ao ler arquivo {FILENAME}. Exception: {e}')
    exit()


"""
---------------------------------------------------
-------- 2. REALIZANDO INGESTÃO DE DADOS ----------
    2.2 Conectando ao banco e inserindo dados
---------------------------------------------------
Instanciando objeto de conexão ao banco de dados,
criando tabela a partir de DataFrame lido e 
construindo query de ingestão dos dados disponíveis
"""

# Instância de conexão ao banco de dados
load_dotenv(find_dotenv())
db = DatabaseConnection(host=os.getenv('DB_HOST'), 
                        database=os.getenv('DB_NAME'), 
                        user=os.getenv('DB_USER'),
                        password=os.getenv('DB_PWD'))

# Dropando tabela, caso existentes
db.execute_query(query=f'DROP TABLE IF EXISTS {DB_TABLE}')

# Criando tabela a partir do DataFrame lido e aplicando ingestão
db.create_table_from_df(df=df, table=DB_TABLE)
db.insert_execute_values(df=df, table=DB_TABLE)

# Validando ingestão a partir de contagem de registros
logger.debug(f'Validando registros inseridos a partir da contagem de linhas da tabela')
query = f'SELECT count(1) FROM {DB_TABLE}'
table_rows = db.select_values(query).values[0]
if table_rows == len(df):
    logger.info(f'Ingestão realizada com sucesso. A tabela possui {table_rows} linhas e o arquivo possui {len(df)}. Programa encerrado')
else:
    logger.warning(f'Quantidade de linhas na tabela ({table_rows}) difere da quantidade de linhas do DataFrame ({len(df)})')
exit()

