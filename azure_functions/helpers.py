import pytz
import logging
import requests
import pandas as pd
from datetime import datetime

from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

from azure.storage.blob import BlobServiceClient


def send_request_with_retry(session, url, headers, params):
    retries = Retry(total=3, backoff_factor=1, status_forcelist=[500, 502, 503, 504])
    session.mount('https://', HTTPAdapter(max_retries=retries))
    response = session.get(url, headers=headers, params=params)
    return response

def fetch_jobs(job_search_url,job_search_headers,geo_codes,max_postings) -> pd.DataFrame:
    df_jobs = pd.DataFrame()
    with requests.Session() as session:
        for geo_code in geo_codes:
            for i in range(0, max_postings, 25):
                # querystring = {"geo_code":f"{geo_code}","date_posted":"any_time","title_id":"2732","sort_by":"most_recent","start":f"{i}","easy_apply":"false","under_10_applicants":"false"}
                querystring = {"geo_code":f"{geo_code}","date_posted":"past_24_hours","title_id":"2732","sort_by":"most_recent","start":f"{i}"}
                response = send_request_with_retry(session, job_search_url, job_search_headers, querystring)

                if response.status_code == 200:
                    data = response.json()['data']
                    df_temp = pd.DataFrame(data)
                    df_jobs = pd.concat([df_jobs, df_temp], ignore_index=True)
                    count = len(data)
                    if count < 25:
                        logging.info("There are less than 25 objects in the JSON data for geo: %s", geo_code)
                        break
                else:
                    logging.info("Error: %s for: %s", response.status_code, geo_code)
                    break

    if not df_jobs.empty:
        df_jobs['jobId'] = df_jobs['job_urn'].apply(lambda x: x[-10:])
        df_jobs = df_jobs.drop_duplicates(subset=['jobId'])
        df_jobs = df_jobs.sort_values(by='posted_time', ascending=False)
        df_jobs.reset_index(drop=True, inplace=True)
        aet_timezone = pytz.timezone('Australia/Sydney')
        current_date_aet = datetime.now(aet_timezone).date()
        df_jobs['fetched_date'] = current_date_aet
        logging.info("number of jobs fetched = %d", df_jobs.shape[0])
        return(df_jobs)
    else:
        logging.info('Empty list')
        return()

def fetch_job_detail(job_details_url,job_details_headers,df_jobId):
    job_details = []
    failed_job_urls = [] 
    logging.info("Fetching job details")
    with requests.Session() as session:
        for row in df_jobId:
            job_url = "https://www.linkedin.com/jobs/view/"+row
            querystring = {"job_url": job_url, "include_skills": "true"}
            response = send_request_with_retry(session, job_details_url, job_details_headers, querystring)
            if response.status_code == 200 and response.json() is not None:
                job_details.append(response.json()['data'])
                # logging.info("Fetched data for job URL: %s", job_url)
            else:
                failed_job_urls.append(job_url)
                logging.info("Failed to fetch data for job URL: %s", job_url)
        logging.info("Fetched all job details")
        
    df_job_det = pd.DataFrame(job_details)
    df_job_det = df_job_det.drop_duplicates(subset=['job_id'])
    df_job_det.reset_index(drop=True, inplace=True)

    aet_timezone = pytz.timezone('Australia/Sydney')
    current_date_aet = datetime.now(aet_timezone).strftime('%Y-%m-%d')
    df_job_det['fetched_date'] = current_date_aet

    df_failed_urls = pd.DataFrame({'job_url': failed_job_urls})
    df_failed_urls['fetched_date'] = current_date_aet
    logging.info("number of job details fetched = %d", df_job_det.shape[0])
    return(df_job_det,df_failed_urls)

def upload_df_to_blob_storage(df, blob_name, container_name, blob_service_client):
    # Determine file format based on the last letters of blob_name
    file_extension = blob_name.split('.')[-1].lower()
    if file_extension not in ['csv', 'json']:
        raise ValueError("Invalid file format. Supported formats are 'csv' and 'json'.")

    if file_extension == 'csv':
        data = df.to_csv(index=False)  # Convert DataFrame to CSV data
    elif file_extension == 'json':
        data = df.to_json(orient='records')  # Convert DataFrame to JSON data

    # Create a blob client using the local file name as the name for the blob
    blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)

    
    # Upload data to blob storage
    blob_client.upload_blob(data, overwrite=True)