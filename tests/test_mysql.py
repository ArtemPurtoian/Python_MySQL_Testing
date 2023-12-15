import pytest
from mysql.connector.errors import ProgrammingError
from utils.config_reader import ReadConfig


# The correctness of the SELECT query response
def test_select_positive(company_database):
    table_name = ReadConfig.get_table_name()
    select = company_database.select_all(table_name)

    assert len(select) == 7, f"The number of table records is incorrect!"


# Negative case - the SELECT query is incorrect
def test_select_negative_query(company_database):
    table_name = ReadConfig.get_table_name()

    with pytest.raises(ProgrammingError,
                       match="You have an error in your SQL syntax;"):
        company_database.select_all_with_error(table_name)


# Negative case - the number of rows is incorrect
def test_select_negative_len(company_database):
    table_name = ReadConfig.get_table_name()
    select = company_database.select_all(table_name)

    with pytest.raises(AssertionError):
        assert len(select) != 7


# The number of columns in a table
def test_columns_count(company_database):
    table_name = ReadConfig.get_table_name()
    columns_count = company_database.get_columns_count(table_name)
    assert columns_count == 6, \
        "The number of columns is incorrect!"


# The type of the specified columns in a table
@pytest.mark.parametrize("column_name, expected_column_type",
                         [("id", "int"),
                          ("first_name", "varchar(15)"),
                          ("last_name", "varchar(15)"),
                          ("it_role", "varchar(10)"),
                          ("email", "varchar(50)"),
                          ("date_employed", "date")])
def test_column_type(company_database, column_name, expected_column_type):
    table_name = ReadConfig.get_table_name()
    column_type = company_database.get_column_type(table_name, column_name)

    assert column_type == expected_column_type, \
        f"The column type is not {expected_column_type}"


# The format of the email addresses corresponds to the enterprise domain name
def test_email_format(company_database):
    table_name = ReadConfig.get_table_name()
    select = company_database.select_all(table_name)
    for column in select:
        assert (column[4] ==
                (column[1] + "." + column[2] + "@it_company.com").lower()), \
            "Email has incorrect format!"


# The year of employment is not higher than the current year
def test_date_employed_year(company_database):
    table_name = ReadConfig.get_table_name()
    year_from_mysql = company_database.select_date_employed_year(table_name)
    next_year = company_database.get_next_year()
    assert year_from_mysql < next_year, \
        f"Year {year_from_mysql} is higher than the current year."


# The number of records after INSERT query. Delete inserted data after the test
def test_insert_len(company_database):
    table_name = ReadConfig.get_table_name()
    first_select = company_database.select_all(table_name)
    company_database.insert_new_row(table_name)
    select_after_insert = company_database.select_all(table_name)

    assert len(select_after_insert) == len(first_select) + 1, \
        f"The number of records is incorrect - {len(select_after_insert)}!"
    company_database.delete_new_row(table_name)


# The correctness of the inserted data: name + surname -> name.surname@email
def test_insert_data_format(company_database):
    table_name = ReadConfig.get_table_name()
    company_database.insert_new_row(table_name)
    select_after_insert = company_database.select_all(table_name)

    assert (select_after_insert[-1][4] ==
            (select_after_insert[-1][1] +
             "." +
             select_after_insert[-1][2] + "@it_company.com").lower())
    company_database.delete_new_row(table_name)
