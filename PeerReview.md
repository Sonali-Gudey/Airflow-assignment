## Peer Learning

### Shubham's approach:

#### Question-1:

1. First he defined a task in Apache Airflow that uses the PostgresOperator to execute a SQL statement for creating a table named EMP in a PostgreSQL database. 
2. When the task is executed as part of an Airflow DAG, the table will be created if it doesn't already exist.
3. Then he defined a task in Apache Airflow that uses the PostgresOperator to execute an SQL statement for inserting data into a table named EMP in a PostgreSQL database. 
4. The task inserts multiple rows of data into the table with specified values for the columns name, profession, birth_date, and friend.
5. Next he defined a task in Apache Airflow that uses the PostgresOperator to execute an SQL query to retrieve all records from the EMP table in a PostgreSQL database. 
6. The task retrieves the data and returns the result set containing all columns and rows from the table.


### Question-2:

1. First he created a DAG, the DAG includes a DummyOperator named t1, which represents a placeholder task with no actual functionality.
2. Then he defined an EmailOperator task named t2 in the Airflow DAG. This task sends an email with the subject "Alert Mail" and the HTML content "Mail Test" to the recipient specified in the to parameter. The task is part of the dag DAG.


### Question-3:

1. In the code he defined a PythonOperator task named t1 in the Airflow DAG. This task calls the my_function function as the python_callable. 
2. Inside the function, a random number between 1 and 2 is generated. If the number is 1, it raises an AirflowException with the message "This is a test exception". Otherwise, it prints "Success". The task is part of the dag DAG.
3. slack_success is responsible for sending a Slack message with the content "Successful dag run" to the specified channel when all preceding tasks in the DAG complete successfully (TriggerRule.ALL_SUCCESS).
4. slack_failed is responsible for sending a Slack message with the content "Failed dag run" to the specified channel when any preceding task in the DAG fails (TriggerRule.ALL_FAILED).
5. Both tasks use the same Slack webhook token and Slack connection ID to authenticate and send messages to the Slack channel. The username "airflow" is used as the sender of the messages.
