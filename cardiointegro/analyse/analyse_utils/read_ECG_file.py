import logging

import pandas as pd
from pymatreader import read_mat

logging.basicConfig(level=logging.INFO, filename="log_ECG_features.log",
                    format="%(asctime)s %(levelname)s %(message)s")


def read_ECG_file(ecg_file):
    """
    Функция для чтения ЭКГ из mat или feather формата файла.

    Аргументы:
        ecg_file (TemporaryUploadedFile): файл ЭКГ
    Возвращает:
        ecg_df (pd.DataFrame): Датафрейм с каналами ЭКГ записи
    """
    if ecg_file.name.endswith('.mat'):
        data = read_mat(ecg_file)
        try:
            ecg_df = pd.DataFrame(data['val'])
        except KeyError:
            try:
                ecg_df = pd.DataFrame(data)
            except ValueError as e:
                logging.error(f'The file with the extension .mat does not meet the standard.\nFile name is: {ecg_file.name} \nType of error is: {e}')
    else:
        try:
            ecg_df = pd.read_feather(ecg_file)
        except TypeError as e:
            logging.error(f'The file does not belong to the feather format.\nFile name is: {ecg_file.name} \nType of error is: {e}')

    return ecg_df
