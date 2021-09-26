#!/usr/bin/env bash

source /home/flo/dev/venv/bin/activate && python -m tilt_logger.__main__ --db-pass $(cat /home/flo/dev/db_pass)