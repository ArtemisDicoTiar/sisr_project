import pandas as pd

names = ['Set5', 'Set14', 'Text', 'Urban100_partial']
scales = [2, 3, 4, 8]
iqas = ['FSIM', 'PSNR', 'RMSE', 'SSIM']

total_df = pd.DataFrame()
index_list = list()
cols = []
for iqa in iqas:
    cols.append(iqa + '_min')
    cols.append(iqa + '_max')
cur_scale_df = pd.DataFrame()

for scale in scales:
    for name in names:
        cur_name_org_df = pd.read_csv('./{name}_min_max.csv'.format(name=name))
        cur_name_data_df = pd.read_csv('./{name}_all_iqa.csv'.format(name=name))

        cur_name_org_df = cur_name_org_df.loc[cur_name_org_df['factor'] == scale]
        cur_name_data_df = cur_name_data_df.loc[cur_name_data_df['factor'] == scale]

        result = dict()
        for iqa in iqas:
            max_method, min_method = cur_name_org_df.loc[cur_name_org_df['iqa'] == 'FSIM'][['Max1', 'Min1']].values[0]
            max_val = cur_name_data_df.loc[cur_name_data_df['iqa'] == iqa][max_method].values[0]
            min_val = cur_name_data_df.loc[cur_name_data_df['iqa'] == iqa][min_method].values[0]

            result[iqa + '_min_method'] = min_method
            result[iqa + '_min_val'] = min_val
            result[iqa + '_max_method'] = max_method
            result[iqa + '_max_val'] = max_val

        cur_scale_df = cur_scale_df.append(result, ignore_index=True)

        index_list.append((scale, name))

cur_scale_df.index = pd.MultiIndex.from_tuples(index_list, names=("factor", "image_set"))

cur_scale_df.to_csv('./all_min_max.csv')
