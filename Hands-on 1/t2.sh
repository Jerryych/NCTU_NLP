#!/bin/bash
# Run python files related to task 2

echo Running ./t2.py
python3 t2.py
echo Output files: ./t2_300.json, ./t2_all_word.json
echo Running ./t2_output.py
python3 t2_output.py
echo Output files: ./t2_ans.txt
