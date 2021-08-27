"""
---------------------------------------------------
--------- SCRIPTS: upload_objects ---------
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
1. Configurações iniciais
    1.1 Importando bibliotecas
    1.2 Configurando logs
    1.3 Definindo variáveis do projeto
2. Gerenciando buckets e objetos
    2.1 Criando e configurando bucket
    2.2 Realizando upload de objetos
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
import boto3
from botocore.exceptions import ClientError
from botocore.retries import bucket
from utils.aws.s3 import JimmyBuckets, create_bucket, delete_bucket, upload_object, upload_files_in_dir

# Bibliotecas padrão
import os

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


"""
---------------------------------------------------
-------- 2. GERENCIANDO BUCKETS E OBJETOS ---------
        2.1 Criando e configurando bucket
---------------------------------------------------
"""

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

# Realizando o upload de arquivo de texto
jbuckets.upload_object(
    file=os.path.join(DATA_PATH, CSV_FILENAME),
    bucket_name=BUCKET_NAME,
    key=DATA_FOLDER + CSV_FILENAME
)

# Realizando o upload individual de imagens
logger.debug(f'Iniciando o upload das imagens presentes no diretório do projeto')
for img in os.listdir(IMGS_PATH):
    jbuckets.upload_object(
        file=os.path.join(IMGS_PATH, img),
        bucket_name=BUCKET_NAME,
        key=IMGS_FOLDER + img,
        verbose=False
    )
logger.info(f'Upload de {len(os.listdir(IMGS_PATH))} imagens realizado com sucesso')

# Realizando o upload de todos os arquivos em um diretório raíz
jbuckets.s3_resource.Bucket(BUCKET_NAME).objects.all().delete()
jbuckets.upload_files_in_dir(
    directory=DATA_PATH,
    bucket_name=BUCKET_NAME
)

