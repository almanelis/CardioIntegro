import pandas as pd

from . import find_best_ecg_channel
from . import notice_ecg_feature_all


def exchange_ecg_features(cleaned_ecg:pd.DataFrame, sampling_rate:float, features:list[str], reference_millivolt:float=10) -> dict and dict:
    """
    Функция для определения канала ЭКГ с наилучшим качеством сигнала и расчета параметров ЭКГ для этого канала.

    Аргументы:
        cleaned_ecg (pd.DataFrame): DataFrame, содержащий очищенные данные ЭКГ, где столбцы соответствуют каналам ЭКГ, а строки - временным точкам.
        sampling_rate (float): Частота дискретизации ЭКГ сигнала.
        reference_millivolt (float, 10): Опорное значение в милливольтах для нормализации ЭКГ сигнала.
        features (list[str]): Выбранные признаки из ЭКГ

    Возвращает:
        list: Список, содержащий лучший канал ЭКГ и словарь с параметрами ЭКГ для этого канала.
    """
    # Поиск наилучшего канала для дальнейшей работы с ним
    best_channel = find_best_ecg_channel(cleaned_ecg)

    ECG_parameters_temp = {'best_channel': best_channel}

    # Рассчитываем необходимые параметры и сохраняем их
    detected_features, plots_dict = notice_ecg_feature_all(
        cleaned_ecg.iloc[best_channel],
        feature=features,
        sampling_rate=sampling_rate,
        reference_millivolt=reference_millivolt
    )
    ECG_parameters_temp.update(detected_features)

    return ECG_parameters_temp, plots_dict
