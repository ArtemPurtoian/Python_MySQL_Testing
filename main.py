"""
Run this script in the first place to create a local DB!
"""
from utils.config_reader import ReadConfig
from databases.company_db import CompanyDB


company = CompanyDB()
company.create_database(ReadConfig.get_database_name())
company.use_database(ReadConfig.get_database_name())
company.create_table(ReadConfig.get_table_name())
company.create_trigger_generate_email(ReadConfig.get_table_name())
company.create_trigger_upper_names(ReadConfig.get_table_name())
company.insert_into_empty(ReadConfig.get_table_name())

select = company.select_all(ReadConfig.get_table_name())
for row in select:
    print(row)
