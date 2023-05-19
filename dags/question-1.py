from datetime import datetime, timedelta
from airflow import DAG
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2023, 4, 20),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'postgres_dag',
    default_args=default_args,
    description='A DAG that creates a table, inserts values, and selects values from PostgreSQL',
    schedule_interval=timedelta(days=1),
)

create_table_sql = """
    CREATE TABLE IF NOT EXISTS sample_table (
    name VARCHAR(50),
    age INTEGER,
    email VARCHAR(100)
);
"""

insert_values_sql = """
    INSERT INTO sample_table (name, age, email) VALUES
    ('Sonali', 21, 'sonali@gmail.com'),
    ('Anusha', 25, 'anshu@gmail.com'),
    ('Suhani', 45, 'suhani@gmail.com');
"""

select_values_sql = """
    SELECT * FROM sample_table;
"""

create_table_task = PostgresOperator(
    task_id='create_table',
    postgres_conn_id='postgres_conn',
    sql=create_table_sql,
    dag=dag,
)

insert_values_task = PostgresOperator(
    task_id='insert_values',
    postgres_conn_id='postgres_conn',
    sql=insert_values_sql,
    dag=dag,
)

select_values_task = PostgresOperator(
    task_id='select_values',
    postgres_conn_id='postgres_conn',
    sql=select_values_sql,
    dag=dag,
)

create_table_task >> insert_values_task >> select_values_task