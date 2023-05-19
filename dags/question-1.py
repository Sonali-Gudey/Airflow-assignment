# Importing the required libraries
from datetime import datetime
from airflow import DAG
from airflow.providers.snowflake.operators.snowflake import SnowflakeOperator

# Declaring the varibales
SNOWFLAKE_CONN_ID = "snowflake_connection"
SNOWFLAKE_SAMPLE_TABLE = "employee_data_table"
SNOWFLAKE_DATABASE = "employee_data"
SNOWFLAKE_SCHEMA="employee_data_schema"

# Declaring the SQL strings
# SQL query to use the created database
USING_SNOWFLAKE_DATABASE_SQL_STRING = (
    f"use database {SNOWFLAKE_DATABASE}"
)
# SQL query to use the created schema
USING_SNOWFLAKE_SCHEMA_SQL_STRING = (
    f"use schema {SNOWFLAKE_SCHEMA}"
)
# SQL query to creat a table
CREATE_TABLE_SQL_STRING = (
    f"CREATE OR REPLACE TABLE {SNOWFLAKE_SAMPLE_TABLE} (id INT,first_name VARCHAR(250),last_name VARCHAR(250),address VARCHAR(250));"
)
# SQL query to insert values into above created table
INSERT_TO_TABLE_SQL_STRING = (
    f"INSERT INTO {SNOWFLAKE_SAMPLE_TABLE} values(1,'Chakradhar','Srinvias','Ongole'),(2,'Atul','Reddy','Banglore'),(3,'Arjun','Reddy','Hyderabad'),(4,'Rocky','Bhai','KGF');"
)
# SQL query to select from created tables
SELECT_TABLE_SQL_STRING = (
    f"SELECT * FROM {SNOWFLAKE_SAMPLE_TABLE};"
)

# Creating a dag and creating tasks in them
with DAG(
    dag_id="querying_snowflake",
    start_date=datetime(2023,4,21 ),
    default_args={"snowflake_conn_id": SNOWFLAKE_CONN_ID},
    schedule="@daily",
    catchup=False,
) as dag:
    task1 = SnowflakeOperator(task_id="using_snowflake_database", sql=USING_SNOWFLAKE_DATABASE_SQL_STRING) # task1 - for using created database
    task2 = SnowflakeOperator(task_id="using_snowflake_schema", sql=USING_SNOWFLAKE_SCHEMA_SQL_STRING) # task2 - for using created schema
    task3 = SnowflakeOperator(task_id="create_table", sql=CREATE_TABLE_SQL_STRING) # task3 - for creation of table
    task4 = SnowflakeOperator(task_id="Insert_data", sql=INSERT_TO_TABLE_SQL_STRING) # task4 - for inserting into table
    task5 = SnowflakeOperator(task_id="Select_data", sql=SELECT_TABLE_SQL_STRING) # task5 - for selecting data from the table
    
    # Declaring dependencies of the task.
    task1>>task2>>task3>>task4>>task5 