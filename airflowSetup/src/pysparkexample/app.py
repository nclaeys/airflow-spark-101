import argparse

from pyspark.sql import SparkSession
from pyspark.sql import Row
from pyspark.sql.dataframe import DataFrame
from pyspark.sql.functions import *

from pysparkexample.common.spark import ClosableSparkSession, transform, SparkLogger


def main():
    parser = argparse.ArgumentParser(description="pyspark-example")
    parser.add_argument(
        "-d", "--date", dest="date", help="date in format YYYY-mm-dd", required=True
    )
    parser.add_argument(
        "-e", "--env", dest="env", help="environment we are executing in", required=True
    )
    args = parser.parse_args()

    session = (SparkSession
               .builder
               .appName("pyspark taxi example")
               #.enableHiveSupport()
               .getOrCreate())

    run(session, args.env, args.date)


def run(spark: SparkSession, environment: str, date: str):
    """Main ETL script definition.

    :return: None
    """
    # execute ETL pipeline
    logger = SparkLogger(spark)
    logger.info(f"Executing job for {environment} on {date}")

    df_zone = extract_zone_data(spark,environment, date)
    df_taxi = extract_taxi_data(spark, environment, date)

    transformed = transform_data(df_taxi, df_zone, date)

    persist_data(spark, environment, transformed)


def extract_zone_data(spark: SparkSession, environment: str, date: str) -> DataFrame:
    csv_location = construct_resources_path(environment, 'taxi_zone_lookup.csv')
    df_zones = spark.read.format("csv")\
        .option("inferschema", "true")\
        .option("header", "true")\
        .option("mode", "DROPMALFORMED").load(csv_location)

    df_concat_zones = df_zones.select(df_zones.LocationID,
                                      concat(df_zones.Zone, lit(', '), df_zones.Borough).alias('Location'))
    df_concat_zones.show(10, False)
    
    return df_concat_zones


def extract_taxi_data(spark: SparkSession, environment: str, date: str) -> DataFrame:
    csv_location = construct_resources_path(environment, 'yellow_tripdata_2023-01.parquet')
    df = spark.read.parquet(csv_location)
    df.show(10, False)
    return df

def transform_data(df_taxi: DataFrame, df_zone: DataFrame, date: str) -> DataFrame:
    df_id_count = df_taxi.groupBy('PULocationID', 'DOLocationID') \
        .count().withColumnRenamed('count', 'Number of trips')

    df_id_count_renamed = df_id_count\
        .join(df_zone, df_id_count['PULocationID'] == df_zone['LocationID'], how='inner').drop('LocationID').withColumnRenamed('Location', 'PULocation')\
        .join(df_zone, df_id_count['DOLocationID'] == df_zone['LocationID'], how='inner').drop('LocationID').withColumnRenamed('Location', 'DOLocation')\
        .sort(desc('Number of trips'))

    df_id_count_renamed.show(10, False)
    return df_id_count_renamed


def persist_data(spark: SparkSession, environment: str, data: DataFrame):
    """Writes the output dataset to some destination

    :param data: DataFrame to write.
    :return: None
    """
    parquet_folder = construct_resources_path(environment, f'/{environment}/popular_taxi_rides')
    data.write.format('parquet').mode('overwrite').save(parquet_folder)


def construct_resources_path(environment, file_name):
    if environment == 'prd':
        csv_location = f'/workspace/resources/{file_name}'
    else:
        csv_location = f'resources/{file_name}'
    return csv_location


if __name__ == "__main__":
    main()
