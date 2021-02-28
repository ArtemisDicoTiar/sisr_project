import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import plotly.express as px

iqas = ['FSIM', 'PSNR', 'RMSE', 'SSIM']
all_df = pd.read_csv('./all_min_max.csv')

for factor in [2, 3, 4, 8]:
    cur_factor_df = all_df.loc[all_df['factor'] == factor]
    image_sets = cur_factor_df['image_set'].to_list()

    FSIM_min = cur_factor_df['FSIM_min_val'].to_list()
    FSIM_max = cur_factor_df['FSIM_max_val'].to_list()
    FSIM_min_method = cur_factor_df['FSIM_min_method'].to_list()
    FSIM_max_method = cur_factor_df['FSIM_max_method'].to_list()

    PSNR_min = cur_factor_df['PSNR_min_val'].to_list()
    PSNR_max = cur_factor_df['PSNR_max_val'].to_list()
    PSNR_min_method = cur_factor_df['PSNR_min_method'].to_list()
    PSNR_max_method = cur_factor_df['PSNR_max_method'].to_list()

    RMSE_min = cur_factor_df['RMSE_min_val'].to_list()
    RMSE_max = cur_factor_df['RMSE_max_val'].to_list()
    RMSE_min_method = cur_factor_df['RMSE_min_method'].to_list()
    RMSE_max_method = cur_factor_df['RMSE_max_method'].to_list()

    SSIM_min = cur_factor_df['SSIM_min_val'].to_list()
    SSIM_max = cur_factor_df['SSIM_max_val'].to_list()
    SSIM_min_method = cur_factor_df['SSIM_min_method'].to_list()
    SSIM_max_method = cur_factor_df['SSIM_max_method'].to_list()

    #
    f, axes = plt.subplots(4, 1, figsize=(6, 10))

    (fsim, psnr, rmse, ssim) = axes

    rs = [0, 1, 2, 3]
    barWidth = 0.4
    fsim.barh(rs, FSIM_max, color='#008080', height=barWidth, edgecolor='white')
    psnr.barh(rs, PSNR_max, color='#008080', height=barWidth, edgecolor='white')
    rmse.barh(rs, RMSE_min, color='#ba2c73', height=barWidth, edgecolor='white')
    ssim.barh(rs, SSIM_max, color='#008080', height=barWidth, edgecolor='white')

    rs = [x + barWidth for x in rs]
    fsim.barh(rs, FSIM_min, color='#ba2c73', height=barWidth, edgecolor='white')
    psnr.barh(rs, PSNR_min, color='#ba2c73', height=barWidth, edgecolor='white')
    rmse.barh(rs, RMSE_max, color='#008080', height=barWidth, edgecolor='white')
    ssim.barh(rs, SSIM_min, color='#ba2c73', height=barWidth, edgecolor='white')

    # Add xticks on the middle of the group bars
    for idx in range(4):
        plt.sca(axes[idx])
        plt.ylabel(iqas[idx], fontweight='bold')
        plt.yticks([r + barWidth / 2 for r in range(len(rs))], image_sets)
        plt.grid('minor', linestyle=':')
        xmin, xmax, ymin, ymax = plt.axis()
        xavg, yavg = (xmin + xmax) / 2, (ymin + ymax) / 2
        if idx == 0:
            for met_idx, val in enumerate(FSIM_max):
                plt.text(xavg / 20, met_idx - barWidth / 3, FSIM_max_method[met_idx], weight='bold')
                plt.text(xavg / 20, met_idx + barWidth * 2 / 3, FSIM_min_method[met_idx], weight='bold')
        elif idx == 1:
            for met_idx, val in enumerate(PSNR_max):
                plt.text(xavg / 20, met_idx - barWidth / 3, PSNR_max_method[met_idx], weight='bold')
                plt.text(xavg / 20, met_idx + barWidth * 2 / 3, PSNR_min_method[met_idx], weight='bold')
        elif idx == 2:
            for met_idx, val in enumerate(RMSE_max):
                plt.text(xavg / 20, met_idx - barWidth / 3, RMSE_min_method[met_idx], weight='bold')
                plt.text(xavg / 20, met_idx + barWidth * 2 / 3, RMSE_max_method[met_idx], weight='bold')
        elif idx == 3:
            for met_idx, val in enumerate(SSIM_max):
                plt.text(xavg / 20, met_idx - barWidth / 3, SSIM_max_method[met_idx], weight='bold')
                plt.text(xavg / 20, met_idx + barWidth * 2 / 3, SSIM_min_method[met_idx], weight='bold')

    f.suptitle("Scale Factor: {}".format(factor), fontsize=16)

    # Create legend & Show graphic
    # plt.tight_layout()
    f.legend(['Best', 'Worst'], loc='upper right')
    plt.show()
    f.savefig('./{scale}.png'.format(scale=factor))

    # rs = [0, 0.25]
    # group_gap = 1
    # for idx, image_set in enumerate(image_sets):
    #     fsim.barh(rs, FSIM_all[2*idx:2*(idx+1)])
    #     psnr.barh(rs)
    #     rmse.barh(rs)
    #     ssim.barh(rs)
    #     rs = [x + group_gap for x in rs]
