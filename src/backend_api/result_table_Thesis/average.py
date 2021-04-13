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
    'Urban100': [
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

all_df = pd.DataFrame()
for category in categories.keys():
    cur_scale_cur_cat_df = pd.DataFrame()
    for image in categories[category]:
        cur_scale_cur_cat_df = cur_scale_cur_cat_df.append(
            other=base_df.loc[(base_df['image_name'] == image)],
            ignore_index=True,
        )

    cur_scale_cur_cat_df['Dataset'] = category
    cols = cur_scale_cur_cat_df.columns

    cur_scale_cur_cat_df = cur_scale_cur_cat_df[[cols[-1]] + list(cols[:-1])]
    cur_scale_cur_cat_df = cur_scale_cur_cat_df.groupby(['factor', 'iqa']).mean()

    cur_scale_cur_cat_df = cur_scale_cur_cat_df\
        .sort_values(by=['iqa'])

    mins = cur_scale_cur_cat_df.idxmin(axis="columns")
    maxs = cur_scale_cur_cat_df.idxmax(axis="columns")

    cur_scale_cur_cat_df['min'] = mins
    cur_scale_cur_cat_df['max'] = maxs

    cur_scale_cur_cat_df.to_csv(
        path_or_buf='./tables/avg_raw_{category}.csv'.format(category=category),
        index=True
    )
