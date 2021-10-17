"""
Author: Jacob Levy
This dag orchestrates and schedules the process of scraping the Epic Games Store 
for free games and reporting any new ones to a Discord server
"""
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime


from tasks.EGS_Scraper_Tasks.EGS_Scraper import scrape_data
from tasks.EGS_Scraper_Tasks.Embed_Poster import start_bot

#Setting up our default arguments.
default_args = {
    'owner': 'jlevy0',
    'start_date': datetime(2021, 10, 10),
    'retries':1
}

with DAG('EGS_Scraper', 
    default_args=default_args,
    schedule_interval= '0 12 * * *',
    catchup = False
    ) as dag:
    Scrape_Epic_Games_Store = PythonOperator(
        task_id='scrapeData',
        python_callable=scrape_data)

    Post_Embed_Data = PythonOperator(
        task_id='postEmbed',
        python_callable=start_bot)

Scrape_Epic_Games_Store >> Post_Embed_Data