import glob
import re
import os
from pprint import pprint as pp
import pandas as pd

from src.backend_api.processor.pre_process.downsampling import DownSampler

from src.backend_api.processor.processor.InterpolationProcessor import Interpolator
from src.backend_api.processor.processor.DeepLearningProcessor import DeepLearningProcessor, ImageSaver, ImageLoader
from src.backend_api.processor.processor.EdgePreserveProcessor import EdgePreserveProcessor

from src.backend_api.settings.ProgramSetting import ProgramSetting, ProgramMode

from src.backend_api.settings.configs.ProgramConfig import \
    ScalingRate, ScaleDirection, \
    ProgramMode, \
    ModelUsage, ModelList

from src.backend_api.utils.IQA_utils import IQA_metrics

imageLoader = ImageLoader()
method_search = re.compile("\S*/\S*?_(\S*)x")

iqa_metrics = IQA_metrics()


def downSample_dataSet(current_dir):
    data_sets = os.listdir('{current_dir}/../dataset/GroundTruth'.format(current_dir=current_dir))
    for scale_factor in [2, 3, 4, 8]:
        print("* CURRENT SCALE: {factor}".format(factor=scale_factor))
        downSampler = DownSampler(scale_factor=scale_factor, color_type='color')

        for data_idx, data_set in enumerate(data_sets):
            if data_set == '.DS_Store':
                continue
            print("\t* CURRENT DATASET: {dataset}".format(dataset=data_set))
            images = os.listdir('{current_dir}/../dataset/GroundTruth/{data_set}'
                                .format(data_set=data_set, current_dir=current_dir))

            for img_idx, image in enumerate(images):
                if image == '.DS_Store':
                    continue

                raw_name = image.split('.')[0]
                ext_name = image.split('.')[-1]

                print('\t\t{image} >> {raw_name}x{scale}.{ext}'
                      .format(image=image, raw_name=raw_name, scale=scale_factor, ext=ext_name), end='  .....  ')

                if os.path.exists('{current_dir}/../dataset/DownSampled/{data_set}/{raw_name}x{scale}.{ext}'
                                          .format(data_set=data_set, raw_name=raw_name, scale=scale_factor,
                                                  ext=ext_name, current_dir=current_dir)):
                    print('>>>>>>>>>>>>>>  EXIST')
                    continue

                downSampler.load_image('{current_dir}/../dataset/GroundTruth/{data_set}/{image}'
                                       .format(data_set=data_set, image=image, current_dir=current_dir))

                downSampler.process_down_sample()
                downSampler.save_img('{current_dir}/../dataset/DownSampled/{data_set}/{raw_name}x{scale}.{ext}'
                                     .format(current_dir=current_dir, data_set=data_set, raw_name=raw_name,
                                             scale=scale_factor, ext=ext_name))

                print('>>>>>>>>>>>>>>  DONE')


def upSample_dataSet(current_dir):
    global dest_img
    setting = ProgramSetting()
    setting.program_mode = ProgramMode.Experiment.UpScale.ONCE

    setting.scaling_rate = ScalingRate(
        scale_direction=ScaleDirection.UP,
        first_scale=2,
    )

    model_set = ModelList()

    setting.model_usage = ModelUsage(
        first_model=model_set,
    )

    setting.setting_conflict_check()

    for method in setting.model_usage.first_model:
        print("* Current: {cur_method}".format(cur_method=method), end=' >> ')

        for model in setting.model_usage.first_model[method].keys():
            print("{cur_model}".format(cur_model=model), end=' >> ')

            for scale_factor in [2, 3, 4, 8]:
                print("X{scale}".format(scale=scale_factor))

                data_sets = os.listdir('{current_dir}/../dataset/GroundTruth'.format(current_dir=current_dir))

                for data_idx, data_set in enumerate(data_sets):
                    if data_set == '.DS_Store':
                        continue

                    print("\t* CURRENT DATASET: {dataset}".format(dataset=data_set))
                    images = os.listdir('{current_dir}/../dataset/GroundTruth/{data_set}'
                                        .format(data_set=data_set, current_dir=current_dir))

                    for img_idx, image in enumerate(images):
                        if image == '.DS_Store':
                            continue

                        print(data_idx, '-', len(data_sets), '==', img_idx, '-', len(images))

                        raw_name = image.split('.')[0]
                        ext_name = image.split('.')[-1]
                        origin_img = '{current_dir}/../dataset/DownSampled/{data_set}/{raw_name}x{scale}.{ext}' \
                            .format(data_set=data_set, raw_name=raw_name, scale=scale_factor,
                                    ext=ext_name, current_dir=current_dir)
                        print('\t\t{origin}'
                              .format(origin=origin_img), end=' ..... \n')

                        if method.lower() == 'interpolation':
                            dest_img = '{current_dir}/../dataset/UpSampled/{data_set}/' \
                                       '{raw_name}_{model}x{scale}.{ext}' \
                                .format(data_set=data_set, raw_name=raw_name, scale=scale_factor,
                                        ext=ext_name, current_dir=current_dir, model=model)
                            if os.path.exists(dest_img):
                                print('>>>>>>>>>>>>>>  EXIST')
                                continue

                            interpolator = Interpolator(
                                scale_factor=scale_factor
                            )

                            interpolator.set_method(model)
                            interpolator.load_image(origin_img)
                            interpolator.save_interpolated_img(dest_img)

                        elif method.lower() == 'deeplearning':
                            if scale_factor == 8 and model.lower() != 'vdsr':
                                print('MODEL NOT EXIST')
                                continue
                            if scale_factor == 3 and model.lower() == 'lapsrn':
                                print('MODEL NOT EXIST')
                                continue

                            deepLearningProcessor = DeepLearningProcessor(
                                scale_factor=scale_factor,
                                method=model
                            )
                            deepLearningProcessor.image = origin_img

                            if model.lower() == 'vdsr':
                                for pre in ['bilinear', 'bicubic', 'nearest', 'lanczos']:
                                    dest_img = '{current_dir}/../dataset/UpSampled/{data_set}/' \
                                               '{raw_name}_{model}_{pre}x{scale}.{ext}' \
                                        .format(data_set=data_set, raw_name=raw_name, scale=scale_factor,
                                                ext=ext_name, current_dir=current_dir, model=model, pre=pre)
                                    if os.path.exists(dest_img):
                                        print('>>>>>>>>>>>>>>  EXIST')
                                        continue

                                    deepLearningProcessor.pre_interpolation = pre
                                    processed_img = deepLearningProcessor.processed_result()
                                    ImageSaver(dest_img, processed_img)

                            else:
                                dest_img = '{current_dir}/../dataset/UpSampled/{data_set}/' \
                                           '{raw_name}_{model}x{scale}.{ext}' \
                                    .format(data_set=data_set, raw_name=raw_name, scale=scale_factor,
                                            ext=ext_name, current_dir=current_dir, model=model)
                                if os.path.exists(dest_img):
                                    print('>>>>>>>>>>>>>>  EXIST')
                                    continue

                                processed_img = deepLearningProcessor.processed_result()

                                ImageSaver(dest_img, processed_img)

                        elif method.lower() == 'edgepreserve':
                            dest_img = '{current_dir}/../dataset/UpSampled/{data_set}/' \
                                       '{raw_name}_{model}x{scale}.{ext}' \
                                .format(data_set=data_set, raw_name=raw_name, scale=scale_factor,
                                        ext=ext_name, current_dir=current_dir, model=model)
                            if os.path.exists(dest_img):
                                print('>>>>>>>>>>>>>>  EXIST')
                                continue
                            if scale_factor == 3:
                                print("not supporting scale factor")
                                continue

                            edgePreserveProcessor = EdgePreserveProcessor(
                                scale_factor=scale_factor,
                                method=model
                            )
                            edgePreserveProcessor.image = origin_img
                            processed_img = edgePreserveProcessor.processed_result()
                            ImageSaver(dest_img, processed_img)

                        print('\t\t>>{destination} >>>>>>>>>>>>>>  DONE'
                              .format(destination=dest_img))


def getIQAInfos(current_dir):
    data_sets = os.listdir('{current_dir}/../dataset/GroundTruth'.format(current_dir=current_dir))
    result_df = pd.read_csv('./result.csv')
    done_list = set(result_df['Unnamed: 0'].to_list())

    for scale_factor in [
        2,
        3,
        4,
        8
    ]:
        print("* CURRENT SCALE: {factor}".format(factor=scale_factor))

        for data_idx, data_set in enumerate(data_sets):
            if data_set == '.DS_Store':
                continue
            print("\t* CURRENT DATASET: {dataset} >> {idx}/{total}"
                  .format(dataset=data_set, idx=data_idx + 1, total=len(data_sets)))

            images = os.listdir('{current_dir}/../dataset/GroundTruth/{data_set}'
                                .format(data_set=data_set, current_dir=current_dir))

            for img_idx, image in enumerate(images):
                raw_name = image.split('.')[0]
                ext_name = image.split('.')[-1]

                if '{image}x{scale}'.format(image=raw_name, scale=scale_factor) in done_list:
                    continue

                results = dict()
                if image == '.DS_Store':
                    continue
                print('{data_set}/{image} >> {idx}/{total}'.format(
                    data_set=data_set, current_dir=current_dir, image=image, idx=img_idx + 1, total=len(images)
                ))

                imageLoader.image_directory = '{current_dir}/../dataset/GroundTruth/{data_set}/{image}' \
                    .format(data_set=data_set, current_dir=current_dir, image=image)
                imageLoader.load_image()
                original_image = imageLoader.image_array

                down_img_name = '{raw_name}x{scale}'.format(raw_name=raw_name, scale=scale_factor)

                for pred in sorted(glob.glob(
                        '{current_dir}/../dataset/UpSampled/{data_set}/{raw_name}*x{scale}.{ext}'.format(
                            data_set=data_set,
                            current_dir=current_dir,
                            raw_name=raw_name,
                            scale=scale_factor,
                            ext=ext_name
                        ))):

                    up_method = method_search.findall(pred)[0]

                    imageLoader.image_directory = pred
                    imageLoader.load_image()
                    predictedImage = imageLoader.image_array

                    if down_img_name not in results.keys():
                        results[down_img_name] = dict()

                    if up_method not in results[down_img_name].keys():
                        results[down_img_name][up_method] = dict()

                    iqa_metrics.originalImage = original_image
                    iqa_metrics.predictedImage = predictedImage

                    results[down_img_name][up_method] = iqa_metrics.get_result(_with='dict')

                if not results:
                    continue

                cur_img_result = pd.DataFrame.from_dict({(i, j): results[i][j]
                                                         for i in results.keys()
                                                         for j in results[i].keys()},
                                                        orient='index')

                cur_img_result = cur_img_result.stack().unstack(level=1)

                if not os.path.exists('./result.csv'):
                    cur_img_result.to_csv('./result.csv', mode='w')
                else:
                    cur_img_result.to_csv('./result.csv', mode='a', header=False)


def addIQAInfos(current_dir):
    data_sets = os.listdir('{current_dir}/../dataset/GroundTruth'.format(current_dir=current_dir))
    data_sets.reverse()
    result_df = pd.read_csv('./result_plus.csv')
    done_list = set(result_df['Unnamed: 0'].to_list())

    for scale_factor in [
        2,
        3,
        4,
        8
    ]:
        print("* CURRENT SCALE: {factor}".format(factor=scale_factor))

        for data_idx, data_set in enumerate(data_sets):
            if data_set == '.DS_Store':
                continue
            print("\t* CURRENT DATASET: {dataset} >> {idx}/{total}"
                  .format(dataset=data_set, idx=data_idx + 1, total=len(data_sets)))

            images = os.listdir('{current_dir}/../dataset/GroundTruth/{data_set}'
                                .format(data_set=data_set, current_dir=current_dir))

            for img_idx, image in enumerate(images):
                raw_name = image.split('.')[0]
                ext_name = image.split('.')[-1]

                if '{image}x{scale}'.format(image=raw_name, scale=scale_factor) in done_list:
                    continue

                results = dict()
                if image == '.DS_Store':
                    continue
                print('{data_set}/{image} >> {idx}/{total}'.format(
                    data_set=data_set, current_dir=current_dir, image=image, idx=img_idx + 1, total=len(images)
                ))

                imageLoader.image_directory = '{current_dir}/../dataset/GroundTruth/{data_set}/{image}' \
                    .format(data_set=data_set, current_dir=current_dir, image=image)
                imageLoader.load_image()
                original_image = imageLoader.image_array

                down_img_name = '{raw_name}x{scale}'.format(raw_name=raw_name, scale=scale_factor)

                for pred in sorted(glob.glob(
                        '{current_dir}/../dataset/UpSampled/{data_set}/{raw_name}*x{scale}.{ext}'.format(
                            data_set=data_set,
                            current_dir=current_dir,
                            raw_name=raw_name,
                            scale=scale_factor,
                            ext=ext_name
                        ))):
                    print(pred)
                    up_method = method_search.findall(pred)[0]

                    imageLoader.image_directory = pred
                    imageLoader.load_image()
                    predictedImage = imageLoader.image_array

                    if down_img_name not in results.keys():
                        results[down_img_name] = dict()

                    if up_method not in results[down_img_name].keys():
                        results[down_img_name][up_method] = dict()

                    iqa_metrics.originalImage = original_image
                    iqa_metrics.predictedImage = predictedImage

                    results[down_img_name][up_method] = {
                        'UIQ': iqa_metrics.UIQ,
                        # 'SRE': iqa_metrics.SRE,
                    }

                if not results:
                    continue

                cur_img_result = pd.DataFrame.from_dict({(i, j): results[i][j]
                                                         for i in results.keys()
                                                         for j in results[i].keys()},
                                                        orient='index')

                cur_img_result = cur_img_result.stack().unstack(level=1)

                if not os.path.exists('./result_plus.csv'):
                    cur_img_result.to_csv('./result_plus.csv', mode='w')
                else:
                    cur_img_result.to_csv('./result_plus.csv', mode='a', header=False)


if __name__ == '__main__':
    cur_dir = os.path.dirname(os.path.abspath(__file__))
    # downSample_dataSet(current_dir=cur_dir)
    # upSample_dataSet(current_dir=cur_dir)

    # Set5, Set14, Urban 100, BSD 100, Sun-Hays 80
    # getIQAInfos(cur_dir)
    addIQAInfos(cur_dir)
