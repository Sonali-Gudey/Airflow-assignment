# Airflow-assignment

### Question-1: Create Dags to perform the following tasks:
#### a. Task to create a simple table.

```
create_table_sql = """
    CREATE TABLE IF NOT EXISTS sample_table (
    name VARCHAR(50),
    age INTEGER,
    email VARCHAR(100)
);

create_table_task = PostgresOperator(
    task_id='create_table',
    postgres_conn_id='postgres_conn',
    sql=create_table_sql,
    dag=dag,
)
```

#### b. Task to insert few custom values in to the created table in previous step.

```
insert_values_sql = """
    INSERT INTO sample_table (name, age, email) VALUES
    ('Sonali', 21, 'sonali@gmail.com'),
    ('Anusha', 25, 'anshu@gmail.com'),
    ('Suhani', 45, 'suhani@gmail.com');
"""

insert_values_task = PostgresOperator(
    task_id='insert_values',
    postgres_conn_id='postgres_conn',
    sql=insert_values_sql,
    dag=dag,
)
```

#### c. Task to select the values from the table.

```
select_values_sql = """
    SELECT * FROM sample_table;
"""

select_values_task = PostgresOperator(
    task_id='select_values',
    postgres_conn_id='postgres_conn',
    sql=select_values_sql,
    dag=dag,
)
```

#### Connection is created in airflow UI between postgres and airflow.

<img width="1440" alt="Screenshot 2023-05-18 at 5 57 46 PM" src="https://github.com/Sonali-Gudey/Airflow-assignment/assets/123619701/b6985947-78fa-4fbc-b727-a832b2ce21db">


#### Dependency flow

```
create_table_task >> insert_values_task >> select_values_task
```


<img width="1440" alt="Screenshot 2023-05-18 at 5 21 25 PM" src="https://github.com/Sonali-Gudey/Airflow-assignment/assets/123619701/fe3a7172-4209-4976-b59d-71c4810e964e">

<img width="1334" alt="Screenshot 2023-05-18 at 5 51 25 PM" src="https://github.com/Sonali-Gudey/Airflow-assignment/assets/123619701/578aae08-608d-4a71-a8e4-eb45e9baf229">


### Question-2:  Create a dag with following tasks:
#### a. A dummy task which always succeeds.


```
dummy_task = DummyOperator(
    task_id='dummy_task',
    dag=dag
)
```


#### b. Upon successful completion of the task your setup of airflow environment should be such that it sends an email alert to your sigmoid mail id.


```
email_task = EmailOperator(
    task_id='email_task',
    to='sonali.g@sigmoidanalytics.com',
    subject='Dummy task completed successfully',
    html_content='The dummy task has completed successfully.',
    dag=dag
)
```

#### Dependency flow

```
dummy_task >> email_task
```

<img width="1440" alt="Screenshot 2023-05-18 at 5 59 45 PM" src="https://github.com/Sonali-Gudey/Airflow-assignment/assets/123619701/b5cf2d59-38c3-46c6-93c6-873061ca891f">

![5A03E41B-7080-4678-8575-2B044F9527BF_1_201_a](https://github.com/Sonali-Gudey/Airflow-assignment/assets/123619701/1b22e585-4b5d-43f2-9f5f-7adda16270fe)


### Question-3:  Create a dag with following tasks:

#### a. A dummy task which can succeed/fail.

```
# Creating a task which fails sometimes
    task1 = PythonOperator(
        task_id='check_even',
        python_callable=check_even,
        dag=dag
    )
```

#### b. Upon success/failure send an alert message to slack workspace.

```
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
```

#### Dependency flow

```
 task1 >> [task2,task3]
```

![image](https://github.com/Sonali-Gudey/Airflow-assignment/assets/123619701/47bff2bc-9d40-42be-8985-e1ea7e65ca88)


<img width="1386" alt="Screenshot 2023-05-18 at 6 41 11 PM" src="https://github.com/Sonali-Gudey/Airflow-assignment/assets/123619701/0c21f77b-beaa-44e5-a8b4-44f24f1f5eb8">

#### 1. Initially slack channel is created. Using Slack API one app is created with activated incoming webhooks.
#### 2. In airflowUI connection is created for slack.


<img width="1386" alt="Screenshot 2023-05-19 at 11 21 02 AM" src="https://github.com/Sonali-Gudey/Airflow-assignment/assets/123619701/f06b9675-b186-4766-99e4-9199912d93a1">


#### 3. When the task fails or succeeds it sends slack notification using SlackWebhookHook.

![image](https://github.com/Sonali-Gudey/Airflow-assignment/assets/123619701/7b259790-f9c7-4fca-9564-5c44dfdaca6e)


















