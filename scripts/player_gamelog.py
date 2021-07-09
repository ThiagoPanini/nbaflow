"""
---------------------------------------------------
------------- SCRIPTS: player_gamelog -------------
---------------------------------------------------
Script responsável por retornar detalhes de partidas
realizadas por um determinado jogador em uma determinada
temporada na NBA. Como parâmetros do usuário, pode-se
fornecer o nome completo do jogador e a temporada
alvo de análise de extração dos dados.

Table of Contents
---------------------------------------------------
1. Configurações Iniciais
    1.1 Importando bibliotecas
2. Histórico de Partidas da NBA
    2.1 Extração completa
---------------------------------------------------
"""

# Author: Thiago Panini
# Date: 08/07/2021


"""
---------------------------------------------------
------------ 1. CONFIGURAÇÕES INICIAIS ------------
            1.1 Importando bibliotecas
---------------------------------------------------
"""

# Importando classe encapsulada
from core.gamelog import NBAGamelog

# Funções auxiliares da biblioteca NBA
from nba_api.stats.static import players

# Pacotes python padrão
import pandas as pd
from datetime import datetime


"""
---------------------------------------------------
--------- 2. HISTÓRICO DE PARTIDAS DA NBA ---------
       2.1 Extração individual de jogador
---------------------------------------------------
Nesta task, será proposta a extração individual de
um único jogador considerando uma única temporada.
"""

# Coletando parâmetros de entrada do usuário: nome do jogador e temporada alvo
player_name = 'Damian Lillard'
current_year = datetime.now().year
season = str(current_year - 1) + '-' + str(current_year)[-2:]

# Extraindo id do jogador a partir do nome
player_id = players.find_players_by_full_name(player_name)[0]['id']

# Instanciando classe e extraindo gamelog
nba_gamelog = NBAGamelog()
gamelog = nba_gamelog.player_gamelog_season_complete(player_id, season)

# Preparando colunas do DataFrame de retorno
gamelog.columns = [col.lower() for col in gamelog.columns]
src_columns = list(gamelog.columns)
src_columns.insert(2, 'player_name')
gamelog['player_name'] = player_name
gamelog = gamelog.loc[:, src_columns]


"""
---------------------------------------------------
--------- 2. HISTÓRICO DE PARTIDAS DA NBA ---------
     2.2 Extraindo indicadores de performance
---------------------------------------------------
Tópico responsável pela extração de indicadores
de performance do jogador a partir do histórico de
partidas gerado no passo anterior.
"""

# Gerando indicadores de temporada
total_matches = len(gamelog)
total_wins = gamelog['wl'].value_counts()['W']
pct_wins = round(total_wins / total_matches, 3)
season_status = str(total_wins) + '/' + str(total_matches)

# Gerando indicadores de performance
avg_minutes = round(gamelog['min'].mean(), 1)
avg_fg_pct = round(gamelog['fg_pct'].mean(), 3)
avg_fg3_pct = round(gamelog['fg3_pct'].mean(), 3)
avg_ft_pct = round(gamelog['ft_pct'].mean(), 3)
avg_points = round(gamelog['pts'].mean(), 1)
avg_plus_minus = round(gamelog['plus_minus'].mean(), 1)

# Building string with performance
result_string = f"""
------------------------------------------
Estatísticas de Temporada: {player_name}
------------------------------------------
Season: {season}

[1] Indicadores gerais
    * Partidas totais: {total_matches}
    * Status da temporada: {season_status}
    * Percentual de vitórias: {str(100 * pct_wins) + "%"}
    
[2] Indicadores de performance
    * Média de minutos: {avg_minutes}
    * Média de arremessos certos: {avg_fg_pct}
    * Média de arremessos certos do perímetro: {avg_fg3_pct}
    * Média de lances livres certos: {avg_ft_pct}
    * Média de pontos: {avg_points}
    * Média de plus minus: {avg_plus_minus}
"""


"""
---------------------------------------------------
--------- 2. HISTÓRICO DE PARTIDAS DA NBA ---------
         2.3 Envio de resultados por e-mail
---------------------------------------------------
Para testar uma aplicação real dessa extração, será
proposto o envio dos resultados em um e-mail simples.
Posteriormente, a ideia é consolidar esse desenvolvimento
em um tópico SNS da AWS ou através do serviço SES
"""

# Importando pacote de e-mail e libs auxiliares
from xchange_mail.mail import send_simple_mail
import os
from dotenv import load_dotenv, find_dotenv

# Lendo variáveis de ambiente
load_dotenv(find_dotenv())

# Definindo variáveis de configuração do e-mail
USERNAME = os.getenv('MAIL_FROM')
PWD = os.getenv('MAIL_PASSWORD')
SERVER = 'outlook.office365.com'
MAIL_BOX = os.getenv('MAIL_BOX')
MAIL_TO = os.getenv('MAIL_TO')
if MAIL_TO.count('@') > 1:
    MAIL_TO = MAIL_TO.split(';')
else:
    MAIL_TO = [MAIL_TO]

# Definindo variáveis de formatação do e-mail
SUBJECT = f'[NBAFLOW] Estatísticas de {player_name} em {season}'

# Enviando e-mail
send_simple_mail(username=USERNAME,
                 password=PWD,
                 server=SERVER,
                 mail_box=MAIL_BOX,
                 mail_to=MAIL_TO,
                 subject=SUBJECT,
                 mail_body=result_string)
