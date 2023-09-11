"""Test cases for features built in players.py module.

This file handles unit tests for everything under players module, specially
the class NBAPlayers. So, for any new capability delivered in the
aforementioned module, this test script is the place where test cases will be
found.

___
"""

# Importing libraries
import pytest
import pandas as pd

from nbaflow.players import NBAPlayers


@pytest.mark.players
@pytest.mark.get_players_info
def test_players_info_is_delivered_as_a_pandas_dataframe(
    nba_players: NBAPlayers
):
    """
    G: Given that an user wants to get information about NBA players
    W: When the method get_players_info() is called from NBAPlayers class
    T: Then the returned object must be a pandas DataFrame
    """

    # Calling the method to get information about NBA players
    assert isinstance(nba_players.get_players_info(), pd.DataFrame)


@pytest.mark.players
@pytest.mark.get_players_info
def test_players_info_dataframe_has_a_set_of_expected_columns(
    nba_players: NBAPlayers
):
    """
    G: Given that an user wants to get information about NBA players
    W: When the method get_players_info() is called from NBAPlayers class
    T: Then the returned DataFrame must have a set of expected columns
    """

    # Setting up the list of expected DataFrame columns
    expected_cols = ['person_id', 'display_last_comma_first',
                     'display_first_last', 'rosterstatus', 'from_year',
                     'to_year', 'playercode', 'player_slug', 'team_id',
                     'team_city', 'team_name', 'team_abbreviation',
                     'team_code', 'team_slug', 'games_played_flag',
                     'otherleague_experience_ch']

    # Getting players DataFrame and its columns
    df_players_info = nba_players.get_players_info()
    current_cols = list(df_players_info.columns)

    assert current_cols == expected_cols


@pytest.mark.players
@pytest.mark.get_players_info
def test_total_of_active_players_is_less_than_total_of_all_players(
    nba_players: NBAPlayers
):
    """
    G: Given that an user wants to get information about NBA players
    W: When the method get_players_info() is called twice with its argument
       "active" set as both True and False
    T: Then the DataFrame of active players (active_players=True) must have
       less rows than the DataFrame of all players (active_players=False),
       prooving that the active players filter is working properly
    """

    # Getting both DataFrames of active and all players
    df_active_players = nba_players.get_players_info(active_players=True)
    df_all_players = nba_players.get_players_info(active_players=False)

    assert len(df_active_players) < len(df_all_players)
