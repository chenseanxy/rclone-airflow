# rclone-airflow
Rclone + Airflow for scheduled, easily configurable backups & syncs

## Quick Start

- Have Docker & docker-compose installed
- Clone this repository: `git clone https://github.com/chenseanxy/rclone-airflow.git && cd rclone-airflow`
- Rclone config:
  - Copy your current config file `~/.config/rclone/rclone.conf` to conf/rclone, or
  - Generate a new one with `docker run --rm -it --user $UID:$GID --volume $PWD/conf/rclone:/config/rclone rclone/rclone config`
- Jobs config: See "Configuration"
- Docker-compose:
  - Regarding compose files:
    - Use prebuilt image with `docker-compose.yml`, or
    - Use locally built image with `docker-compose.local.yml` and add your own DAGs & plugins, build with `AIRFLOW_UID=$UID docker-compose -f docker-compose.local.yml build`
  - Add your data volumes in x-rclone-conf.volumes, preferablly using :rw flag if you're just using this for backups
  - Change TZ to your local timezone, use [TZ database name](https://en.wikipedia.org/wiki/List_of_tz_database_time_zones#List) format
- Start the service stack
  - Prebuilt image: `AIRFLOW_UID=$UID docker-compose up -d`
  - Local image: `AIRFLOW_UID=$UID docker-compose -f docker-compose.local.yml up -d`


## Configuration

Jobs config: /conf/jobs.yml

Config will be automatically refreshed when Airflow refreshes DAG (defaults: every 60 seconds)

```yaml
isos:                   # Job name
  cron: 0 0 0 * *       # See crontab.guru, required
  source: /data/isos    # Source location, required
  target: remote:isos   # Target location, required
  
  # See backup-dir in rclone docs, value here is a prefix
  # Actual backup-dir will be `value/<date-time>`,
  # like `remote:backup/isos/2021-10-24-11-45`
  # Not required, leave out to disable backup-dir
  backup: remote:backup/isos
```

Each job will have one DAG (workflow) generated, you'll have to manually enable each one in Airflow UI
- Or you could set `AIRFLOW__CORE__DAGS_ARE_PAUSED_AT_CREATION` to `false` in compose, to automatically enable these dags upon creation

Each config job will only have one instance running at a time, later instances will queue after running instances.

## Monitoring

TODO; via rclone's prometheus metric endpoint

## Components and Dependencies

Using rclone rcd as rclone server, and Airflow + rclonerc to control rclone using HTTP API;

- RClone: pinned to 1.56.2 via compose file, though upgrading shouldn't pose much problems
- Airflow: pinned to 2.2.0, upgrading might need further changes to compose file
- [rclonerc](https://github.com/chenseanxy/rclonerc): Via Dockerfile, not pinned

##  Contributing

This is a POC at the moment, and all issues & pull requests are welcome!

Current ideas:

- Configurable success & error hooks, for notification, etc
- Allow for generic rclone flags, filters, options, etc
- Runnable DAG for global bandwidth limit, etc

Dev environment: use `docker-compose -f docker-compose.local.yml up -d` & `pipenv install --dev`
