import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from pyspark.sql import SparkSession
from pyspark.sql.functions import col

# Initialize a Spark session
sc = SparkContext()
spark = SparkSession(sc)

# Get Glue job arguments and parameters
args = getResolvedOptions(sys.argv, ['JOB_NAME', 'SRC_BUCKET', 'SRC_KEY', 'DEST_BUCKET', 'DEST_KEY'])

# Read the CSV file from the source S3 bucket
src_bucket = args['SRC_BUCKET']
src_key = args['SRC_KEY']
s3_source_path = f's3://{src_bucket}/{src_key}'
df = spark.read.csv(s3_source_path, header=True, inferSchema=True)

# Perform a simple transformation (e.g., remove rows with null values)
df_transformed = df.filter(col('column_name').isNotNull())  # Replace 'column_name' with your actual column name

# Write the transformed DataFrame back to the destination S3 bucket
dest_bucket = args['DEST_BUCKET']
dest_key = args['DEST_KEY']
s3_dest_path = f's3://{dest_bucket}/{dest_key}'
df_transformed.write.csv(s3_dest_path, mode='overwrite', header=True)

# Stop the Spark session
spark.stop()
