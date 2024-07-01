import logging

import pandas as pd
import numpy as np
import neurokit2 as nk

logging.basicConfig(level=logging.INFO, filename="log_ECG_features.log",
                    format="%(asctime)s %(levelname)s %(message)s")

def find_best_ecg_channel(cleaned_ecg:pd.DataFrame) -> str:
  """
  Функция для определения канала ЭКГ с наилучшим качеством сигнала из набора данных ЭКГ.

  Аргументы:
    cleaned_ecg (pd.DataFrame): DataFrame, содержащий очищенные данные ЭКГ, где столбцы соответствуют каналам ЭКГ, а строки - временным точкам.

  Возвращает:
    best_channel (str): Название канала ЭКГ с наилучшим качеством сигнала.
  """
  # Переводим микровольты в милливольты
  cleaned_ecg = cleaned_ecg / 1000

  # Рассчитываем лучший из 12 каналов ECG
  best_quality = -1
  best_channel = None

  # Проходим по каждому каналу ECG в таблице
  for channel_ind in range(len(cleaned_ecg)):
      try:
          signal_quality = nk.ecg_quality(cleaned_ecg.iloc[channel_ind])  # Расчет качества сигнала
      except (ValueError, IndexError, ZeroDivisionError) as e:
          logging.info(f'Type of error is: {e}\nThe channel: {channel_ind} could not calculate the quality in the file.')

      average_quality = np.max(np.mean(signal_quality, axis=0))  # Среднее значение качества по всем отведениям

      if average_quality > best_quality:
          best_quality = average_quality
          best_channel = channel_ind

  return best_channel