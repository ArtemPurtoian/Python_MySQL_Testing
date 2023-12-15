from utils.base_instance import BaseInstance
import datetime
"""
DB class - takes the config from the parent class.
Provides methods to operate within the DB.
"""


class CompanyDB(BaseInstance):
    def __init__(self):
        super().__init__()

    # Creating a table "employees" with 6 columns
    def create_table(self, table_name: str):
        self.cursor.execute(
            f"CREATE TABLE {table_name} "
            "(id INT AUTO_INCREMENT PRIMARY KEY, "
            "first_name VARCHAR(15) NOT NULL, "
            "last_name VARCHAR(15) NOT NULL, "
            "it_role VARCHAR(10) NOT NULL, "
            "email VARCHAR(50) NOT NULL, "
            "date_employed DATE NOT NULL);"
        )

    # Trigger - concatenates the first name and the last name into an email
    def create_trigger_generate_email(self, table_name: str):
        self.cursor.execute(f"""
                    CREATE TRIGGER generate_email
                    BEFORE INSERT ON {table_name}
                    FOR EACH ROW
                    BEGIN
                        DECLARE last_name_formatted VARCHAR(50);
                        SET last_name_formatted = REPLACE(LOWER(NEW.last_name), ' ', '_');
                        SET NEW.email = CONCAT(LOWER(NEW.first_name), '.',
                         last_name_formatted, '@it_company.com');
                    END;
            """)

    # Trigger - turns the first name and the last name into upper case
    def create_trigger_upper_names(self, table_name: str):
        self.cursor.execute(f"""    
                CREATE TRIGGER upper_names
                BEFORE INSERT on {table_name}
                FOR EACH ROW
                BEGIN
                    SET NEW.first_name = UPPER(NEW.first_name),
                        NEW.last_name = UPPER(NEW.last_name), 
                        NEW.it_role = UPPER(NEW.it_role); 
                END;
            """)

    # Inserting data with 7 rows into an empty table
    def insert_into_empty(self, table_name: str):
        insert = (
            f"INSERT INTO {table_name} (first_name, last_name, it_role, date_employed) "
            "VALUES (%s, %s, %s, %s);"
        )

        data_to_insert = [
            ('alex', 'stone', 'ceo', '2023-10-23'),
            ('bob', 'dylan', 'cto', '2023-10-23'),
            ('dolph', 'lundgren', 'qa', '2023-10-24'),
            ('sylvester', 'stallone', 'dev', '2023-10-24'),
            ('samantha', 'stevenson', 'hr', '2023-10-25'),
            ('john', 'travolta', 'recruiter', '2023-10-25'),
            ('robert', 'deniro', 'smm', '2023-10-26')
        ]
        self.cursor.executemany(insert, data_to_insert)

    def select_all(self, table_name: str) -> list:
        self.cursor.execute(f"SELECT * FROM {table_name};")
        select = self.cursor.fetchall()
        return select

    # Select query with a deliberate error for testing
    def select_all_with_error(self, table_name: str) -> list:
        self.cursor.execute(f"SELECT FROM {table_name};")
        select_with_error = self.cursor.fetchall()
        return select_with_error

    # Getting the number of columns
    def get_columns_count(self, table_name: str) -> int:
        self.cursor.execute(f"DESCRIBE {table_name};")
        columns = self.cursor.fetchall()
        columns_count = len(columns)
        return columns_count

    # Getting the data type of each column
    def get_column_type(self, table_name: str, column_name: str):
        self.cursor.execute(f"DESCRIBE {table_name}")
        columns = self.cursor.fetchall()

        column_type = None
        for column in columns:
            if column[0] == column_name:
                column_type = column[1]
                break

        return column_type

    # Getting the year next to the current
    @staticmethod
    def get_next_year():
        current_date = datetime.datetime.now()
        return current_date.year + 1

    # Extracting the year from the max employment date
    def select_date_employed_year(self, table_name: str) -> int:
        self.cursor.execute(f"SELECT EXTRACT(YEAR FROM (MAX(date_employed))) "
                            f"FROM {table_name};")
        max_date_employed = self.cursor.fetchone()
        year = max_date_employed[0]
        return year

    def insert_new_row(self, table_name: str):
        insert_new = self.cursor.execute(
            f"INSERT INTO {table_name} (first_name, last_name, it_role, "
            f"date_employed) "
            f"VALUES ('christopher', 'walken', 'pm', '2023-11-01');"
        )
        return insert_new

    """
    In MySQL deleting from a table using subqueries is restricted, so I create 
    a temporary table with only the maximum id of the rows which is the newly 
    inserted row so I can delete it after testing is completed.
    """
    def delete_new_row(self, table_name: str):
        self.cursor.execute(
            f"CREATE TEMPORARY TABLE temporary_table "
            f"SELECT MAX(id) as id_to_delete FROM {table_name};"
        )
        delete_new = self.cursor.execute(
            f"DELETE FROM {table_name} "
            f"WHERE id = (SELECT MAX(id_to_delete) FROM temporary_table)")
        self.cursor.execute("DROP TEMPORARY TABLE IF EXISTS temporary_table;")
        return delete_new
