import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions
from apache_beam.options.pipeline_options import GoogleCloudOptions
from apache_beam.options.pipeline_options import StandardOptions
from apache_beam.io.iobase import Write
from apache_beam.transforms import PTransform
import apache_beam as beam
from apache_beam.io.gcp.bigquery import parse_table_schema_from_json
from datetime import datetime
import time

def main():
    options = PipelineOptions(region='us-central1')
    google_cloud_options = options.view_as(GoogleCloudOptions)
    google_cloud_options.project = 'springer-nature-analytics'
    google_cloud_options.job_name = 'container'
    google_cloud_options.staging_location = 'gs://cloud-dataflow-etl/staging'
    google_cloud_options.temp_location = 'gs://cloud-dataflow-etl/temp'
    # options.view_as(SetupOptions).save_main_session = True
    options.view_as(StandardOptions).runner = 'DataflowRunner'
    folder_name=datetime.now().strftime("%Y-%m-%d")
    gcs_loc='gs://sandbox_data_engineering/sangam_test/container/'

    query_API_4="""SELECT * FROM `springer-nature-analytics.dataeng_sandbox.ni_full_refresh`"""

    bq_source_API_4 = beam.io.ReadFromBigQuery (query=query_API_4, use_standard_sql=True)
    
    with beam.Pipeline(options=options) as p:

        API4 = p | " READING API4 from BQ" >> beam.io.Read(bq_source_API_4)|"writing api4">>beam.io.WriteToText(gcs_loc,file_name_suffix='.json',num_shards=100)
        

if __name__ == "__main__":
    main()
