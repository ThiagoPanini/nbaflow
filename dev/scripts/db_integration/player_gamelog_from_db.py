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
from io import BytesIO
from exchangelib import attachments
from cloudgeass.aws.rds import PostgreSQLConnection
from nbaflow.utils.log import log_config

# Pacotes python padrão
import pandas as pd
from datetime import datetime
import os
from dotenv import find_dotenv, load_dotenv

# Biblioteca customizada para envio de e-mails
import jaiminho.exchange as jex

# Logging
import logging


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
db = PostgreSQLConnection(
    host=os.getenv('DB_HOST'), 
    database=os.getenv('DB_NAME'), 
    user=os.getenv('DB_USER'),
    password=os.getenv('DB_PWD')
)

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

    # Configurando e-mail a ser enviado
    try:
        # Preparando insumos
        df_html = jex.df_to_html(player_stats)
        zip_att = zip([f'{player_name}_{season}.csv'], [player_stats])

        # Enviando e-mail
        jex.send_mail(
            username=MAIL_FROM,
            password=os.getenv('MAIL_PWD'),
            server=MAIL_SERVER,
            mail_box=MAIL_BOX,
            mail_to=MAIL_TO,
            subject=f'[NBAFlow] Estatísticas de {player_name} na temporada {season}',
            body=MAIL_BODY + df_html,
            zip_attachments=zip_att
        )
        logger.info(f'E-mail com estatísticas de {player_name} na temporada {season} enviado com sucesso. Programa encerrado.')
    except Exception as e:
        logger.error(f'Erro ao enviar e-mail. Exception: {e}')
        exit()
