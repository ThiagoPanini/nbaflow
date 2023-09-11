"""Managing NBA players data.

This module provides features to help users to analyse data from NBA players.
This can be achieved by handling operations on nba_api python package and its
endpoints that have players data.

___
"""

# Importing libraries
from nba_api.stats.endpoints import (
    commonallplayers,
    playergamelog
)

import requests
from requests.exceptions import ReadTimeout

import pandas as pd

from datetime import datetime
from time import sleep

from nbaflow.utils.log import log_config
from nbaflow.utils.requests import handle_timeout_errors


# Setting up a logger object
logger = log_config(logger_name=__file__)


class NBAPlayers():
    """
    """

    def __init__(self, request_timeout: int = 30) -> None:
        self.request_timeout = request_timeout

    def get_players_info(self, active_players: bool = True) -> pd.DataFrame:
        """
        """

        # Getting players information
        df_players_info = commonallplayers.CommonAllPlayers(
            timeout=self.request_timeout
        ).common_all_players.get_data_frame()

        # Preparing the DataFrame columns
        df_players_info.columns = [
            col.lower().strip() for col in df_players_info.columns
        ]

        # Getting only active players (if applicable)
        if active_players:
            current_year = str(datetime.now().year)
            df_players_info = df_players_info.query("to_year == @current_year")
        
        return df_players_info



