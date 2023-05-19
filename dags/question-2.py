# Importing the required libraries
from datetime import datetime,timedelta
from airflow import DAG
from airflow.operators.empty import EmptyOperator
from airflow.operators.email import EmailOperator

# Declaring time and message for content in mail.
time_now = datetime.now() 
message = (f"<h3> Hello Chakradhar</h3>, This mail is sent from airflow, Given scheduled Task is completed at {time_now} .")

# Declaring default arguments for the dag
default_args = {
    'owner' :'admin',
    'retries': 5,
    'retry_delay' : timedelta(minutes=5)
}

# Creating a dag and creating tasks in them
with DAG(
    dag_id="email_sending",
    start_date=datetime(2023,4,21),
    default_args=default_args,
    schedule="@daily",
    catchup=False,
) as dag:
    # Task1 - which never fails, i.e dummy task
    task1=EmptyOperator(
        task_id="Dummy"
    )
    # Task2 - for sending success message of the task to below mail with above message
    task2=EmailOperator(
        task_id="Sending_Email",
        to="csrinivas@sigmoidanalytics.com",
        subject="Success Message",
        html_content=message
    )
    # Declaring dependencies of the task.
    task1>>task2