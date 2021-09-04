"""
---------------------------------------------------
--------------- SCRIPTS: s3_manager ---------------
---------------------------------------------------
Script desenvolvido para testar e executar as 
funcionalidades criadas e alocadas em módulos
especiais de gerenciamento de operações relacionadas
ao manuseio de elementos no s3 utilizando o SDK
Python boto3 como ferramenta de intermédio.

Neste script, será possível encontrar algumas das
principais funcionalidades da classe "JimmyButler", 
sendo esta construída com o propósito de encapsular
algumas das operações mais comuns envolvendo o
Serviço de Armazenamento Simples da AWS.

Table of Contents
---------------------------------------------------
1. Configurações iniciais
    1.1 Importando bibliotecas
    1.2 Configurando logs
    1.3 Definindo variáveis do projeto
2. Gerenciando buckets e objetos
    2.1 Criando e configurando bucket
    2.2 Realizando upload de objetos
    2.3 Realizando o download de objetos
---------------------------------------------------
"""

# Author: Thiago Panini
# Date: 27/08/2021


"""
---------------------------------------------------
------------ 1. CONFIGURAÇÕES INICIAIS ------------
            1.1 Importando bibliotecas
---------------------------------------------------
"""

# Códigos úteis AWS
from cloudgeass.aws.s3 import JimmyBuckets

# Bibliotecas padrão
import os

# Logging
import logging
from utils.log import log_config


"""
---------------------------------------------------
------------ 1. CONFIGURAÇÕES INICIAIS ------------
               1.2 Configurando log
---------------------------------------------------
"""

# Instanciando e configurando objeto de log
logger = logging.getLogger(__file__)
logger = log_config(logger)


"""
---------------------------------------------------
------------ 1. CONFIGURAÇÕES INICIAIS ------------
        1.3 Definindo variáveis do projeto
---------------------------------------------------
"""

# Variáveis de diretório
PROJECT_PATH = os.getcwd()
DATA_PATH = os.path.join(PROJECT_PATH, 'dev/data')
IMGS_PATH = os.path.join(DATA_PATH, 'images/players')
CSV_FILENAME = 'all_players_gamelog.csv'

# Variáveis de configuração AWS
REGION = 'sa-east-1'
BUCKET_NAME = 'nbaflow-files'
DROP_EXISTENT = True
DATA_FOLDER = 'data/'
IMGS_FOLDER = 'imgs/'
LOCAL_DIR_BUCKET_DOWNLOAD = os.path.join(PROJECT_PATH, 'tmp')


"""
---------------------------------------------------
-------- 2. GERENCIANDO BUCKETS E OBJETOS ---------
        2.1 Criando e configurando bucket
---------------------------------------------------
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
print('Gerenciamento de buckets s3 e ingestão de objetos via boto3')
print('-' * 62)

logger.debug(f'Instanciando classe JimmyBuckets e configurando ambiente s3')
jbuckets = JimmyBuckets(region=REGION)

# Deletando (se aplicável) e criando novo bucket
if DROP_EXISTENT:
    jbuckets.delete_bucket(bucket_name=BUCKET_NAME, empty_bucket=True)
jbuckets.create_bucket(bucket_name=BUCKET_NAME)


"""
---------------------------------------------------
-------- 2. GERENCIANDO BUCKETS E OBJETOS ---------
        2.2 Realizando o upload de objetos
---------------------------------------------------
"""

# Realizando o upload de todos os arquivos em um diretório raíz
jbuckets.upload_directory(
    directory=DATA_PATH,
    bucket_name=BUCKET_NAME
)



