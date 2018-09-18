#!/bin/bash
# Run python files to download and parse subtitles

echo ========================
echo Running ./downloadSub.py
echo ------------------------
python3 downloadSub.py
echo ========================
echo Running ./t2s.py
echo ------------------------
python3 t2s.py
echo ========================
echo Running ./parse.py
echo ------------------------
python3 parse.py
