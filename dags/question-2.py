from datetime import datetime
from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.email_operator import EmailOperator

default_args = {
    'owner': 'sigmoid',
    'depends_on_past': False,
    'start_date': datetime(2023, 4, 25),
    'retries': 1
}

dag = DAG('sigmoid_email_alert', default_args=default_args, schedule_interval='@daily')

dummy_task = DummyOperator(
    task_id='dummy_task',
    dag=dag
)

email_task = EmailOperator(
    task_id='email_task',
    to='sonali.g@sigmoidanalytics.com',
    subject='Dummy task completed successfully',
    html_content='The dummy task has completed successfully.',
    dag=dag
)

dummy_task >> email_task