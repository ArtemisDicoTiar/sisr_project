import pandas as pd
import numpy as np
from pprint import pprint as pp

iqa_df = pd.read_csv('./result_org.csv')
categories = {
    'Text': [
        'DSC03376',
        'DSC03366',
        'DSC02725',
        'DSC03071',
        'DSC03345',
        'DSC02842',
        'DSC03083',
        'DSC02861',
        'DSC03091',
        'DSC03144'
    ],
    'Set5': [
        'baby',
        'bird',
        'butterfly',
        'head',
        'woman'
    ],
    'Set14': [
        'baboon',
        'barbara',
        'bridge',
        'coastguard',
        'comic',
        'face',
        'flower',
        'foreman',
        'lenna',
        'man',
        'monarch',
        'pepper',
        'ppt3',
        'zebra'
    ],
    'Urban100_partial': [
        'img_001',
        'img_002',
        'img_003',
        'img_004',
        'img_005',
        'img_006',
        'img_007',
        'img_008',
        'img_009',
        'img_010',

    ]
}

for cat_name, cat_images in categories.items():
    cur_cat_df = pd.DataFrame()
    for cat_image in cat_images:
        cur_cat_df = cur_cat_df.append(iqa_df.loc[iqa_df['image_name'] == cat_image])

    cur_cat_df.set_index(keys=['factor', 'iqa'], inplace=True)
    cur_cat_df = cur_cat_df.groupby(by=['factor', 'iqa']).mean()
    cur_cat_df.to_csv(cat_name+'_all_iqa.csv')
    res = cur_cat_df.apply(
        lambda x: pd.Series(
            np.concatenate(
                [x.nlargest(2).index.values, x.nsmallest(2).index.values]
            )),
        axis=1)


    # res.columns = ["Max1", "Max2", "Min1", "Min2"]
    # cur_cat_df[["Max1", "Max2", "Min1", "Min2"]] = res

    # res.to_csv(cat_name+'_min_max.csv')
