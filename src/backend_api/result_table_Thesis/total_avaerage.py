import pandas as pd

base_df = pd.read_csv('../result_org.csv')

all_df = pd.DataFrame()
for scale in [2, 3, 4, 8]:
    cur_scale_df = base_df.loc[base_df['factor'] == scale]
    print(cur_scale_df.columns)
    print(cur_scale_df)
    all_df = all_df.append(
        other=cur_scale_df.groupby(['factor']).mean().round(decimals=4),
        ignore_index=True
    )
# all_df = all_df[['factor', 'DRCNN', 'EDSR', 'ESPCN', 'FSRCNN', 'ICBI', 'INEDI', 'LapSRN',
#        'VDSR_bicubic', 'VDSR_bilinear', 'VDSR_lanczos', 'VDSR_nearest',
#        'bicubic', 'bilinear' , 'lanczos', 'nearest']]

print(all_df.columns)
print(all_df)
# all_df.to_csv('./tables/all_average.csv')
