# Importing the required libraries
from datetime import datetime
from airflow.operators.python_operator import PythonOperator
from airflow import DAG
from airflow.utils.trigger_rule import TriggerRule
from airflow.hooks.base_hook import BaseHook
from airflow.contrib.operators.slack_webhook_operator import SlackWebhookOperator
from random import random

# retrieves the Slack connection details from Airflow's Connection feature and sets them to the variables
SLACK_CONN_ID="Slack_connection" # defines a connection identifier 
slack_webhook_token = BaseHook.get_connection(SLACK_CONN_ID).password # retrieves the connection details for the Slack_connection connection from Airflow's Connection feature.
channel = BaseHook.get_connection(SLACK_CONN_ID).login

# Declaring default arguments for the dag
default_args = {
    'owner' :'admin'
    }

# function which fails sometimes when the randomly generated number is less than 0.5
def random_fail():
    num = random()
    if num < 0.5:
        raise ValueError(f"Random number {num} is less than 0.5!")
    else:
        print(f"Random number {num} is greater than or equal to 0.5!")

# Creating a dag and creating tasks in them
with DAG(
    dag_id="slack_sending",
    start_date=datetime(2023,4,21),
    default_args=default_args,
    schedule="@daily",
    catchup=False,
) as dag:
    # Creating a task fails some time
    task1 = PythonOperator(
        task_id='random_fail',
        python_callable=random_fail,
        dag=dag
    )
    # Creating success message task in slack, which triggers on success of above task using trigger rule
    task2 = SlackWebhookOperator(
        task_id='slack_success',
        webhook_token=slack_webhook_token,
        message='Task succeded',
        channel=channel,
        username='airflow',
        http_conn_id=SLACK_CONN_ID,
        trigger_rule=TriggerRule.ALL_SUCCESS
    )
    # Creating success message task in slack, which triggers on fail of above task using trigger rule
    task3 = SlackWebhookOperator(
        task_id='slack_fail',
        webhook_token=slack_webhook_token,
        message='Task Failed',
        channel=channel,
        username='airflow',
        http_conn_id=SLACK_CONN_ID,
        trigger_rule=TriggerRule.ALL_FAILED
    )

    # Declaring dependencies of the task.
    task1 >> [task2,task3]