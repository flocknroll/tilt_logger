# tilt_logger

##  Pre requisites
Enable bluetooth before starting:
```bash
bluetoothctl -- power on
```

## Running
The `TILT_DB_PWD` environment variable must be set.

```bash
sudo TILT_DB_PWD=<pass> python -m tilt_logger.__main__
```