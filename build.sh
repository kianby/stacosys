#!/bin/sh
#pyinstaller stacosys/run.py --name stacosys --onefile
poetry run pyinstaller stacosys.spec
