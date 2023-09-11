"""Confest file for managing pytest fixtures and other components.

This file will handle essential components and elements to be used on test
scripts along the project, like features and other things.

___
"""

# Importing libraries
import pytest
import pandas as pd

from nbaflow.players import NBAPlayers


# Returning a NBAPlayers class object
@pytest.fixture()
def nba_players() -> NBAPlayers:
    return NBAPlayers()

# Returning a pandas DataFrame with result of get_players_info() method
@pytest.fixture()
def df_players_info(nba_players: NBAPlayers) -> pd.DataFrame:
    return nba_players.get_players_info() # Validar se precisa mesmo, dado que existem regras como active=True
