# tilt_logger

## Pre requisites
1. Enable bluetooth before starting:
```bash
bluetoothctl -- power on
```

2. Start a postgres DB with docker:
```bash
docker run -d -p 5432:5432 -e POSTGRES_PASSWORD=<master_pass> -v /data/postgresql:/var/lib/postgresql/data --name tiltdb timescale/timescaledb:latest-pg13
```

3. Create a `tilt_db` DB with a `tilt` user

3. Init the DB with [init.sql](./sql/init.sql)

## Running
It must be run as root to access the BT hardware.

```bash
sudo python -m tilt_logger.__main__ -p <pass>
```