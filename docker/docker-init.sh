#!/bin/bash

cd /stacosys
# workaround for startup
cp -f stacosys/run.py .
python3 run.py /config/config.ini

# catch for debug
#tail -f /dev/null