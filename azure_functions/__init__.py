import pytz
import logging
import requests
import pandas as pd
from datetime import datetime
import azure.functions as func

from azure.storage.blob import BlobServiceClient

from .helpers import send_request_with_retry,fetch_jobs,fetch_job_detail,upload_df_to_blob_storage


# def main(req: func.HttpRequest) -> func.HttpResponse:
def main(mytimer: func.TimerRequest) -> None:
    logging.info('Python HTTP trigger function processed a request.')
    
    #Azure uploading blob
    sas_token = 
    account_url = 

    # Create the BlobServiceClient object
    service_client = BlobServiceClient(account_url=account_url,credential=sas_token)

    job_search_url = 
    job_search_headers = 

    job_details_url = 
    job_details_headers =

    geo_codes = 
    max_postings = 250
    aet_timezone = pytz.timezone('Australia/Sydney')
    current_date = datetime.now(aet_timezone).date().strftime('%Y-%m-%d')

    #Jobs fetched
    df_jobs = fetch_jobs(job_search_url,job_search_headers,geo_codes,max_postings)
    filename_fetched = f"jobs_fetched_{current_date}.csv"
    jp_container = "raw/raw-job-postings"
    
    if df_jobs is not None:
        # Upload df_jobs to a container named "container1"
        upload_df_to_blob_storage(df_jobs, filename_fetched, jp_container, service_client)

        # Job details fetched and failed URLs 
        df_jobId = df_jobs['jobId']

        df_job_det,df_failed_urls = fetch_job_detail(job_details_url,job_details_headers,df_jobId)

        filename_details = f"jobs_details_fetched_{current_date}.json"
        jd_container = "raw/raw-job-details"

        filename_failed_jobs = f"failed_job_urls_{current_date}.csv"
        fj_container = "failed-job-urls"

        # Upload df_job_det to a container named "container2"
        upload_df_to_blob_storage(df_job_det, filename_details, jd_container , service_client)

        # Upload df_failed_urls to a container named "container3"
        upload_df_to_blob_storage(df_failed_urls, filename_failed_jobs, fj_container, service_client)

        logging.info("This time triggered function executed successfully. Pass check data lake for a response.")
    else:
        logging.info("This HTTP triggered function wasnt executed successfully.")
