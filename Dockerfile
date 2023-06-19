FROM public.ecr.aws/dataminded/spark-k8s-glue:v3.3.1-hadoop-3.3.4-v2

ENV PYSPARK_PYTHON python3
WORKDIR /opt/spark/work-dir
USER 0

COPY resources/taxi_zone_lookup.csv /workspace/resources/taxi_zone_lookup.csv
COPY resources/yellow_tripdata_2023-01.parquet /workspace/resources/yellow_tripdata_2023-01.parquet

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt --no-cache-dir
COPY src src
COPY setup.py setup.py
RUN pip3 install .