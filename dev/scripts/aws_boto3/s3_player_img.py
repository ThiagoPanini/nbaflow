"""
---------------------------------------------------
-------------- SCRIPTS: s3_player_img -------------
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
2. Coletando imagem de jogador em bucket s3
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
from dotenv.main import find_dotenv, load_dotenv
from utils.aws.s3 import JimmyBuckets

# Bibliotecas padrão
import os

# Gerenciamento de e-mails
import jaiminho.exchange as jex

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

# Variáveis de configuração AWS
REGION = 'sa-east-1'
BUCKET_NAME = 'nbaflow-files'
FOLDER_PREFIX = 'images/players/'

# Variáveis de credenciais de e-mail
load_dotenv(find_dotenv())
MAIL_FROM = os.getenv('MAIL_FROM')
MAIL_SERVER = 'outlook.office365.com'
MAIL_BOX = os.getenv('MAIL_BOX')
MAIL_SUBJECT = '[NBAFlow] Imagem de <player_name> direto de bucket s3'

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
print('Recebendo imagens de jogadores da NBA por e-mail')
print('-' * 62)


"""
---------------------------------------------------
--- 2. COLETANDO IMAGEM DE JOGADOR EM BUCKET S3 ---
        2.1 Coletando informações do usuário
---------------------------------------------------
"""

# Coletando nome do jogador alvo
player_name = input('\nDigite o nome do jogador: \n').strip()

# Insira o destinatário
mail_to = input(f'\nInsira o destinatário de e-mail: \n')
print()


"""
---------------------------------------------------
--- 2. COLETANDO IMAGEM DE JOGADOR EM BUCKET S3 ---
          2.2 Coletando imagem no bucket
---------------------------------------------------
"""

# Instanciando classe JimmyBuckets
jbuckets = JimmyBuckets(region=REGION)

# Montando chave de pesquisa e coletando imagem em bytes
player_key = FOLDER_PREFIX + player_name + '.png'
player_img = jbuckets.read_object(bucket_name=BUCKET_NAME, key=player_key)
filename = player_name + '.png'

# Enviando e-mail
try:
    jex.send_mail(
        username=MAIL_FROM,
        password=os.getenv('MAIL_PWD'),
        server=MAIL_SERVER,
        mail_box=MAIL_BOX,
        mail_to=[mail_to],
        subject=f'Imagem de {player_name} coletada de bucket s3',
        body=f'<img src="cid:{filename}">',
        zip_attachments=zip([filename], [player_img])
    )
    logger.info(f'E-mail com imagem do jogador {player_name} enviado com uscesso por e-mail')
except Exception as e:
    logger.error(f'Erro ao enviar imagem por e-mail. Exception: {e}')
    exit()