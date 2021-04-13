import glob
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

image_cat = 'Urban100'
image = 'img_002'
scale = 3

# x_range = 10, 25
# y_range = 25, 38

x_range = 0, 0
y_range = 0, 0

img_format = 'png'
base_dir = '../../dataset'
img_format = 'JPG' if image_cat == 'Texts' else 'png'

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
    #     target_img = mpimg.imread(path)[x_range[0]:x_range[1], y_range[0]:y_range[1]]
    # else:
    #     target_img = mpimg.imread(path)[x_range[0]*scale:x_range[1]*scale, y_range[0]*scale:y_range[1]*scale]

    plt.imshow(target_img, interpolation=None, aspect='equal')

plt.suptitle('{target} X{scale} results'.format(target=image_cat + '>' + image,
                                                         scale=scale),
             fontsize=50, weight='bold')
plt.tight_layout()
plt.show()
fig.savefig('./zoomed/{target}_{scale}_{ran}.png'
            .format(target=image_cat + '_' + image,
                    scale=scale,
                    ran='x_' + str(x_range[0]) + str(x_range[1]) + 'y_' + str(y_range[0]) + str(y_range[1]))
            )
print('cur:', image_cat, '>', image, 'x', scale)
