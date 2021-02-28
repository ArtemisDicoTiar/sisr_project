import pandas as pd
from pprint import pprint as pp

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

iqa_df = iqa_df.stack().to_frame().reset_index().rename(columns={'level_3': 'method', 0: 'value'})


# fig = px.scatter(iqa_df, x="factor", y="value", color="method",
#                  # barmode="group",
#                  facet_row="image_name", facet_col="iqa",
#                  # trendline='ols',
#                  opacity=0.5
#                  )

fig = px.scatter(iqa_df, x="factor", y="value", color="method",
                 # barmode="group",
                 animation_frame="image_name",
                 # animation_group="iqa",
                 # hover_name="method",
                 facet_col="iqa",
                 # trendline='ols',
                 opacity=0.75
                 )
range_df = range_df.set_index(keys=['iqa', 'image_name', 'factor'])
iqa_min = range_df.groupby(level="iqa").min().min(axis=1)
iqa_max = range_df.groupby(level="iqa").max().max(axis=1)
# FSIM, PSNR, RMSE, SSIM
fig.layout.yaxis1.update(matches=None, range=[iqa_min['FSIM'], iqa_max['FSIM']], showticklabels=True)
fig.layout.yaxis2.update(matches=None, range=[iqa_min['PSNR'], iqa_max['PSNR']], showticklabels=True)
fig.layout.yaxis3.update(matches=None, range=[iqa_min['RMSE'], iqa_max['RMSE']], showticklabels=True)
fig.layout.yaxis4.update(matches=None, range=[iqa_min['SSIM'], iqa_max['SSIM']], showticklabels=True)

fig.layout.updatemenus[0].buttons[0].args[1]['frame']['duration'] = 2000
fig.layout.updatemenus[0].buttons[0].args[1]['transition']['duration'] = 500
fig.write_html("./graphPerImage.html")
fig.show()
