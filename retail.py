from airflow.decorators import dag ,task
from datetime import datetime
from airflow.providers.google.cloud.transfers.local_to_gcs import LocalFilesystemToGCSOperator
from airflow.providers.google.cloud.operators.bigquery import BigQueryCreateEmptyDatasetOperator
from airflow.models.baseoperator import chain
from astro import sql as aql
from astro.files import File
from astro.sql.table import Table, Metadata
from astro.constants import FileType
from include.dbt.cosmos_config import DBT_PROJECT_CONFIG, DBT_CONFIG
from cosmos.airflow.task_group import DbtTaskGroup
from cosmos.constants import LoadMode
from cosmos.config import ProjectConfig, RenderConfig

@dag(
    start_date = datetime(2025,6,1),
    schedule = None,
    catchup = False,
    tags = ['retail']
)

def retail():
    upload_csv_gcp = LocalFilesystemToGCSOperator(
        task_id= 'upload_csv_gcp',
        src ='include/dataset/online_retail.txt',
        dst = 'raw/online_retail.csv',
        bucket = 'ahmedmarzouk-online-retail',
        gcp_conn_id = 'gcp',
        mime_type = 'text/csv',
        gzip = True
    )

    create_retail_dataset = BigQueryCreateEmptyDatasetOperator(
        task_id='create_retail_dataset',
        dataset_id='retail',
        gcp_conn_id='gcp',
    )
    gcs_to_raw = aql.load_file(
        task_id='gcs_to_raw',
        input_file=File(
            'gs://ahmedmarzouk-online-retail/raw/Online_Retail.txt',
            conn_id='gcp',
            filetype=FileType.CSV,
            
         
        ),
        output_table=Table(
            name='raw_invoices',
            conn_id='gcp',
            metadata=Metadata(schema='retail'),
           
        ),
        use_native_support=False,
        
    )

    @task.external_python(python='/usr/local/airflow/soda_venv/bin/python')
    def check_load(scan_name='check_load', checks_subpath='sources'):
        from include.soda.check_function import check

        return check(scan_name, checks_subpath)


    transform = DbtTaskGroup(
    group_id='transform',
    project_config=DBT_PROJECT_CONFIG,
    profile_config=DBT_CONFIG,
    render_config=RenderConfig(
        load_method=LoadMode.DBT_LS,
        select=['path:models/transform']
     
    )
)
    
    @task.external_python(python='/usr/local/airflow/soda_venv/bin/python')
    def check_transform(scan_name='check_transform', checks_subpath='transform'):
        from include.soda.check_function import check

        return check(scan_name, checks_subpath)
 

    report = DbtTaskGroup(
    group_id='report',
    project_config=DBT_PROJECT_CONFIG,
    profile_config=DBT_CONFIG,
    render_config=RenderConfig(
        load_method=LoadMode.DBT_LS,
        select=['path:models/report']
     
    )
)
    @task.external_python(python='/usr/local/airflow/soda_venv/bin/python')
    def check_report(scan_name='check_report', checks_subpath='report'):
        from include.soda.check_function import check

        return check(scan_name, checks_subpath)
    
    chain(upload_csv_gcp,
          create_retail_dataset,
          gcs_to_raw,
          check_load(),
          transform,
          check_transform(),
          report,
          check_report()
          )
    
   
retail()

