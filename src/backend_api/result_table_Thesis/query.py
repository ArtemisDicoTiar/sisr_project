import pandas as pd


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

base_df = pd.read_csv('../result_org.csv')

for scale in [2, 3, 4, 8]:
    for category in categories.keys():
        cur_scale_cur_cat_df = pd.DataFrame()
        for image in categories[category]:
            cur_scale_cur_cat_df = cur_scale_cur_cat_df.append(
                other=base_df.loc[(base_df['image_name'] == image) & (base_df['factor'] == scale)],
                ignore_index=True,
            )
        cur_scale_cur_cat_df = cur_scale_cur_cat_df\
            .drop(columns=['factor'])\
            .sort_values(by=['image_name', 'iqa'])\
            .round(3)

        cur_scale_cur_cat_df.to_csv(
            path_or_buf='./tables/{category}_{scale}.csv'.format(category=category, scale=scale),
            index=False
        )


