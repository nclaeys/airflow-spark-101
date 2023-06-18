FROM apache/airflow:2.5.1

USER root

RUN apt-get update && apt-get install -y default-jdk tar

ENV JAVA_HOME='/usr/lib/jvm/java-11-openjdk-amd64'
ENV PATH=$PATH:$JAVA_HOME/bin

ENV SPARK_HOME='/opt/spark'
ENV PATH=$PATH:$SPARK_HOME/bin:$SPARK_HOME/sbin

ENV AIRFLOW_VERSION=2.5.1

COPY spark-3.3.2-bin-hadoop3.tgz /tmp/spark-3.3.2-bin-hadoop3.tgz
RUN mkdir /opt/spark && tar -xvf /tmp/spark-3.3.2-bin-hadoop3.tgz -C /tmp/ && mv /tmp/spark-3.3.2-bin-hadoop3/* /opt/spark/
COPY src/ /workspace/src/
COPY setup.py /workspace/
RUN mkdir -p /workspace/resources/popular_taxi_rides
RUN chown -R airflow:root /workspace

USER airflow
ADD requirements.txt .
RUN pip install -r requirements.txt

COPY resources/taxi_zone_lookup.csv /workspace/resources/taxi_zone_lookup.csv
COPY resources/yellow_tripdata_2023-01.parquet /workspace/resources/yellow_tripdata_2023-01.parquet


WORKDIR /workspace
RUN pip install -e .