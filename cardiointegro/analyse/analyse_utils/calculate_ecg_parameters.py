import numpy as np
from scipy import stats

def calculate_ecg_parameters(output_dict, cleaned_ecg):
    """
    Функция принимает на вход:
    output_dict = {'best_channel': INDEX,'RR': [], ...};
    cleaned_ecg (pd.DataFrame): DataFrame, содержащий очищенные данные ЭКГ, где столбцы соответствуют каналам ЭКГ, а строки - временным точкам
    """

    best_channel = output_dict['best_channel']
    parameters = {}
    try:
        def calculate_M(output_dict): # Мат. ожидание RR зубцов (М)
            try:
                  if 'RR' in output_dict:
                      RR_values = output_dict['RR']
                      M = sum(RR_values) / len(RR_values)
                      return M
                  else:
                      return None

            except Exception as e:
                # print(f"Error in calculate_M: {e}")
                return None

        def calculate_SCO(cleaned_ecg, best_channel): # среднеквадратичное отклонение (SCO) для best_channel в cleaned_ecg
            try:
                values = cleaned_ecg[best_channel]
                SCO = np.std(values)
                return SCO
            except Exception as e:
                # print(f"Error in calculate_SCO: {e}")
                return None

        def calculate_coefficient_cov(cleaned_ecg, best_channel): # коэффициент вариации (coefficient_cov) для best_channel в cleaned_ecg
            try:
                values = cleaned_ecg[best_channel]
                mean = np.mean(values)
                std = np.std(values)
                coefficient_cov = std / mean
                return coefficient_cov
            except Exception as e:
                # print(f"Error in calculate_coefficient_cov: {e}")
                return None

        def calculate_amplitude(cleaned_ecg, best_channel): # амплитуду моды распределения (amplitude) для best_channel в cleaned_ecg
            try:
                values = cleaned_ecg[best_channel]
                mode = stats.mode(values)[0][0]
                amplitude = mode - np.mean(values)
                return amplitude
            except Exception as e:
                # print(f"Error in calculate_amplitude: {e}")
                return None

        def calculate_delta_x(cleaned_ecg, best_channel): # вариационный размах (delta_x) для best_channel в cleaned_ecg
            try:
                values = cleaned_ecg[best_channel]
                delta_x = np.max(values) - np.min(values)
                return delta_x
            except Exception as e:
                # print(f"Error in calculate_delta_x: {e}")
                return None

        def calculate_index(cleaned_ecg, best_channel): # индекс вегетатичного равновесия (index) для best_channel в cleaned_ecg
            try:
                values = cleaned_ecg[best_channel]
                index = np.mean(values) / np.std(values)
                return index
            except Exception as e:
                # print(f"Error in calculate_index: {e}")
                return None

        def calculate_vri(cleaned_ecg, best_channel): # вегетатичный показатель ритма (vri) для best_channel в cleaned_ecg
            try:
                values = cleaned_ecg[best_channel]
                vri = np.std(values) / np.mean(values)
                return vri
            except Exception as e:
                # print(f"Error in calculate_vri: {e}")
                return None

        def calculate_iarp(cleaned_ecg, best_channel): # показатель адекватности процессов регуляции (iarp) для best_channel в cleaned_ecg
            try:
                values = cleaned_ecg[best_channel]
                iarp = np.mean(values) / np.std(values)
                return iarp
            except Exception as e:
                # print(f"Error in calculate_iarp: {e}")
                return None

        def calculate_sib(cleaned_ecg, best_channel): # Индекс напряжения Баевского (sib) для best_channel в cleaned_ecg
            try:
                values = cleaned_ecg[best_channel]
                sib = np.max(values) / np.min(values)
                return sib
            except Exception as e:
                # print(f"Error in calculate_sib: {e}")
                return None

        parameters = {
            'M': calculate_M(output_dict),
            'SCO': calculate_SCO(cleaned_ecg, best_channel),
            'coefficient_cov': calculate_coefficient_cov(cleaned_ecg, best_channel),
            'amplitude': calculate_amplitude(cleaned_ecg, best_channel),
            'delta_x': calculate_delta_x(cleaned_ecg, best_channel),
            'index': calculate_index(cleaned_ecg, best_channel),
            'vri': calculate_vri(cleaned_ecg, best_channel),
            'iarp': calculate_iarp(cleaned_ecg, best_channel),
            'sib': calculate_sib(cleaned_ecg, best_channel)
        }
        return parameters
    except Exception as e:
        # print(f"Error: {e}")
        return None
