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
    endpoint_request,
    max_attempts: int = 5,
    timesleep: int = 5,
):
    """
    Handle timeout errors when requesting data from nba_api.

    Args:
        endpoint_request (Any):
            The request to be made using the NBA API endpoint.

        max_attempts (int, optional):
            The maximum number of attempts to make the request. Defaults to 5.

        timesleep (int, optional):
            The number of seconds to sleep between attempts. Defaults to 5.

    Returns:
        Any: The result returned by the provided request.

    Raises:
        ReadTimeout: If all attempts to make the request time out.

    Note:
        This function handles timeout errors (ReadTimeout) that may occur
        during the request process. It makes multiple attempts (up to
        'max_attempts') with increasing timeouts.

    Example:
        >>> data = handle_timeout_errors(
        >>>    request_data, max_attempts=5, timesleep=3
        >>> )
    """

    # Looping over a given number of request attempts
    for i in range(max_attempts):
        try:
            # Returning whatever the function was coded to return
            return endpoint_request

        # Handling timeout errors
        except ReadTimeout:
            logger.warning("Timeout error on requesting data from nba_api in "
                           f"the {i + 1}/{max_attempts} try. Next attempt "
                           f"will be made after {timesleep} seconds.")

            # Sleeping time before next request attempt
            sleep(timesleep)

        # Another error was thrown and so there is nothing to do
        except Exception as e:
            logger.error("A different exception than ReadTimeout was thrown "
                         "and so this handler function isn't able to deal "
                         "with it. Check the traceback for more details.")
            raise e

    # Exceeded max tries
    logger.error("Exceeded max tries when trying to request data from nba_api")
    raise ReadTimeout
