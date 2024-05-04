import os
import uuid

import matplotlib.pyplot as plt
import pandas as pd
import neurokit2 as nk
import h5py


UPLOAD_DIR = 'files/plots/'


def ecg_analyse_process(filepath: os.path):
    # Генерация уникального имени файла с расширением .png
    unique_filename1 = str(uuid.uuid4()) + '_result1.png'
    unique_filename2 = str(uuid.uuid4()) + '_result2.png'
    unique_filename3 = str(uuid.uuid4()) + '_result3.png'

    # первый анализ
    start_sample = 1_857_940  # 1_554_940
    stop_sample = 1_859_940  # 1_557_030 1_859_940
    data = h5py.File(filepath, 'r')
    ecg_data = data['ECG']
    time_to_record = data['num_data_records']
    sampling_rate = 1/(time_to_record[0][0]/len(ecg_data))
    ecg_data_pd = pd.DataFrame(
        {"Voltage": ecg_data[i][0]} for i in range(start_sample, stop_sample)
        )
    cleaned_ECG_array = nk.ecg_clean(
        ecg_data_pd['Voltage'],
        sampling_rate=sampling_rate,
        method='neurokit'
        )
    cleaned_df = pd.DataFrame(data=cleaned_ECG_array, columns=["ECG"])
    cleaned_ecg = cleaned_df['ECG']
    _, waves = nk.ecg_delineate(
        cleaned_ecg,
        rpeaks=None,
        sampling_rate=sampling_rate,
        method='dwt', show=False
        )

    output_list = []

    for P_start, P_end in zip(waves["ECG_P_Onsets"], waves["ECG_P_Offsets"]):

        if (str(P_start) == 'nan') or (str(P_end) == 'nan'):
            p_set = float('nan')

    else:
        duartion = float((P_end-P_start)/sampling_rate)
        p_set = (P_start, duartion)

    output_list.append(p_set)

    plt.switch_backend('AGG')
    plt.figure(figsize=(15, 10))
    nk.events_plot([waves['ECG_P_Onsets'], waves['ECG_P_Offsets']],
                   cleaned_ecg,
                   color=['red', 'green'])
    plt.title('P-peaks')
    plt.xlabel('Samples')
    plt.ylabel('Voltage')
    plt.savefig(UPLOAD_DIR + unique_filename1, format='png')
    plt.close('all')

    _, rpeaks = nk.ecg_peaks(cleaned_ecg,
                             sampling_rate=sampling_rate,
                             correct_artifacts=True)

    # второй анализ
    output_list = []

    for R_number in range(len(rpeaks['ECG_R_Peaks'])-1):

        R_end = rpeaks['ECG_R_Peaks'][R_number+1]
        R_start = rpeaks['ECG_R_Peaks'][R_number]

        duartion = float((R_end-R_start)/sampling_rate)
        r_set = (R_start, duartion)

        output_list.append(r_set)

    plt.switch_backend('AGG')
    plt.figure(figsize=(10, 5))
    nk.events_plot(rpeaks['ECG_R_Peaks'], cleaned_ecg)
    plt.xlabel('Samples')
    plt.ylabel('Voltage')
    plt.title('RR-intervals')
    plt.savefig(UPLOAD_DIR + unique_filename2, format='png')
    plt.close('all')

    _, waves = nk.ecg_delineate(cleaned_ecg, rpeaks=None,
                                sampling_rate=sampling_rate,
                                method='dwt', show=False)

    # третий анализ
    output_list = []

    index = 0
    nan_index = []

    if waves["ECG_R_Onsets"][0] > waves["ECG_R_Offsets"][0]:
        waves["ECG_R_Offsets"].pop(0)
        waves["ECG_R_Onsets"].pop(-1)

    for QRS_start, QRS_end in zip(waves["ECG_R_Onsets"],
                                  waves["ECG_R_Offsets"]):

        if (str(QRS_start) == 'nan') or (str(QRS_end) == 'nan'):
            nan_index.append(index)
        elif (QRS_start > QRS_end):
            nan_index.append(index)

        index += 1

    for index in sorted(nan_index, reverse=True):
        waves["ECG_R_Onsets"].pop(index)
        waves["ECG_R_Offsets"].pop(index)

    for QRS_start, QRS_end in zip(waves["ECG_R_Onsets"],
                                  waves["ECG_R_Offsets"]):

        duartion = float((QRS_end-QRS_start)/sampling_rate)
        qrs_set = (QRS_start, duartion)
        output_list.append(qrs_set)

    plt.switch_backend('AGG')

    plt.figure(figsize=(10, 5))
    nk.events_plot([waves['ECG_R_Onsets'], waves['ECG_R_Offsets']],
                   cleaned_ecg, color=['red', 'green'])
    plt.title('QRS-compexes')
    plt.xlabel('Samples')
    plt.ylabel('Voltage')
    plt.savefig(UPLOAD_DIR + unique_filename3, format='png')
    plt.close('all')

    return ('plots/' + unique_filename1,
            'plots/' + unique_filename2,
            'plots/' + unique_filename3)


# ecg_analyse('uploads/01_ECG_01.mat')
