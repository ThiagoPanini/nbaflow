"""Managing NBA players data.

This module provides features to help users to analyse data from NBA players.
This can be achieved by handling operations on nba_api python package and its
endpoints that have players data.

___
"""

# Importing libraries
from nba_api.stats.endpoints import (
    commonallplayers
)

import pandas as pd
from datetime import datetime

from nbaflow.utils.log import log_config


# Setting up a logger object
logger = log_config(logger_name=__file__)


def get_players_data(
    timeout: int = 30,
    only_active_players: bool = True
) -> pd.DataFrame:
    """
    Retrieve data about NBA players.

    This function uses the `commonallplayers` nba_api endpoint to retrieve
    data about NBA players, regardless wheter they are active or not. So, the
    user gets the data in a pandas DataFrame format.

    Example:
        ```python
        # Importing the function to get data about NBA players
        from nbaflow.players import get_players_data

        # Getting NBA data
        df_players_data = get_players_data(only_active_players=False)
        ```

    Args:
        active_players (bool, optional):
            If True, only active players' data will be returned.

    Returns:
        pd.DataFrame: A DataFrame containing data about NBA players.

    Note:
        This function fetches data about NBA players using the
        'common_all_players' endpoint from the nba_api.
        It optionally filters the data to include only active players.
    """

    # Getting players data
    df_players = commonallplayers.CommonAllPlayers(
        timeout=timeout
    ).common_all_players.get_data_frame()

    # Preparing the DataFrame columns
    df_players.columns = [
        col.lower().strip() for col in df_players.columns
    ]

    # Getting only active players (if applicable)
    if only_active_players:
        current_year = str(datetime.now().year)
        df_players = df_players.query(f"to_year == {current_year}")

    return df_players
