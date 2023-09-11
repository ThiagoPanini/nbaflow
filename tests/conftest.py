"""Confest file for managing pytest fixtures and other components.

This file will handle essential components and elements to be used on test
scripts along the project, like features and other things.

___
"""

# Importing libraries
import pytest

from nbaflow.players import NBAPlayers


# Returning a NBAPlayers class object
@pytest.fixture()
def nba_players() -> NBAPlayers:
    return NBAPlayers()
