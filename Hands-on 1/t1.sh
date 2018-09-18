#!/bin/bash
# Run python files related to task 1

echo Running ./t1.py
python3 t1.py
echo Output files: ./t1_300.json, ./t1_all_word.json
echo Running ./t1_output.py
python3 t1_output.py
echo Output files: ./t1_ans.txt
