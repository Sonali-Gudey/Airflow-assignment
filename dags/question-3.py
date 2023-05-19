from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.utils.trigger_rule import TriggerRule
from airflow.contrib.operators.slack_webhook_operator import SlackWebhookOperator
from airflow.hooks.base_hook import BaseHook

from random import *

SLACK_CONN_ID="slack_connection" # defines a connection identifier 
slack_webhook_token = BaseHook.get_connection(SLACK_CONN_ID).password # retrieves the connection details for the Slack_connection connection from Airflow's Connection feature.
channel = BaseHook.get_connection(SLACK_CONN_ID).login

# Define the default arguments for the DAG
default_args = {
    'owner': 'airflow'
}

# function which fails sometimes when the randomly generated number is less than 0.5
def check_even():
    num = randint(1, 10)
    if num % 2 != 0:
        raise ValueError(f"Random number {num} is not a Even number!")
    else:
        print(f"Random number {num} is a Even number!")

# Creating a dag and creating tasks in them
with DAG(
    dag_id="slack_alert",
    start_date=datetime(2023,4,21),
    default_args=default_args,
    schedule_interval='@daily',
    catchup=False,
) as dag:
    # Creating a task fails some time
    task1 = PythonOperator(
        task_id='check_even',
        python_callable=check_even,
        dag=dag
    )
    # Creating success message task in slack, which triggers on success of above task using trigger rule
    task2 = SlackWebhookOperator(
        task_id='slack_success_alert',
        webhook_token=slack_webhook_token,
        message='Task succeded',
        channel=channel,
        username='airflow',
        http_conn_id=SLACK_CONN_ID,
        trigger_rule=TriggerRule.ALL_SUCCESS
    )
    # Creating success message task in slack, which triggers on fail of above task using trigger rule
    task3 = SlackWebhookOperator(
        task_id='slack_fail_alert',
        webhook_token=slack_webhook_token,
        message='Task Failed',
        channel=channel,
        username='airflow',
        http_conn_id=SLACK_CONN_ID,
        trigger_rule=TriggerRule.ALL_FAILED
    )

    # Declaring dependencies of the task.
    task1 >> [task2,task3]

