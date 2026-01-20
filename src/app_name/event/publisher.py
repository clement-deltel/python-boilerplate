"""Module used to publish log messages to RabbitMQ.

Typical usage example:
    publisher = AMQPPublisher()
    publisher.connect()
    publisher.publish_message(log_message)
    publisher.close()
"""

# Standard Library
from threading import RLock
from time import sleep

# Third-party
import pika
from pika.exceptions import AMQPChannelError, AMQPConnectionError, ConnectionClosedByBroker

# Local Application
from app_name.common.config import AMQPConfig, get_config_class
from app_name.event.logger.amqp import log


class AMQPPublisher:
    """AMQP Publisher class for publishing log messages to RabbitMQ.

    This class handles RabbitMQ connections, channel management, and message publishing
    with automatic reconnection and error recovery capabilities.
    """

    def __init__(self) -> None:
        """Initialize class."""
        self.config: AMQPConfig = get_config_class("amqp")
        self._lock = RLock()  # Reentrant lock for thread safety

        self._connection = None
        self._channel = None
        self._is_connected = False

        # Reconnection parameters
        self._reconnect_attempts = 0
        self._max_reconnect_attempts = 5
        self._reconnect_delay = 5

        # Performance optimization
        self._delivery_mode = pika.DeliveryMode.Persistent if self.config.message_persistent else pika.DeliveryMode.Transient
        self._properties = pika.BasicProperties(delivery_mode=self._delivery_mode)

        self._connection_parameters = self._get_connection_parameters()

        self.extra = {"host": self._connection_parameters.host, "exchange": self.config.exchange}

    def _get_connection_parameters(self) -> pika.ConnectionParameters:
        """Get RabbitMQ connection parameters from config.

        Returns:
            pika.ConnectionParameters: Connection parameters for RabbitMQ.
        """
        return pika.ConnectionParameters(
            host=self.config.hostname,
            port=self.config.port,
            virtual_host=self.config.virtual_host,
            credentials=pika.PlainCredentials(username=self.config.username, password=self.config.password),
            heartbeat=self.config.heartbeat,
            connection_attempts=self.config.connection_attempts,
            retry_delay=self.config.retry_delay,
            socket_timeout=self.config.socket_timeout,
            blocked_connection_timeout=self.config.blocked_connection_timeout,
        )

    def connect(self) -> bool:
        """Establish connection to RabbitMQ and set up channel.

        Returns:
            bool: True if connection successful, False otherwise.
        """
        with self._lock:
            if self._is_connected and self._connection and not self._connection.is_closed:
                return True

            try:
                # Close existing connection if any
                self._close_connection()

                # Establish new connection
                log().logger.debug("Connecting to RabbitMQ...", extra=self.extra)
                self._connection = pika.BlockingConnection(self._connection_parameters)
                self._channel = self._connection.channel()

                # Declare exchange
                self._channel.exchange_declare(exchange=self.config.exchange, exchange_type=self.config.exchange_type, durable=self.config.exchange_durable)

                self._is_connected = True
                self._reconnect_attempts = 0

            except (AMQPConnectionError, ConnectionClosedByBroker) as err:
                log().logger.error("Failed to connect to RabbitMQ: %s", err, extra=self.extra)
                self._is_connected = False
            except Exception as err:
                log().logger.error("Unexpected error during RabbitMQ connection: %s", err, extra=self.extra)
                self._is_connected = False

            return self._is_connected

    def _reconnect(self) -> bool:
        """Attempt to reconnect to RabbitMQ with exponential backoff.

        Returns:
            bool: True if reconnection successful, False otherwise.
        """
        if self._reconnect_attempts >= self._max_reconnect_attempts:
            log().logger.error("Max reconnection attempts (%s) exceeded", self._max_reconnect_attempts, extra=self.extra)
            return False

        delay = min(self._reconnect_delay * (2 ** (self._reconnect_attempts - 1)), 60)
        log().logger.info(
            "Attempting to reconnect to RabbitMQ in %s seconds...(%s/%s)", delay, self._reconnect_attempts, self._max_reconnect_attempts, extra=self.extra
        )
        sleep(delay)

        self._reconnect_attempts += 1
        return self.connect()

    def is_connected(self) -> bool:
        """Check if the publisher is connected to RabbitMQ.

        Returns:
            bool: True if connected and channel is open, False otherwise.
        """
        with self._lock:
            return self._is_connected and self._connection and not self._connection.is_closed and self._channel and not self._channel.is_closed

    def _close_connection(self) -> None:
        """Close the RabbitMQ connection and channel safely."""
        try:
            if self._channel and not self._channel.is_closed:
                self._channel.close()
        except Exception as err:
            log().logger.error("Error closing channel: %s", err, extra=self.extra)
        finally:
            self._channel = None

        try:
            if self._connection and not self._connection.is_closed:
                self._connection.close()
        except Exception as err:
            log().logger.error("Error closing connection: %s", err, extra=self.extra)
        finally:
            self._connection = None
            self._is_connected = False

    def close(self) -> None:
        """Close the AMQP connection and cleanup resources."""
        with self._lock:
            self._close_connection()
        log().close()

    def publish_message(self, message: str) -> bool:
        """Publish a log message to RabbitMQ.

        Args:
            message (str): message to publish.

        Returns:
            bool: True if message published successfully, False otherwise.
        """
        # Ensure we have a connection
        if not self.is_connected() and not self.connect() and not self._reconnect():
            return False

        try:
            with self._lock:
                # Double-check connection after acquiring lock
                if not self.is_connected() and not self.connect():
                    return False

                # Publish message
                self._channel.basic_publish(
                    exchange=self.config.exchange, routing_key=self.config.routing_key, body=message.encode("utf-8"), properties=self._properties
                )

                return True

        except (AMQPConnectionError, AMQPChannelError, ConnectionClosedByBroker) as err:
            log().logger.warning("AMQP connection error during publish: %s. Attempting reconnection.", err, extra=self.extra)
            self._is_connected = False
            # Try to reconnect and republish once
            if self._reconnect():
                return self.publish_message(message)
            return False

        except Exception as err:
            log().logger.error("Unexpected error during message publish: %s", err, extra=self.extra)
            return False
