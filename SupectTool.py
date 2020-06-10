# -*- coding: utf-8 -*-
import sys
import json
import pandas as pd


def susexp(filename):
    data = []
    tmp = ''
    with open(filename, 'r', encoding='UTF-8') as fr:
        lines = fr.readlines()[1:-2]
        for line in lines:
            if '},' not in line:
                tmp = tmp + line
            else:
                st = tmp + line.strip().split('},')[0]
                j = json.loads('[' + st + '}]')
                data.append(j)
                tmp = line.strip().split('},')[1]
        j = json.loads('['+tmp + '}]')
        data.append(j)

    df = pd.DataFrame() 
    for line in data:
        for i in line:
            df1 = pd.DataFrame([i])
            df = df.append(df1)
    df = df[['NAME', 'API', 'CMD', 'METRICS', 'TYPE', 'LABEL']]
    df.index = range(1, df.shape[0]+1)
    df.to_excel('suspects.xlsx', sheet_name='Data', startcol=0, index=False)
    objects = json.dumps(df.to_dict(orient='records'), indent=4)
    with open('./suspects.json.exp', 'wt') as f:
        f.write(objects)


if __name__ == "__main__":
    susexp('./suspects.json')
