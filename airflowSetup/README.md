
## Setting the right Airflow user
On Linux, the quick-start needs to know your host user id and needs to have group id set to 0. Otherwise the files created in dags, logs and plugins will be created with root user ownership. You have to make sure to configure them for the docker-compose:

mkdir -p ./dags ./logs ./plugins ./config
echo -e "AIRFLOW_UID=$(id -u)" > .env
See Docker Compose environment variables

## Initialize the database
On all operating systems, you need to run database migrations and create the first user account. To do this, run.

docker compose up airflow-init
After initialization is complete, you should see a message like this:

airflow-init_1       | Upgrades done
airflow-init_1       | Admin user airflow created
airflow-init_1       | 2.6.2
start_airflow-init_1 exited with code 0
The account created has the login airflow and the password airflow.

## Cleaning-up the environment
The docker-compose environment we have prepared is a “quick-start” one. It was not designed to be used in production and it has a number of caveats - one of them being that the best way to recover from any problem is to clean it up and restart from scratch.

The best way to do this is to:

Run docker compose down --volumes --remove-orphans command in the directory you downloaded the docker-compose.yaml file

Remove the entire directory where you downloaded the docker-compose.yaml file rm -rf '<DIRECTORY>'

Run through this guide from the very beginning, starting by re-downloading the docker-compose.yaml file

## Running Airflow
Now you can start all services:

docker compose up