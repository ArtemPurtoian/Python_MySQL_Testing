import mysql.connector
from utils.config_reader import ReadConfig


# Class - takes the config and initializes connection for inheritance
class BaseInstance:
    def __init__(self):
        # Initializing connection
        self._connection = (
            mysql.connector.connect(
                host=ReadConfig.get_host_name(),
                user=ReadConfig.get_user_name(),
                password=ReadConfig.get_password(),
                autocommit=ReadConfig.get_autocommit()
            )
        )
        self.cursor = self._connection.cursor()

    # Connection closing method to use in a fixture
    def close_connection(self):
        if self._connection:
            if self.cursor:
                self.cursor.close()
            self._connection.close()

    def create_database(self, database_name: str):
        self.cursor.execute(f"CREATE DATABASE IF NOT EXISTS {database_name};")

    def use_database(self, database_name: str):
        self.cursor.execute(f"USE {database_name};")

    def drop_database(self, database_name: str):
        self.cursor.execute(f"DROP DATABASE {database_name};")
