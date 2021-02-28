import matplotlib.pyplot as plt
import cv2
import pandas as pd


def load_image(image_dir: [str]):
    return cv2.imread(image_dir)


def get_method_metric(df: pd.DataFrame,
                      method_name: str):
    metrics_srs = df[method_name]
    metrics_srs = metrics_srs.round(decimals=6)
    index = metrics_srs.index.to_list()
    values = metrics_srs.values.tolist()

    result_str = ''
    for i, v in zip(index, values):
        result_str += str(i) + ':' + str(v)
        result_str += '\n'

    return result_str


def get_final_results(target_image_dirs: dict,
                      metrics_df_dir: str,
                      save_dir=None):
    metrics_df = pd.read_csv(metrics_df_dir)
    metrics_df.set_index('Unnamed: 0', inplace=True)
    metrics_df = metrics_df.transpose()

    fig, axs = plt.subplots(nrows=len(target_image_dirs) // 3 + 1, ncols=3,
                            # figsize=(9, 6),
                            subplot_kw={'xticks': [], 'yticks': []})
    for ax, pred_items in zip(axs.flat, target_image_dirs.items()):
        pred_type, pred_image_dir = pred_items
        cur_img = load_image(pred_image_dir)
        ax.imshow(cur_img)
        ax.set_title(str(pred_type))

        metrics_result = get_method_metric(metrics_df, pred_type)
        ax.set_xlabel(metrics_result, fontsize=10)

    plt.tight_layout()

    if save_dir is None:
        plt.show()
    else:
        plt.savefig(save_dir)


if __name__ == '__main__':
    image_base = '../../test_images/'

    get_final_results(
        target_image_dirs={
            'original': image_base + 'originalImage.jpg',
            'EDSR_x2': image_base + 'DeepLearningModels/EDSR_x2.jpg',
            'FSRCNN_x2': image_base + 'DeepLearningModels/FSRCNN_x2.jpg',
            'bilinear': image_base + 'Interpolations/bilinear.jpg',
            'bicubic': image_base + 'Interpolations/cubic.jpg',
            'lanczos': image_base + 'Interpolations/lanczos.jpg',
            'nearest': image_base + 'Interpolations/nearest.jpg',
        },
        metrics_df_dir=image_base + 'IQAmetrics_0912_2020.csv',
        save_dir='../../test_images/temp_result_0912_2020.jpg'
    )
