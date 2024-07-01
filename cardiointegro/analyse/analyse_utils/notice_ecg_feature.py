import pandas as pd
import numpy as np
import neurokit2 as nk
import uuid

from .CardioKit import CardioKit


def notice_ecg_feature_all(cleaned_ecg: pd.DataFrame, sampling_rate: float, reference_millivolt: float = 10, show: bool = True, feature: list = ['all']) -> dict:
    """
    Функция выполняет комплексный анализ ЭКГ сигнала, извлекая характеристики,
    связанные с амплитудой, длительностью и морфологией волн, сегментов и интервалов.

    Аргументы:
        cleaned_ecg (Union[list, np.array, pd.Series]): Очищенный ЭКГ сигнал.
        sampling_rate (int): Частота дискретизации ЭКГ сигнала.
        reference_millivolt (int, 10): Справочный милливольт для расчета амплитуды.
        show (bool, optional): Если True, то функция отобразит графики
                               с обнаруженными волнами, интервалами и амплитудами.
                               По умолчанию False.
        feature (str, optional): Тип анализа ЭКГ сигнала. Доступные значения:
                                       'all' (по умолчанию), 'RR', 'QRS', 'P_peak', 'T_peak', 'PQ_segment',
                                       'PQ_interval', 'ST_segment', 'ST_interval', 'QT_interval', 'TP_interval', 'R_peak',
                                       'P_amplitude', 'T_amplitude', 'Q_amplitude'.

    Возвращает:
        output_dict (dict): Словарь с результатами анализа. Каждый ключ соответствует типу анализа,
                            а значения представляют собой список соответствующих характеристик.
    """

    save_dir = 'files/plots/'

    plots_dict = {
        'plot1': save_dir + 'Best_channel_record' + str(uuid.uuid4()) + '.png',
        'plot2': save_dir + 'Average_peaks' + str(uuid.uuid4()) + '.png',
        'plot3': save_dir + 'RR_intervals' + str(uuid.uuid4()) + '.png',
        'plot4': save_dir + 'EDR' + str(uuid.uuid4()) + '.png',
        'plot5': save_dir + 'qrs_epochs' + str(uuid.uuid4()) + '.png'
        }

    # Иннициализация класса
    ck = CardioKit()

    # Детектируем особенности ЭКГ
    info, rpeaks = nk.ecg_peaks(cleaned_ecg, sampling_rate=sampling_rate, correct_artifacts=True)

    # Получаем другие пики и отрисовываем Average_peaks с сохранением файла]
    _, waves = ck.ecg_delineate(cleaned_ecg, rpeaks=None, sampling_rate=sampling_rate, method='dwt', show=True, save_fig=True, fig_name=plots_dict['plot2'])

    # Инициализируем выходной словарь
    output_dict = {}

    # Отрисовка каналов
    ck.signal_plot(cleaned_ecg, sampling_rate=sampling_rate, subplots=False, standardize=False, labels=None, show_legend=False, save_fig=True, fig_name=plots_dict['plot1'])

    if 'all' in feature or  'Average' in feature:
      qrs_epochs = ck.ecg_segment(cleaned_ecg, rpeaks=None, sampling_rate=sampling_rate, show=True, show_legend=False, save_fig=True, fig_name=plots_dict['plot5'])


    if 'all' in feature or 'EDR' in feature:
      # Отрисовка EDR
      ecg_rate = nk.signal_rate(info, sampling_rate=sampling_rate, desired_length=len(info)) # Get heart rate
      EDR = nk.ecg_rsp(ecg_rate, sampling_rate=sampling_rate)
      ck.signal_plot([EDR], standardize = True, sampling_rate=sampling_rate, subplots=False, labels=None, show_legend=False, save_fig=True, fig_name=plots_dict['plot4'])


    if 'all' in feature or 'RR' in feature:

        if len('ECG_R_Peaks') > 2:
            # 1. Детекция RR-интервалов
            for R_number in range(len(rpeaks['ECG_R_Peaks']) - 1):
                R_end = rpeaks['ECG_R_Peaks'][R_number + 1]
                R_start = rpeaks['ECG_R_Peaks'][R_number]
                duration = float((R_end - R_start) / sampling_rate)
                output_dict.setdefault('RR', []).append(duration)
        else:
            output_dict.setdefault('RR', []).append('Nan')
        if show:
          # Отрисовка R пиков
          ck.events_plot(rpeaks['ECG_R_Peaks'], cleaned_ecg, show_legend=False, save_fig=True, fig_name=plots_dict['plot3'])

    if 'all' in feature or 'QRS' in feature:
        # 2.1 Детекция QRS-комплексов
        index = 0
        nan_index = []

        if 'ECG_R_Onsets' in waves and 'ECG_R_Offsets' in waves:

            if waves["ECG_R_Onsets"][0] > waves["ECG_R_Offsets"][0]:
                waves["ECG_R_Offsets"].pop(0)
                waves["ECG_R_Onsets"].pop(-1)
            for QRS_start, QRS_end in zip(waves["ECG_R_Onsets"], waves["ECG_R_Offsets"]):
                if (str(QRS_start) == 'nan') or (str(QRS_end) == 'nan'):
                    nan_index.append(index)
                elif (QRS_start > QRS_end):
                    nan_index.append(index)
                index += 1
            for index in sorted(nan_index, reverse=True):
                waves["ECG_R_Onsets"].pop(index)
                waves["ECG_R_Offsets"].pop(index)
            for QRS_start, QRS_end in zip(waves["ECG_R_Onsets"], waves["ECG_R_Offsets"]):
                duration = float((QRS_end - QRS_start) / sampling_rate)
                output_dict.setdefault('QRS', []).append(duration)
        else:
            output_dict.setdefault('QRS', []).append('Nan')

    if 'all' in feature or 'P_peak' in feature:
        # 2.2 Детекция P-пиков

        if 'ECG_P_Onsets' in waves and 'ECG_P_Offsets' in waves:

            for P_start, P_end in zip(waves["ECG_P_Onsets"], waves["ECG_P_Offsets"]):
                if (str(P_start) == 'nan') or (str(P_end) == 'nan'):
                    p_set = float('nan')
                else:
                    duration = float((P_end - P_start) / sampling_rate)
                output_dict.setdefault('P_peak', []).append(duration)
        else:
            output_dict.setdefault('P_peak', []).append('Nan')

    if 'all' in feature or 'T_peak' in feature:
        # 2.3 Детекция T-пиков

        if 'ECG_T_Onsets' in waves and 'ECG_T_Offsets' in waves:

              for T_start, T_end in zip(waves["ECG_T_Onsets"], waves["ECG_T_Offsets"]):
                  if (str(T_start) == 'nan') or (str(T_end) == 'nan'):
                      t_set = float('nan')
                  else:
                      duration = float((T_end - T_start) / sampling_rate)
                  output_dict.setdefault('T_peak', []).append(duration)
        else:
            output_dict.setdefault('T_peak', []).append('Nan')

    if 'all' in feature or 'PQ_segment' in feature:
        # 2.4 Детекция PQ-сегментов
        index = 0
        nan_index = []

        if 'ECG_P_Offsets' in waves and 'ECG_R_Onsets' in waves:

            if waves["ECG_P_Offsets"][0] > waves["ECG_R_Onsets"][0]:
                waves["ECG_R_Onsets"].pop(0)
                waves["ECG_P_Offsets"].pop(-1)
            for PQ_start, PQ_end in zip(waves["ECG_P_Offsets"], waves["ECG_R_Onsets"]):
                if (str(PQ_start) == 'nan') or (str(PQ_end) == 'nan'):
                    nan_index.append(index)
                elif (PQ_start > PQ_end):
                    nan_index.append(index)
                index += 1
            for index in sorted(nan_index, reverse=True):
                waves["ECG_P_Offsets"].pop(index)
                waves["ECG_R_Onsets"].pop(index)
            for PQ_start, PQ_end in zip(waves["ECG_P_Offsets"], waves["ECG_R_Onsets"]):
                duration = float((PQ_end - PQ_start) / sampling_rate)
                output_dict.setdefault('PQ_segment', []).append(duration)
        else:
            output_dict.setdefault('PQ_segment', []).append('Nan')

    if 'all' in feature or 'PQ_interval' in feature:
        # 2.5 Детекция PQ-интервалов
        index = 0
        nan_index = []

        if 'ECG_P_Onsets' in waves and 'ECG_R_Onsets' in waves:

            if (waves["ECG_P_Onsets"][0] > waves["ECG_R_Onsets"][0]):
                waves["ECG_R_Onsets"].pop(0)
                waves["ECG_P_Onsets"].pop(-1)
            for PQ_start, PQ_end in zip(waves["ECG_P_Onsets"], waves["ECG_R_Onsets"]):
                if (str(PQ_start) == 'nan') or (str(PQ_end) == 'nan'):
                    nan_index.append(index)
                elif (PQ_start > PQ_end):
                    nan_index.append(index)
                index += 1
            for index in sorted(nan_index, reverse=True):
                waves["ECG_P_Onsets"].pop(index)
                waves["ECG_R_Onsets"].pop(index)
            for PQ_start, PQ_end in zip(waves["ECG_P_Onsets"], waves["ECG_R_Onsets"]):
                duration = float((PQ_end - PQ_start) / sampling_rate)
                output_dict.setdefault('PQ_interval', []).append(duration)
        else:
            output_dict.setdefault('PQ_interval', []).append('Nan')

    if 'all' in feature or 'ST_segment' in feature:
        # 2.6 Детекция ST-сегментов
        index = 0
        nan_index = []

        if 'ECG_R_Offsets' in waves and 'ECG_T_Onsets' in waves:

            if waves["ECG_R_Offsets"][0] > waves["ECG_T_Onsets"][0]:
                waves["ECG_T_Onsets"].pop(0)
                waves["ECG_R_Offsets"].pop(-1)
            for ST_start, ST_end in zip(waves["ECG_R_Offsets"], waves["ECG_T_Onsets"]):
                if (str(ST_start) == 'nan') or (str(ST_end) == 'nan'):
                    nan_index.append(index)
                elif (ST_start > ST_end):
                    nan_index.append(index)
                index += 1
            for index in sorted(nan_index, reverse=True):
                waves["ECG_R_Offsets"].pop(index)
                waves["ECG_T_Onsets"].pop(index)
            for ST_start, ST_end in zip(waves["ECG_R_Offsets"], waves["ECG_T_Onsets"]):
                duration = float((ST_end - ST_start) / sampling_rate)
                output_dict.setdefault('ST_segment', []).append(duration)
        else:
            output_dict.setdefault('ST_segment', []).append('Nan')

    if 'all' in feature or 'ST_interval' in feature:
        # 2.7 Детекция ST-интервалов
        index = 0
        nan_index = []

        if 'ECG_R_Offsets' in waves and 'ECG_T_Offsets' in waves:

            if waves["ECG_R_Offsets"] and waves["ECG_T_Offsets"] and len(waves["ECG_R_Offsets"]) > 0 and len(waves["ECG_T_Offsets"]) > 0:
                if waves["ECG_R_Offsets"][0] > waves["ECG_T_Offsets"][0]:
                    waves["ECG_T_Offsets"].pop(0)
                    waves["ECG_R_Offsets"].pop(-1)
            for ST_start, ST_end in zip(waves["ECG_R_Offsets"], waves["ECG_T_Offsets"]):
                if (str(ST_start) == 'nan') or (str(ST_end) == 'nan'):
                    nan_index.append(index)
                elif (ST_start > ST_end):
                    nan_index.append(index)
                index += 1
            for index in sorted(nan_index, reverse=True):
                waves["ECG_R_Offsets"].pop(index)
                waves["ECG_T_Offsets"].pop(index)
            for ST_start, ST_end in zip(waves["ECG_R_Offsets"], waves["ECG_T_Offsets"]):
                duration = float((ST_end - ST_start) / sampling_rate)
                output_dict.setdefault('ST_interval', []).append(duration)
        else:
            output_dict.setdefault('ST_interval', []).append('Nan')

    if 'all' in feature or 'QT_interval' in feature:
        # 2.8 Детекция QT-интервалов
        index = 0
        nan_index = []

        if "ECG_Q_Onsets" in waves and 'ECG_T_Offsets' in waves:

            if waves["ECG_R_Onsets"][0] > waves["ECG_T_Offsets"][0]:
                waves["ECG_T_Offsets"].pop(0)
                waves["ECG_R_Onsets"].pop(-1)
            for QT_start, QT_end in zip(waves["ECG_R_Onsets"], waves["ECG_T_Offsets"]):
                if (str(QT_start) == 'nan') or (str(QT_end) == 'nan'):
                    nan_index.append(index)
                elif (QT_start > QT_end):
                    nan_index.append(index)
                index += 1
            for index in sorted(nan_index, reverse=True):
                waves["ECG_R_Onsets"].pop(index)
                waves["ECG_T_Offsets"].pop(index)
            for QT_start, QT_end in zip(waves["ECG_R_Onsets"], waves["ECG_T_Offsets"]):
                duration = float((QT_end-QT_start)/sampling_rate)
                output_dict.setdefault('QT_interval', []).append(duration)
        else:
            output_dict.setdefault('QT_interval', []).append('Nan')

    if 'all' in feature or 'TP_interval' in feature:
        # 2.9 Детекция TP-интервалов
        index = 0
        nan_index = []

        if "ECG_T_Offsets" in waves and 'ECG_P_Onsets' in waves:

            if (waves["ECG_T_Offsets"][0] > waves["ECG_P_Onsets"][0]):
                waves["ECG_P_Onsets"].pop(0)
                waves["ECG_T_Offsets"].pop(-1)
            for TP_start, TP_end in zip(waves["ECG_T_Offsets"], waves["ECG_P_Onsets"]):
                if (str(TP_start) == 'nan') or (str(TP_end) == 'nan'):
                    nan_index.append(index)
                elif (TP_start > TP_end):
                    nan_index.append(index)
                index += 1
            for index in sorted(nan_index, reverse=True):
                waves["ECG_T_Offsets"].pop(index)
                waves["ECG_P_Onsets"].pop(index)
            for TP_start, TP_end in zip(waves["ECG_T_Offsets"], waves["ECG_P_Onsets"]):
                duration = float((TP_end - TP_start) / sampling_rate)
                output_dict.setdefault('TP_interval', []).append(duration)
        else:
              output_dict.setdefault('TP_interval', []).append('Nan')


    if 'all' in feature or 'R_peak' in feature:
        # 2.10 Детекция R-пиков

        if len(rpeaks['ECG_R_Peaks']) > 1:

            for R_peak in rpeaks['ECG_R_Peaks']:
                output_dict.setdefault('R_peak', []).append(R_peak)
        else:
            output_dict.setdefault('R_peak', []).append('Nan')

    if 'all' in feature or 'P_amplitude' in feature:
        # 2.11 Детекция амплитуд P-волн

        if 'ECG_P_Onsets' in waves and 'ECG_P_Peaks' in waves:

            for P_start, P_end in zip(waves["ECG_P_Onsets"], waves["ECG_P_Peaks"]):
                amplitude = np.amax(cleaned_ecg[int(P_start):int(P_end)])
                output_dict.setdefault('P_amplitude', []).append(amplitude)
        else:
            output_dict.setdefault('P_amplitude', []).append('Nan')

    if 'all' in feature or 'T_amplitude' in feature:
        # 2.12 Детекция амплитуд T-волн

        if 'ECG_T_Onsets' in waves and 'ECG_T_Peaks' in waves:

            for T_start, T_end in zip(waves["ECG_T_Onsets"], waves["ECG_T_Peaks"]):
                if np.isnan(T_start) or np.isnan(T_end):
                    output_dict.setdefault('T_amplitude', []).append('Nan')
                else:
                    amplitude = np.amax(cleaned_ecg[int(T_start):int(T_end)])
                    output_dict.setdefault('T_amplitude', []).append(amplitude)
        else:
            output_dict.setdefault('T_amplitude', []).append('Nan')

    if 'all' in feature or 'Q_amplitude' in feature:
        # 2.13 Детекция амплитуд Q-волн

        if 'ECG_Q_Onsets' in waves and 'ECG_Q_Peaks' in waves:

            for Q_start, Q_end in zip(waves["ECG_Q_Onsets"], waves["ECG_Q_Peaks"]):
                if np.isnan(Q_start) or np.isnan(Q_end):
                      output_dict.setdefault('Q_amplitude', []).append('Nan')
                else:
                    amplitude = np.amax(cleaned_ecg[int(Q_start):int(Q_end)])
                    output_dict.setdefault('Q_amplitude', []).append(amplitude)
        else:
            output_dict.setdefault('Q_amplitude', []).append('Nan')

    return output_dict, plots_dict