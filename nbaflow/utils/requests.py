"""Useful functions that help on making requests to nba_api endpoints.

This module have functions built in order to help other package modules and
classes whenever it's necessary to use requests library to get NBA data.

___
"""

# Importing libraries
from requests.exceptions import ReadTimeout

from nbaflow.utils.log import log_config

from time import sleep


# Setting up a logger object
logger = log_config(logger_name=__file__)


# Function that handles timeout errors on requesting data from nba_api
def handle_timeout_errors(
    function,
    function_args: dict,
    max_attempts: int = 10,
    timesleep: int = 3,
    timeout_increase: int = 5
):
    """
    Handle timeout errors when requesting data from nba_api.

    This function can be used whenever users want to take care of ReadTimeout
    errors that may occur while requesting NBA data using nba_api endpoints. In
    some cases, increasing the request timeout and waiting a while for a new
    attempt can be useful to succesfully get the data. And that's exactly what
    this function do: it receives a max number of attempts and a timeout
    increase factor that is applied whenever a ReadTimeout error is caught.

    To do this, this function receives two main required arguments: a function
    where the nba_api endpoint is called and its arguments as a python dict.
    With that in hands, the logic applied on this function is responsible to
    catch ReadTimeout errors and try the request again after a while.

    Example:
        ```python
        # Importing some function that makes requests to nba_api endpoints
        from nbaflow.players import get_players_data
        from nbaflow.utils.requests import handle_timeout_errors

        # Insted of calling the function directly, let's handle timeout errors
        df_players_data = handle_timeout_errors(
            function=get_players_data,
            function_args={"timeout": 30, "active_players": False},
            max_attempts=5
        )
        ```

    Args:
        function (function):
            The function to call for requesting data.

        function_args (dict):
            A dictionary containing the arguments to be passed to the function.

        max_attempts (int, optional):
            The maximum number of attempts to make the request.

        timesleep (int, optional):
            The number of seconds to sleep between attempts.

        timeout_increase (int, optional):
            The amount by which to increase the timeout on each attempt.

    Returns:
        Any: Whatever the function passed in the function argument returns.

    Raises:
        ReadTimeout:
            If the request to the nba_api endpoint can't be made after \
            all attempts established in `max_attempts`.

        Exception: If any other error is catched during the request process.

    Note:
        This function handles timeout errors (ReadTimeout) that may occur
        during the request process. It makes multiple attempts (up to
        'max_attempts') with increasing timeouts.
    """

    # Looping over a given number of request attempts
    for i in range(max_attempts):
        try:
            # Returning whatever the function was coded to return
            return function(**function_args)

        # Handling timeout errors
        except ReadTimeout:
            logger.warning(f"Timeout error on requesting data w/ function "
                           f"{function.__name__}() with the following args "
                           f"{function_args}. A new attempt will be made with "
                           f"+{timeout_increase} secs of timeout increase.")

            # Increasing timeout on function args for a new attempt
            function_args["timeout"] += timeout_increase
            sleep(timesleep)

        # Another error was thrown and so there is nothing to do
        except Exception as e:
            logger.error("Error on trying to request data with function "
                         f"{function.__name__}() with the following args "
                         f"{function_args}.")
            raise e

    # Exceeded max tries
    logger.error("Exceeded max tries when trying to call the function "
                 f"{function.__name__}(). None will be returned.")
    raise ReadTimeout
