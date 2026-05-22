"""Module used to interact with the Oracle database."""

# Standard Library
from collections.abc import Callable
from functools import wraps
from time import sleep
from typing import Any

# Third-party
import oracledb
from oracledb import Cursor, Error

# Local Application
from app_name.common.config import DatabaseConfig, get_config_class
from app_name.event.logger.log import log


def to_literal(variable: Any) -> str:
    """Convert Python variable to Oracle SQL literal.

    Bool, float, int, str, and None are supported.

    Args:
        variable (Any): input variable.

    Returns:
        str: variable SQL literal formatted.
    """
    match variable:
        case bool():
            return "1" if variable else "0"
        case float():
            # repr() avoids some display issues better than str() for floats
            return repr(variable)
        case int():
            return str(variable)
        case str():
            escaped = variable.replace("'", "''")
            return f"'{escaped}'"
        case None:
            return "NULL"
        case _:
            message = f"Unsupported value type: {type(variable).__name__} -> {variable!r}"
            raise TypeError(message)


def to_literal_list(variables: list[Any]) -> str:
    """Convert a Python list into a SQL IN-list body.

    ['A', 'B'] -> 'A', 'B'
    [1, 2, 3] -> 1, 2, 3

    Note:If the list is empty, returns NULL so that:
      col IN (NULL)
    matches nothing in Oracle.

    Args:
        variables (list[Any]): input variable list.

    Returns:
        str: SQL IN-list literal formatted.

    """
    if not variables:
        return "NULL"

    return ", ".join(to_literal(variable) for variable in variables)


def to_statement_list(query: str) -> list[str]:
    """Split SQL query on semicolons.

    Assume semicolons terminate statements and do not appear inside string literals.

    Args:
        query(str): multi-lines SQL query.

    Returns:
        list: SQL statement list.
    """
    statements = [statement.strip() for statement in query.split(";")]
    return [statement for statement in statements if statement]


def to_cte_union_rows(values: list[str], alias: str = "name", table: str = "dual") -> str:
    """Format a list of values as SELECT ... FROM dual UNION ALL rows for use in a Common Table Expression or CTE.

    Args:
        values (list(str)): string values to emit as literal rows.
        alias (str): column alias for the first row (subsequent rows omit it).
        table (str): target table name. Defaults to "dual" (Oracle).

    Returns:
        A SQL fragment ready to be spliced into a CTE body.

    Raises:
        ValueError: If values is empty, since an empty CTE arm would be invalid SQL.
    """
    if not values:
        message = "Cannot produce a CTE row block from an empty list."
        raise ValueError(message)

    rows = []
    for i, value in enumerate(values):
        escaped = value.replace("'", "''")  # SQL-escape single quotes
        col = f"'{escaped}' as {alias}" if i == 0 else f"'{escaped}'"
        rows.append(f"    select {col} from {table} union all")  # noqa: S608

    return "\n".join(rows)


class Oracle:
    """Class specifying attributes and methods related to the Oracle database."""

    def __init__(self) -> None:
        """Initialize class."""
        self.config: DatabaseConfig = get_config_class("database")
        self.alias = self.config.tns_alias if self.config.tns else self.config.alias
        self.extra = {"database_type": self.config.type, "database_mode": self.config.mode}

        self.connection = None

        if self.config.mode == "thick":
            self.init_client()

    def init_client(self) -> None:
        """Initialize Oracle client, optionally using a tnsnames.ora configuration file."""
        config_dir = None

        if self.config.tns:
            tns_path = self.config.tns_path
            tns_file_path = tns_path.joinpath("tnsnames.ora")

            if not tns_path.is_dir:
                message = f"No such file or directory: {tns_path}"
                raise FileNotFoundError(message)
            if not tns_file_path.is_file:
                message = f"No such file or directory: {tns_file_path}"
                raise FileNotFoundError(message)

            config_dir = str(tns_path)

        try:
            oracledb.init_oracle_client(config_dir=config_dir)
        except oracledb.ProgrammingError as exc:
            # Safe to ignore if already initialized in the same Python process
            if "init_oracle_client() has already been called" not in str(exc):
                raise

    def connect(self) -> None:
        """Connect to database."""
        log().logger.info("Connecting to database...", extra=self.extra)
        for attempt in range(1, self.config.retry_max + 1):
            try:
                self.connection = oracledb.connect(dsn=self.alias, user=self.config.username, password=self.config.password)
            except Error as err:
                log().logger.error("Error connecting to database: %s", err, extra=self.extra)
            else:
                log().logger.info("Successfully connected to database.", extra=self.extra)
                break
            if attempt == self.config.retry_max:
                log().logger.info("Attempts: %s/%s. Aborting...", attempt, self.config.retry_max, extra=self.extra)
                message = "Unable to establish database connection"
                raise Exception(message)
            log().logger.info("Attempts: %s/%s. Retrying in %s seconds...", attempt, self.config.retry_max, self.config.retry_delay, extra=self.extra)
            sleep(self.config.retry_delay)

    def disconnect(self) -> None:
        """Disconnect from database."""
        if self.connection:
            try:
                log().logger.info("Disconnecting from database...", extra=self.extra)
                self.connection.close()
            except Error as err:
                log().logger.error("Error disconnecting from database: %s", err, extra=self.extra)
            else:
                log().logger.info("Successfully disconnected from database.", extra=self.extra)
            finally:
                self.connection = None

    def execute_sql(self, cursor: Cursor, query: str) -> None:
        """Execute a SQL query.

        Args:
            cursor (Cursor): database cursor.
            query (str): SQL query.

        Returns:
            list: result of the query, list of records.
        """
        if self.connection is None:
            log().logger.error("No active database connection. Please connect first.", extra=self.extra)
            return

        try:
            cursor.execute(query)
        except Error as err:
            log().logger.error("Error executing query: %s", err, extra=self.extra)
            return

    @staticmethod
    def cursor_required(func: Callable) -> Callable:
        """Ensure there is a cursor available to run a SQL query."""

        @wraps(func)
        def wrapper(self, *args, **kwargs) -> list:  # noqa: ANN001,ANN002,ANN003
            """."""
            cursor = None
            try:
                cursor = self.connection.cursor()
                result = func(self, cursor, *args, **kwargs)
                cursor.close()
                return result
            except Error as err:
                log().logger.error(err)
                if cursor:
                    cursor.close()
                if not self.connection:
                    self.connect()
                raise

        return wrapper

    def fetch_all(self, cursor: Cursor) -> list:
        """."""
        return cursor.fetchall() if cursor else []

    @cursor_required
    def select(self, cursor: Cursor, query: str, **params) -> list:  # noqa:ANN003
        """."""
        self.execute_sql(cursor, query, **params)
        return self.fetch_all(cursor)
