"""Test cases for features built in players.py module.

This file handles unit tests for everything under players module. So, for any
new capability delivered in the aforementioned module, this test script is the
place where test cases will be found.

___
"""

# Importing libraries
import pytest
import pandas as pd


# @pytest.mark.skip(reason="Figuring out how to mock nba_api endpoints")
@pytest.mark.players
@pytest.mark.get_players_info
def test_players_info_is_delivered_as_a_pandas_dataframe(
    df_active_players_data: pd.DataFrame
):
    """
    G: Given that an user wants to get information about NBA players
    W: When the function get_players_info() is called from players module
    T: Then the returned object must be a pandas DataFrame
    """
    assert isinstance(df_active_players_data, pd.DataFrame)


# @pytest.mark.skip(reason="Figuring out how to mock nba_api endpoints")
@pytest.mark.players
@pytest.mark.get_players_info
def test_players_info_dataframe_has_a_set_of_expected_columns(
    df_active_players_data: pd.DataFrame
):
    """
    G: Given that an user wants to get information about NBA players
    W: When the function get_players_info() is called from players module
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
    current_cols = list(df_active_players_data.columns)

    assert current_cols == expected_cols


# @pytest.mark.skip(reason="Figuring out how to mock nba_api endpoints")
@pytest.mark.players
@pytest.mark.get_players_info
def test_total_of_active_players_is_less_than_total_of_all_players(
    df_active_players_data: pd.DataFrame,
    df_all_players_data: pd.DataFrame
):
    """
    G: Given that an user wants to get information about NBA players
    W: When the function get_players_info() is called twice with its argument
       "active" set as both True and False
    T: Then the DataFrame of active players (active_players=True) must have
       less rows than DataFrame of all players (active_players=False),
       prooving that the active players filter is working properly
    """
    assert len(df_active_players_data) < len(df_all_players_data)
