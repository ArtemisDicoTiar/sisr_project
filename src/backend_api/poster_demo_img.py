import matplotlib.pyplot as plt
import glob
import matplotlib.image as mpimg
import os

target_img_path = 'Set14/ppt3'
target_factor = 4
img_format = 'png'

org_img = '../dataset/GroundTruth/{target}.{ext}'.format(target=target_img_path, ext=img_format)
dwn_img = '../dataset/DownSampled/{target}x{scale}.{ext}'.format(target=target_img_path, scale=target_factor, ext=img_format)
img_ary = [dwn_img, org_img] + \
          sorted(
              glob.glob(
                  '../dataset/UpSampled/{target}_*x{scale}.{ext}'
                      .format(target=target_img_path, scale=target_factor, ext=img_format)
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
    if i == 0:
        target_img = mpimg.imread(path)[10:50, 50:]
    else:
        target_img = mpimg.imread(path)[40:200, 200:]

    plt.imshow(target_img, interpolation=None, aspect='equal')

plt.suptitle('{target} X{scale} results (partial)'.format(target=target_img_path.replace('/', '-'), scale=target_factor),
             fontsize=50, weight='bold')
plt.tight_layout()
plt.show()
fig.savefig('./{target}_{scale}_ppt.png'.format(target=target_img_path.replace('/', '_'), scale=target_factor))
