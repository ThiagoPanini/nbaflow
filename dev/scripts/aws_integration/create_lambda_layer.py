"""
---------------------------------------------------
--------- FEATURE: create_lambda_layer.py ---------
---------------------------------------------------
Neste script, será proposta a alocação de código
responsável por consultar uma lista de dependências
do projeto (ou extrair diretamenta do ambiente
virtual de trabalho) de modo a criar um layer para
o serviço lambda na AWS.

Como principal insumo, serão utilizadas as 
funcionalidades provenientes do pacote cloudgeass,
de construção caseira.

Table of Contents
---------------------------------------------------
1. Configurações Iniciais
    1.1 Importando bibliotecas
    1.2 Definindo logs e variáveis do projeto
2. Criando layer lambda
    2.1 Coletando dependências e armazenando no s3
---------------------------------------------------
"""

# Author: Thiago Panini
# Date: 08/09/2021


"""
---------------------------------------------------
------------ 1. CONFIGURAÇÕES INICIAIS ------------
            1.1 Importando bibliotecas
---------------------------------------------------
"""

# Recursos para operações na AWS
from cloudgeass.aws.serverless import build_lambda_layer
import shutil

# Bibliotecas padrão
import os

# Logging
import logging
from nbaflow.utils.log import log_config


"""
---------------------------------------------------
------------ 1. CONFIGURAÇÕES INICIAIS ------------
     1.2 Definindo logs e variáveis do projeto
---------------------------------------------------
"""

# Configurando objeto de logger
logger = logging.getLogger(__file__)
logger = log_config(logger)

# Definindo parâmetros de diretório
LAYER_ROOT_PATH = 'aws\\lambda'
LAYER_NAME = 'nbaflow_layer'
RUNTIME_FOLDER = 'python'
TARGET_PATH = os.path.join(LAYER_ROOT_PATH, LAYER_NAME, RUNTIME_FOLDER)

# Definindo parâmetros de armazenamento no s3
LAYER_BUCKET = 'lambda-layers-paninit'
LAYER_KEY = 'nbaflow_layer/python.zip'


"""
---------------------------------------------------
------------ 2. CRIANDO LAYER LAMBDA --------------
  2.1 Coletando dependências e armazenando no s3
---------------------------------------------------
"""

# Chamando função para criação do layer
if os.path.isdir(LAYER_ROOT_PATH):
    shutil.rmtree(LAYER_ROOT_PATH)

build_lambda_layer(
    target_path=TARGET_PATH,
    bucket_name=LAYER_BUCKET,
    key=LAYER_KEY,
    packages_from='list',
    packages_list=['nba_api', 'psycopg2', 'psycopg2-binary', 'pandas', 'boto3',
                   'cloudgeass', 'jaiminho']
)

"""build_lambda_layer(
    layer_path=LAYER_PATH,
    bucket_name=LAYER_BUCKET,
    prefix=LAYER_PREFIX,
    type_get_package='li',
    requirements_path=REQUIREMENTS_FILE
)"""