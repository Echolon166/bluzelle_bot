import functools

import dataset
import config


def connect_db(function):
    """
    Decorator that creates a database object and inserts itself
        as the first argument in the calling function.
    Useful to prevent global objects.
    """

    @functools.wraps(function)
    def wrapper(*args, **kwargs):
        result = None

        with dataset.connect(config.CONFIG.database_connection) as db:
            result = function(db, *args, **kwargs)

        return result

    return wrapper
