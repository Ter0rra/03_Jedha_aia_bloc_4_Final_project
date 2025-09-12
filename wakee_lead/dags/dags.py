from datetime import datetime
import os
from airflow import DAG
from airflow.operators.bash_operator import BashOperator


default_args = {
    "owner": "airflow",
    "start_date": datetime(2025, 1, 1),
    'retries': 1,
    # 'schedule_interval': "@daily"
}


with DAG(dag_id="Daily_img_transfer", default_args=default_args, schedule_interval="@daily", catchup=False) as dag:
    start_dag = BashOperator(task_id="start_dag", bash_command="echo 'Start!'")

    move_images = BashOperator(task_id="move_images", bash_command='''
                                pwd
                                ls
                                cd ../../opt/airflow
                                pwd
                                ls
                                mv src/temp/*.jpg data/raw_images
                                ''')
                               
    end_dag = BashOperator(task_id="end_dag", bash_command="echo 'End!'")

    start_dag >>  move_images >> end_dag