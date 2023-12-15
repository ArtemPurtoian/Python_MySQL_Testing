import configparser


parser = configparser.ConfigParser()
parser.read("./configs/config.ini")


"""
Class - reads the config.ini file and provides static methods to get 
each parameter.
"""


class ReadConfig:
    @staticmethod
    def get_db_config():
        db_config = dict(parser.items("db_configuration"))
        return db_config

    @staticmethod
    def get_host_name():
        host_name = ReadConfig.get_db_config().get("host_name")
        return host_name

    @staticmethod
    def get_user_name():
        user_name = ReadConfig.get_db_config().get("user_name")
        return user_name

    @staticmethod
    def get_password():
        password = ReadConfig.get_db_config().get("password")
        return password

    @staticmethod
    def get_autocommit():
        autocommit = ReadConfig.get_db_config().get("autocommit")
        return bool(autocommit)

    @staticmethod
    def get_database_name():
        database_name = ReadConfig.get_db_config().get("database_name")
        return database_name

    @staticmethod
    def get_table_name():
        table_name = ReadConfig.get_db_config().get("table_name")
        return table_name
