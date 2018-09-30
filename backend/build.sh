#!/bin/bash
pyinstaller -F --distpath .. --workpath working --specpath working --clean ./netnet.py
rm -rf __pycache__
rm -rf working
python ./functions.py