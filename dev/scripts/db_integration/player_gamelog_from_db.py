"""
---------------------------------------------------
--------- SCRIPTS: player_gamelog_from_db ---------
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
1. Configurações Iniciais
    1.1 Importando bibliotecas
2. Estatística de jogador da NBA
    2.1 Coleta de Parâmetros do Usuário
    2.2 Construindo e executando consulta no banco
    2.3 Comunicando resultado via e-mail
---------------------------------------------------
"""

# Author: Thiago Panini
# Date: 18/08/2021


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
from datetime import datetime
import os
from dotenv import find_dotenv, load_dotenv

# Biblioteca customizada para envio de e-mails
from xchange_mail.mail import send_simple_mail

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
-------- 2. ESTATÍSTICA DE JOGADOR DA NBA ---------
       2.1 Coleta de Parâmetros do Usuário
---------------------------------------------------
Preparação de variáveis fornecidas pelo usuário para
construção da consulta ao banco de dados considerando
os filtros estabelecidos de jogador e temporada.
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
print('   Indicadores estatísticos de um jogador em uma temporada')
print('-' * 62)

# Coletando jogador alvo da análise
player_name = input('\nDigite o nome do jogador: \n').strip()
#player_name = 'Damian Lillard'

# Coletando temporada alvo da análise
current_year = datetime.now().year
season_ex = str(current_year - 1) + '-' + str(current_year)[-2:]
season = input(f'\nDigite a temporada a ser analisada (ex: {season_ex}): \n')
#season = '2019-20'
print()

# Validando input de temporada
if len(season) != 7:
    logger.error(f'Temporada "{season}" incorreta. Por favor, utilize o formato yyyy-yy (ex: {season_ex})')
    exit()


"""
---------------------------------------------------
-------- 2. ESTATÍSTICA DE JOGADOR DA NBA ---------
  2.2 Construindo e executando consulta no banco
---------------------------------------------------
Criação de string de consulta a ser utilizada no 
retorno dos dados solicitados, instância de objeto
de conexão ao banco de dados e execução da consulta
para retorno de indicadores estatísticos de um jogador
em uma temporada específica em formato DataFrame.
"""

# Construindo query
query = f"""
    SELECT
        player_name,
        season,
        season_type,
        count(1) AS matches,
        sum(case when wl = 'W' then 1 else 0 end) AS wins,
        round(avg(min), 1) AS avg_mins,
        round(avg(pts), 1) AS avg_pts,
        round(100 * avg(fg_pct), 1) AS avg_fg_pct,
        round(100 * avg(fg3_pct), 1) AS avg_fg3_pct,
        round(100 * avg(ft_pct), 1) AS avg_ft_pct,
        round(avg(reb), 1) AS avg_reb,
        round(avg(ast), 1) AS avg_ast,
        round(avg(stl), 1) AS avg_stl,
        round(avg(blk), 1) AS avg_blk,
        round(avg(ast), 1) AS avg_ast
        
    FROM nba_players_gamelog
    
    WHERE player_name = '{player_name}' 
        AND season = '{season}'
        
    GROUP BY
        player_name,
        player_team,
        season,
        season_type
        
    ORDER BY
        season DESC,
        season_type DESC       
"""

# Instanciando objeto de conexão ao banco
load_dotenv(find_dotenv())
db = DatabaseConnection(host=os.getenv('DB_HOST'), 
                        database=os.getenv('DB_NAME'), 
                        user=os.getenv('DB_USER'),
                        password=os.getenv('DB_PWD'))

# Definindo parâmetros de retorno e executando consulta
result_columns = ['player_name', 'season', 'season_type', 'matches', 'wins', 'avg_mins',
                  'avg_pts', 'avg_fg_pct', 'avg_fg3_pct', 'avg_ft_pct', 'avg_reb', 
                  'avg_ast', 'avg_stl', 'avg_blk', 'avg_ast']
player_stats = db.select_values(query, columns=result_columns)

# Validando resultado
if player_stats is None:
    logger.error(f'Nenhum resultado retornado para os filtros de jogador {player_name} e season {season}')
    exit()


"""
---------------------------------------------------
-------- 2. ESTATÍSTICA DE JOGADOR DA NBA ---------
       2.3 Comunicando resultado via e-mail
---------------------------------------------------

"""

# Verificando se usuário deseja receber o resultado por email
flag_mail = int(input(f'\nDeseja receber os dados de {player_name} na season {season} por e-mail?\n[1] Sim\n[2] Não\n'))
if flag_mail != 1:
    print(f'\n{player_stats}\n')
    logger.info('Programa encerrado')
    exit()
else:
    # Coletando e validando e-mail de destino (forma básica)
    mail_to = input(f'\nInsira o e-mail de destino (em caso de mais de um, separar por ";"):\n')
    while True:
        if ';' in mail_to:
            mail_to_errors = [mail for mail in mail_to.split(';') if mail.count('@') != 1 or '.com' not in mail]
            if len(mail_to_errors) > 0:
                mail_to = input(f'\nUm ou mais e-mails fornecidos foram caracterizados como inválidos ({mail_to_errors}). Por favor, tente novamente:\n')
            else:
                break           
        elif mail_to.count('@') != 1 or '.com' not in mail_to:
            mail_to = input(f'\nE-mail {mail_to} inválido. Por favor, tente novamente: \n')
        else:
            break

    # Extraindo valores de envio do owner a partir de variáveis de ambiente
    logger.debug('Coletando parâmetros e enviando e-mail com as estatísticas extraídas')
    MAIL_FROM = os.getenv('MAIL_FROM')
    MAIL_PWD = os.getenv('MAIL_PWD')
    MAIL_SERVER = 'outlook.office365.com'
    MAIL_BOX = os.getenv('MAIL_BOX')
    MAIL_TO = [mail_to]
    MAIL_BODY = f"""
        Conforme solicitado, a tabela abaixo contém dados estatísticos de performance do jogador {player_name} na temporada {season}\n\n
    """

    # Enviando e-mail
    try:
        send_simple_mail(username=MAIL_FROM,
                        password=MAIL_PWD,
                        server=MAIL_SERVER,
                        mail_box=MAIL_BOX,
                        mail_to=MAIL_TO,
                        mail_body=MAIL_BODY,
                        df=player_stats,
                        df_on_body=True,
                        df_on_attachment=True,
                        attachment_filename=f'{player_name}_{season.replace("-", "_")}_stats.csv',
                        subject=f'[NBAFlow] Estatísticas de {player_name} na temporada {season}')
        logger.info(f'E-mail com estatísticas de {player_name} na temporada {season} enviado com sucesso. Programa encerrado.')
    except Exception as e:
        logger.error(f'Erro ao enviar e-mail. Exception: {e}')
        exit()
    
    