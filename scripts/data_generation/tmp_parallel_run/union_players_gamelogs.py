import os
import pandas as pd
from nba_api.stats.endpoints import commonallplayers

data_path = os.path.join(os.getcwd(), 'data')
files = [f for f in os.listdir(data_path) if 'all_players_gamelog_' in f]
print(files)

gamelog = pd.DataFrame()
for f in files:
    gamelog = gamelog.append(pd.read_csv(os.path.join(data_path, f)))
    print(f'Dimensão atualizada do arquivo: {gamelog.shape}')

# Coletando dados de jogadores ativos
TIMEOUT = 30
CURRENT_YEAR = str(datetime.now().year - 1)
print(f'Extraindo jogadores ativos da liga')
i = 0
while True:
    i += 1
    try:
        # Retornando e filtrando dados apenas de jogadores ativos
        players_raw = commonallplayers.CommonAllPlayers(timeout=TIMEOUT).common_all_players.get_data_frame()
        players_raw = players_raw.query('TO_YEAR == @CURRENT_YEAR and TEAM_ID > 0')
        players_raw['PLAYER_TEAM'] = players_raw['TEAM_CITY'] + ' ' + players_raw['TEAM_NAME']

        # Filtrando colunas
        players_info = players_raw.loc[:, ['PERSON_ID', 'DISPLAY_FIRST_LAST', 'PLAYER_TEAM', 'TEAM_ABBREVIATION',
                                           'FROM_YEAR', 'TO_YEAR']]
        players_info.columns = ['player_id', 'player_name', 'player_team', 'player_team_abbrev', 'from_year', 'to_year']
        players_info.reset_index(drop=True, inplace=True)

        break
    except Exception as e:
        TIMEOUT += 5
        if i % 5 == 0:
            print(f'Iniciando {i + 1}ª tentativa com timeout ajustado para {TIMEOUT}s')
        continue
        
# Visualizando base
print(f'Quantidade de jogadores ativos na liga: {len(players_info)}')

# Trazendo nome do jogador pra base
gamelog = gamelog.merge(players_info.loc[:, ['player_id', 'player_name', 'player_team', 'player_team_abbrev']], 
                        how='left', on='player_id')
gamelog.drop('player_id', axis=1, inplace=True)

print(f'Dimensões finais do arquivo: {gamelog.shape}')
gamelog.to_csv(os.path.join(data_path, 'all_players_gamelog.csv'), index=False)