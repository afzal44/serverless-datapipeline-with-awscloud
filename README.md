# Building an End-to-End Data Pipeline with AWS Serverless Services

* Introduction 

In today's data-driven world, organizations rely on efficient data pipelines to collect, process, and analyze data. AWS offers a powerful suite of serverless services that allow you to build scalable and cost-effective data pipelines. In this blog post, we will walk you through the steps of creating a data pipeline using AWS serverless services, from ingesting raw data to performing advanced analytics.BLOG Link : https://www.qloudx.com/building-scalable-data-pipelines-with-aws-serverless-services-part-2/

## Architecture Diagram

![image](https://github.com/afzal44/serverless-datapipeline-with-awscloud/assets/49905450/e8d381b2-ffd9-4bbe-9ef2-9ac2daa837f9)

1. * Ingesting Data at the Bronze Layer

   Our data pipeline begins with ingesting raw data from an on-premises system into an S3 bucket named 'src_bkt.' This data is delivered in zipped compressed format daily via a cron job. This initial layer of data is referred to as the "Bronze Layer."

2. * Scheduling Pipeline Execution with EventBridge

   To automate the data pipeline, we utilize AWS EventBridge. We create an event rule named 'pipeline-run-rule,' which triggers our data pipeline, represented by an AWS Step Functions state machine called 'DemoDataPipeLine,' at a specific time daily.

3. * Data Extraction and Transformation at the Silver Layer

   Inside the 'DemoDataPipeLine' state machine, we have a Lambda function named 'extractor.' This function is responsible for reading the zipped files from the source S3 bucket, decompressing them, and cleaning the data by removing null values. This processed data is now at the "Silver Layer."

4. * Further ETL Processing for the Golden Layer

   After reaching the Silver Layer, the data goes through another ETL (Extract, Transform, and Load) job within the 'DemoDataPipeLine' state machine. This job performs additional transformations and cleaning to prepare the data for analytics. Once completed, the data is now in the "Golden Layer."

5. * Notifications with SNS

   To keep the operations team informed about the progress of the data pipeline, we set up an AWS Simple Notification Service (SNS) topic. This topic sends notifications on every state transition within the 'DemoDataPipeLine' state machine, ensuring that the team is always up-to-date on the pipeline's status.

6. * Data Catalog and Table Population

   With the data now in the Golden Layer, the 'DemoDataPipeLine' state machine triggers AWS Crawlers. These Crawlers automatically populate the data catalog with metadata about the datasets, making it easy to query and analyze the data.

7. * Data Analysis with Athena

   Once the data catalog is populated, we can leverage AWS Athena for querying and analyzing the data. Athena allows you to run SQL queries on the data catalog's tables, enabling data analysts and data scientists to gain valuable insights from the processed data.

8. * Monitoring with CloudWatch

   To ensure the reliability and performance of our data pipeline, we use AWS CloudWatch. CloudWatch provides monitoring and logging capabilities for our Lambda functions and ETL jobs, allowing us to track and troubleshoot any issues that may arise.
