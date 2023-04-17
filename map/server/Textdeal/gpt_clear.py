import pandas
import numpy
import re
import os
import json
import time

with open('../data/gpt_result.json', 'r', encoding='utf-8') as f:
    front = json.load(f)
with open('../data/gpt_result_first.json', 'r', encoding='utf-8') as w:
    end = json.load(w)

with open('../data/clear_text.json', 'r', encoding='utf-8') as z:
    film = json.load(z)

def model_judge(line):
    if '{' in line:
        clear1 = line.split(',')
        for unit in clear1:
            if '{' in unit:
                clear2 = unit.strip(' ')
                clear2 = clear2.strip('{}')
                print(clear2)
        print('--------')


plot = end + front
no_dia = []
for i in film:
    tmp = []
    for j in i:
        if j[0] == '$':
            continue
        tmp.append(j)
    no_dia.append(tmp)
no_dia = no_dia[1:]

for i in range(len(no_dia)):
    print(len(no_dia[i]), len(plot[i]))
    for j in range(len(no_dia[i])):
        if plot[i][j] == 'error':
            print(i, no_dia[i][j])

# for slug in plot:
#     for line in slug:
#         print(line)
#         model_judge(line)
#     # break

