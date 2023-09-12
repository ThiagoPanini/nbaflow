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


class NBAPlayers():
    """
    A class for fetching information about NBA players.

    Args:
        request_timeout (int, optional):
            The timeout duration for API requests in seconds. Defaults to 30.

    Attributes:
        request_timeout (int): The timeout duration for API requests.

    Methods:
        get_players_info(active_players=True):
            Retrieve information about NBA players.

    Example:
        >>> nba_data = NBAPlayers()
        >>> player_info = nba_data.get_players_info(active_players=True)
    """

    def __init__(
        self,
        request_timeout: int = 30,
        handle_timeout_errors: bool = True,
        request_max_tries: int = 5
    ) -> None:
        """
        Initialize the NBAPlayers instance.

        Args:
            request_timeout (int, optional):
                The timeout duration for API requests in seconds.
                Defaults to 30.
        """

        self.request_timeout = request_timeout
        self.handle_timeout_errors = handle_timeout_errors
        self.request_max_tries = request_max_tries

    def get_players_info(self, active_players: bool = True) -> pd.DataFrame:
        """
        Retrieve information about NBA players.

        Args:
            active_players (bool, optional):
                If True, only active players' information will be returned.
                Defaults to True.

        Returns:
            pd.DataFrame: A DataFrame containing information about NBA players.

        Note:
            This method fetches data about NBA players using the
            'common_all_players' endpoint from the nba_api.
            It optionally filters the data to include only active players.

        Example:
            >>> nba_data = NBAPlayers()
            >>> player_info = nba_data.get_players_info(active_players=True)
        """

        # Getting players information
        df_players = commonallplayers.CommonAllPlayers(
                timeout=self.request_timeout
            ).common_all_players.get_data_frame()

        # Preparing the DataFrame columns
        df_players.columns = [
            col.lower().strip() for col in df_players.columns
        ]

        # Getting only active players (if applicable)
        if active_players:
            current_year = str(datetime.now().year)
            df_players = df_players.query(f"to_year == {current_year}")

        return df_players
