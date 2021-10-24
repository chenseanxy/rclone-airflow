FROM apache/airflow:2.2.0
RUN pip install --no-cache-dir rclonerc
COPY --chown=airflow:root dags/* /opt/airflow/dags