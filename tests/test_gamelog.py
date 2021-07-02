"""
---------------------------------------------------
----------------- TESTES: gamelog -----------------
---------------------------------------------------
Scripts reponsável por validar algumas das funciona-
lidades contidas no módulo gamelog deste projeto.
Para tal, serão propostas execuções dos métodos da
classe NBAGamelog para extrações pontuais de dados
de partidas de jogadores específicos.

Table of Contents
---------------------------------------------------
1. Configurações Iniciais
    1.1 Importando bibliotecas
2. Histórico de Partidas da NBA
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

# Importando classe encapsulada
from gamelog.gamelog import NBAGamelog

# Funções auxiliares da biblioteca NBA
from nba_api.stats.static import players


"""
---------------------------------------------------
--------- 2. HISTÓRICO DE PARTIDAS DA NBA ---------
        2.1 Partidas de jogador específico
---------------------------------------------------
Nesta task, será proposta a extração do histórico
de partidas de Damian Lillard na temporada 2020-21,
considerando temporada regular, playoffs e também
um método capaz de retornar dados da temporada
completa (regular + playoffs).

Com o conhecimento prévio do número de partidas
a ser extraída em cada caso para o Dame, é possível
inserir pontos de controle e validadores a serem
contrapostos ao retorno dos métodos da classe.
"""

# Instanciando classe
nba_gamelog = NBAGamelog()

# Definindo variáveis de teste
dame_id = players.find_players_by_full_name('Damian Lillard')[0]['id']
test_season = '2020-21'

# Extraindo histórico de partidas de Damian Lillard - Temporada Regular
dame_reg_season = nba_gamelog.player_gamelog_season(player_id=dame_id,
                                                    season=test_season,
                                                    season_type_all_star='Regular Season',
                                                    timeout=60)

# Extraindo histórico de partidas de Damian Lillard - Playoffs
dame_playoffs = nba_gamelog.player_gamelog_season(player_id=dame_id,
                                                  season=test_season,
                                                  season_type_all_star='Playoffs',
                                                  timeout=60)

# Extraindo histórico de partidas de Damian Lillard - Regular + Playoffs
dame_season = nba_gamelog.player_gamelog_season_complete(player_id=dame_id,
                                                         season=test_season,
                                                         timeout=60)                                                                                                          

# Testes
assert len(dame_reg_season) == 67, 'Número diferente de partidas retornadas para o jogador em temporada regular'
assert len(dame_playoffs) == 6, 'Número diferente de partidas retornadas para o jogador em playoffs'
assert len(dame_season) == len(dame_reg_season) + len(dame_playoffs), 'Método de retorno de partidas da temporada completa difere da soma individual das temporadas'

