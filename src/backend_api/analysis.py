import pandas as pd
from pprint import pprint as pp
from collections import Counter

import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go

iqa_df = pd.read_csv('./result.csv')
iqa_df = iqa_df.rename(columns={
    'Unnamed: 0': 'image_name',
    'Unnamed: 1': 'iqa'
})

image_info = iqa_df["image_name"].str.split("x", n=1, expand=True)

iqa_df["image_name"] = image_info[0]
iqa_df["factor"] = image_info[1]

columns = iqa_df.columns
models = columns[2:-1]

target_columns = list()
target_columns.append(columns[0])
target_columns.append(columns[-1])
target_columns.append(columns[1])
target_columns += models.to_list()

iqa_df = iqa_df[target_columns]
iqa_df.sort_values(by=['image_name', 'factor', 'iqa'], ascending=[True, True, True], inplace=True)
range_df = iqa_df.copy()
iqa_df.set_index(keys=['image_name', 'factor', 'iqa'], inplace=True)

max_res = iqa_df.idxmax(axis=1)
min_res = iqa_df.idxmin(axis=1)
iqa_df['max'] = max_res
iqa_df['min'] = min_res


def get_best(rows):
    if rows.name[2] == 'RMSE':
        return rows['min']
    return rows['max']


iqa_best = iqa_df[['max', 'min']].apply(get_best, axis=1)

iqa_df['best'] = iqa_best

iqa_df.drop(columns=['min', 'max'], inplace=True)

counts = {
    2: {
        'FSIM': [],
        'PSNR': [],
        'RMSE': [],
        'SSIM': [],
    },
    3: {
        'FSIM': [],
        'PSNR': [],
        'RMSE': [],
        'SSIM': [],
    },
    4: {
        'FSIM': [],
        'PSNR': [],
        'RMSE': [],
        'SSIM': [],
    },
    8: {
        'FSIM': [],
        'PSNR': [],
        'RMSE': [],
        'SSIM': [],
    },
}


def counter(rows):
    counts[int(rows.name[1])][rows.name[2]].append(rows['best'])


iqa_df[['best']].apply(counter, axis=1)

iqa_df.to_csv('result_org.csv')
for i in counts.keys():
    for j in counts[i].keys():
        counts[i][j] = sorted(Counter(counts[i][j]).items(), key=lambda x: x[1], reverse=True)
pp(counts)

counts_df = pd.DataFrame.from_dict(counts)

counts_df.to_csv('./result_iqa_org.csv')

