#!/bin/bash

cd /stacosys
python3 stacosys/run.py /config/config.ini

tail -f /dev/null