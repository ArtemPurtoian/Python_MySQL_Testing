import pytest
from databases.company_db import CompanyDB
from utils.config_reader import ReadConfig

"""
Fixture - provides the config of the "company" DB to the tests and closes
connection after a test execution.
"""


@pytest.fixture
def company_database():
    company_db = CompanyDB()
    company_db.use_database(ReadConfig.get_database_name())
    yield company_db
    company_db.close_connection()
