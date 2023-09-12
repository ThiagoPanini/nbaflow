"""Confest file for managing pytest fixtures and other components.

This file will handle essential components and elements to be used on test
scripts along the project, like features and other things.

___
"""

# Importing libraries
import pytest
import pandas as pd

from nbaflow.players import get_players_data


# The result of get_players_data function for active players only
@pytest.fixture()
def df_active_players_data() -> pd.DataFrame:
    return get_players_data(active_players=True)


# The result of get_players_data function for all players in NBA history
@pytest.fixture()
def df_all_players_data() -> pd.DataFrame:
    return get_players_data(active_players=False)
