import matplotlib.pyplot as plt
import glob
import matplotlib.image as mpimg
import os

categories = {
    # 'Texts': [
    #     'DSC03376',
    #     'DSC03366',
    #     'DSC02725',
    #     'DSC03071',
    #     'DSC03345',
    #     'DSC02842',
    #     'DSC03083',
    #     'DSC02861',
    #     'DSC03091',
    #     'DSC03144'
    # ],
    # 'Set5': [
    #     'baby',
    #     'bird',
    #     'butterfly',
    #     'head',
    #     'woman'
    # ],
    'Set14': [
        'baboon',
        'barbara',
        'bridge',
        'coastguard',
        'comic',
        'face',
        'flowers',
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

img_format = 'png'
base_dir = '../../dataset'

for image_cat in categories.keys():
    img_format = 'JPG' if image_cat == 'Texts' else 'png'

    for image in categories[image_cat]:
        for scale in [2, 3, 4, 8]:
            org_img = base_dir + '/GroundTruth/{category}/{target}.{ext}' \
                .format(category=image_cat, target=image, ext=img_format)
            dwn_img = base_dir + '/DownSampled/{category}/{target}x{scale}.{ext}' \
                .format(category=image_cat, target=image, scale=scale, ext=img_format)

            img_ary = [dwn_img, org_img] + sorted(
                glob.glob(
                    base_dir + '/UpSampled/{category}/{target}_*x{scale}.{ext}'.format(
                        category=image_cat, target=image, scale=scale, ext=img_format
                    )
                ),
                reverse=True
            )
            fig = plt.figure(figsize=(25, 15))  # specifying the overall grid size

            for i, path in enumerate(img_ary):
                # img_name = str()
                if i == 0:
                    plt.subplot(5, 5, 2)
                    img_name = 'DownSampled (LR)'

                elif i == 1:
                    plt.subplot(5, 5, 4)
                    img_name = 'Original (HR)'

                else:
                    plt.subplot(5, 5, i + 4)
                    img_name = ": ".join(str(path).split('/')[-1].split('_')[1:]).split('x')[0]

                plt.xticks(None)
                plt.yticks(None)
                plt.xlabel(img_name, weight='bold', fontsize=15)
                target_img = mpimg.imread(path)
                # if i == 0:
                #     target_img = mpimg.imread(path)[10:50, 50:]
                # else:
                #     target_img = mpimg.imread(path)[40:200, 200:]

                plt.imshow(target_img, interpolation=None, aspect='equal')

            plt.suptitle('{target} X{scale} results'.format(target=image_cat + '>' + image,
                                                            scale=scale),
                         fontsize=50, weight='bold')
            plt.tight_layout()
            # plt.show()
            fig.savefig('./images/{target}_{scale}_ppt.png'.format(target=image_cat + '_' + image, scale=scale))
            print('cur:', image_cat, '>', image, 'x', scale)
