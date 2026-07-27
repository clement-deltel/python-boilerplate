"""Module used to interact with the PostgreSQL database."""

# Standard Library
from collections.abc import Callable
from functools import wraps
from time import sleep

# Third-party
from psycopg2 import DatabaseError, connect, extensions

# Local Application
from app_name.common.config import DatabaseConfig, get_config_class
from app_name.event.logger.log import log


class Postgres:
    """Class specifying attributes and methods related to the PostgreSQL database."""

    def __init__(self) -> None:
        """Initialize class."""
        self.config: DatabaseConfig = get_config_class("database")
        self.connection = None

    def connect(self) -> None:
        """Connect to database.

        Raises:
            Exception: if all attempts to connect to the database failed.
        """
        for attempt in range(1, self.config.retry_max + 1):
            try:
                log().logger.info(f"Connecting to database: {self.config.name}...")
                self.connection = connect(
                    dbname=self.config.name,
                    user=self.config.username,
                    password=self.config.password,
                    host=self.config.host,
                    port=self.config.port,
                    connect_timeout=self.config.connect_timeout,
                )
            except DatabaseError as err:
                log().logger.error(f"Error connecting to database: {err}")
            else:
                log().logger.info("Successfully connected to database.")
                break
            if attempt == self.config.retry_max:
                log().logger.info(f"Attempts: {attempt}/{self.config.retry_max}. Aborting...")
                message = "Unable to establish database connection"
                raise Exception(message)
            log().logger.info(f"Attempts: {attempt}/{self.config.retry_max}. Retrying in {self.config.retry_delay} seconds...")
            sleep(self.config.retry_delay)

    def disconnect(self) -> None:
        """Disconnect from database."""
        if self.connection:
            try:
                log().logger.info(f"Disconnecting from database: {self.config.name}...")
                self.connection.close()
            except DatabaseError as err:
                log().logger.error(f"Error disconnecting from database: {err}")
            else:
                log().logger.info("Successfully disconnected from database.")
            finally:
                self.connection = None

    def execute_query(self, cursor: extensions.cursor, query: str, *params: tuple) -> None:
        """Execute a SQL query.

        Args:
            cursor (extensions.cursor): database cursor.
            query (str): SQL query.
            params (tuple): additional parameters for the query.

        Raises:
            Exception: if all attempts to run SQL query failed.
        """
        for attempt in range(1, self.config.retry_max + 1):
            try:
                if params:
                    cursor.executemany(query, params)
                else:
                    cursor.execute(query)
            except DatabaseError as err:
                log().logger.error(f"Error executing query: {err}")
            else:
                log().logger.debug("Successfully executed query.")
                break
            if attempt == self.config.retry_max:
                log().logger.info(f"Attempts: {attempt}/{self.config.retry_max}. Aborting...")
                message = "Unable to process SQL query"
                raise Exception(message)
            log().logger.info(f"Attempts: {attempt}/{self.config.retry_max}. Retrying in {self.config.retry_delay} seconds...")
            sleep(self.config.retry_delay)

    @staticmethod
    def cursor_required(func: Callable) -> Callable:
        """Ensure a database cursor is available."""

        @wraps(func)
        def wrapper(self, *args: tuple, **kwargs: dict) -> Callable:  # noqa: ANN001
            """Run the query with the database cursor."""
            cursor = None
            try:
                cursor = self.connection.cursor()
                result = func(self, cursor, *args, **kwargs)
                cursor.close()
                return result
            except DatabaseError as err:
                log().logger.error(err)
                if cursor:
                    cursor.close()
                raise

        return wrapper

    def commit(self) -> None:
        """Commit the current transaction."""
        if self.connection:
            self.connection.commit()

    @cursor_required
    def insert(self, cursor: extensions.cursor, query: str, *params: tuple) -> None:
        """Insert a record into the database."""
        self.execute_query(cursor, query, *params)
        self.commit()

    @cursor_required
    def update(self, cursor: extensions.cursor, query: str, *params: tuple) -> None:
        """Update a record in the database."""
        self.execute_query(cursor, query, *params)
        self.commit()

    @cursor_required
    def delete(self, cursor: extensions.cursor, query: str, *params: tuple) -> None:
        """Delete a record from the database."""
        self.execute_query(cursor, query, *params)
        self.commit()

    @cursor_required
    def select(self, cursor: extensions.cursor, query: str, *params: tuple) -> tuple:
        """Select records from the database."""
        self.execute_query(cursor, query, *params)
        columns = [element[0] for element in cursor.description]
        data = cursor.fetchall() if cursor else []
        return columns, data


# Global
_database_instance = None


def set_database(database: Postgres) -> None:
    """Set global instance.

    Args:
        database (Postgres): database instance.
    """
    global _database_instance
    _database_instance = database


def get_database() -> Postgres:
    """Get global instance, instantiate it if None.

    Returns:
        Postgres: database instance.
    """
    global _database_instance
    if _database_instance is None:
        _database_instance = Postgres()
    return _database_instance
