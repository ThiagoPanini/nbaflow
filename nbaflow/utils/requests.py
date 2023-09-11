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


# Function that handles timeout erros on requesting data from nba_api
def handle_timeout_errors(
    function,
    function_args: dict,
    max_attempts: int = 10,
    timesleep: int = 3,
    timeout_increase: int = 5
):
    """
    Handle timeout errors when requesting data from nba_api.

    Args:
        function (function):
            The function to call for requesting data.

        function_args (dict):
            A dictionary containing the arguments to be passed to the function.

        max_attempts (int, optional):
            The maximum number of attempts to make the request. Defaults to 10.

        timesleep (int, optional):
            The number of seconds to sleep between attempts. Defaults to 3.

        timeout_increase (int, optional):
            The amount by which to increase the timeout on each attempt.
            Defaults to 5.

    Returns:
        Any: The result returned by the provided function.

    Raises:
        Exception: If an error occurs during the request process.

    Note:
        This function handles timeout errors (ReadTimeout) that may occur
        during the request process. It makes multiple attempts (up to
        'max_attempts') with increasing timeouts.

    Example:
        >>> data = handle_timeout_errors(request_data, {'param1': 'value1',
        'param2': 'value2'}, max_attempts=5)
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
