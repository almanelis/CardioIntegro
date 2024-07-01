import os

def generate_conclusion(data, export_to_txt = False, output_dir = None):

    '''
    INPUT
    data: dict - A dictionary containing statistical parameters of the cardiac rhythm.
    output_dir: str - The directory path to save the conclusion text file.

    RETURN
    conclusion_text: str - Textual summary of the cardiac rhythm analysis based on the input data. The conclusion is also saved as a text file in the specified directory.
    '''
    conclusion = []

    # Check and generate conclusion for M
    try:
        M = data['M']
        if M < 0.5:
            conclusion.append("Математическое ожидание по всему ряду пульсовых интервалов указывает на Выраженную Тахикардию.")
        elif 0.5 <= M < 0.66:
            conclusion.append("Математическое ожидание по всему ряду пульсовых интервалов указывает на Тахикардию.")
        elif 0.66 <= M < 0.76:
            conclusion.append("Математическое ожидание по всему ряду пульсовых интервалов указывает на Умеренную Тахикардию.")
        elif 0.75 <= M < 0.9:
            conclusion.append("Математическое ожидание по всему ряду пульсовых интервалов указывает на Нормальный пульс.")
        elif 0.9 <= M < 1.0:
            conclusion.append("Математическое ожидание по всему ряду пульсовых интервалов указывает на Умеренную Брадикардию.")
        elif 1.0 <= M < 1.2:
            conclusion.append("Математическое ожидание по всему ряду пульсовых интервалов указывает на Брадикардию.")
        elif M > 1.2:
            conclusion.append("Математическое ожидание по всему ряду пульсовых интервалов указывает на Выраженную Брадикардию.")
    except (KeyError, TypeError) as e:
        pass

    # Check and generate conclusion for SCO
    try:
        SCO = data['SCO']
        if SCO < 0.03:
            conclusion.append("Среднеквадратичное отклонение по всему ряду пульсовых интервалов указывает на стабильный(ригидный) ритм - стеноз артерии, снабжающая синусовый узел.")
        elif 0.03 <= SCO <= 0.06:
            conclusion.append("Среднеквадратичное отклонение по всему ряду пульсовых интервалов в норме - нормальная вериабельность ритма.")
        elif 0.06 < SCO < 0.1:
            conclusion.append("Среднеквадратичное отклонение по всему ряду пульсовых интервалов указывает на наличие аритмии сердца.")
        elif SCO > 0.1:
            conclusion.append("Среднеквадратичное отклонение по всему ряду пульсовых интервалов указывает на выраженную аритмию сердца.")
    except (KeyError, TypeError) as e:
        pass

    # Check and generate conclusion for coefficient_cov
    try:
        coefficient_cov = data['coefficient_cov']
        if 3 <= coefficient_cov <= 5:
            conclusion.append("Коэффициент вариации указывает на нормальный ритм сердца.")
        elif coefficient_cov > 10:
            conclusion.append("Коэффициент вариации указывает на нарушение ритмичности сердца.")
        elif coefficient_cov > 5:
            conclusion.append("Коэффициент вариации указывает о нарастании аритмичности сердца.")
        elif coefficient_cov < 3:
            conclusion.append("Коэффициент вариации указывает о стабилизации ритма сердца.")
    except (KeyError, TypeError) as e:
        pass

    # Check and generate conclusion for amplitude
    try:
        amplitude = data['amplitude']
        if 20 <= amplitude < 50:
            conclusion.append("Значение амплитуды в норме - стабильное воздействие симпатического отдела нервной системы.")
        else:
            conclusion.append("Значение амплитуды не в норме - нестабильное воздействие симпатического отдела нервной системы.")
    except (KeyError, TypeError) as e:
        pass

    # Check and generate conclusion for delta_x
    try:
        delta_x = data['delta_x']
        if 0.15 <= delta_x <= 0.3:
            conclusion.append("Значение вариационного размаха в норме - оценка фоновых аритмий и состояния вегетативного гомеостаза.")
        else:
            conclusion.append("Значение вариационного размаха не в норме - оценка фоновых аритмий и состояния вегетативного гомеостаза.")
    except (KeyError, TypeError) as e:
        pass

    # Check and generate conclusion for index
    try:
        index = data['index']
        if 100 <= index <= 300:
            conclusion.append("Индекс Вегетативного равновесия в норме, нет гипертонуса симпатического отдела.")
        elif index > 300:
            conclusion.append("Индекс Вегетативного равновесия повышен, гипертонус симпатического отдела, снижение ваготонии.")
        elif index < 100:
            conclusion.append("Индекс Вегетативного равновесия понижен, повышение ваготонии.")
    except (KeyError, TypeError) as e:
        pass

    # Check and generate conclusion for vri
    try:
        vri = data['vri']
        if 7.1 <= vri <= 9.3:
            conclusion.append("Вегетативный показатель ритма в норме - вегетативный баланс.")
        elif vri < 7.1:
            conclusion.append("Вегетативный показатель ритма не в норме - преобладание парасимпатического отдела.")
        elif vri > 9.3:
            conclusion.append("Вегетативный показатель ритма не в норме - преобладание симпатического отдела.")
    except (KeyError, TypeError) as e:
        pass

    # Check and generate conclusion for iarp
    try:
        iarp = data['iarp']
        if 35 <= iarp <= 70:
            conclusion.append("Показатель адекватности процессов регуляции в норме - централизация управления ритмом.")
        elif iarp > 70:
            conclusion.append("Показатель адекватности процессов регуляции выше нормы - недостаточная централизация управления ритмом.")
        elif iarp < 35:
            conclusion.append("Показатель адекватности процессов регуляции ниже нормы - избыточная централизация управления ритмом.")
    except (KeyError, TypeError) as e:
        pass

    # Check and generate conclusion for sib
    try:
        sib = data['sib']
        if 50 <= sib <= 200:
            conclusion.append("Индекс напряжения Баевского в норме - степень централизации управления ритмом.")
        elif 200 < sib <= 500:
            conclusion.append("Индекс напряжения Баевского увеличен - эмоциональный стресс или физическая работа.")
        elif 500 < sib <= 600:
            conclusion.append("Индекс напряжения Баевского увеличен - стенокардия.")
        elif 600 < sib < 900:
            conclusion.append("Индекс напряжения Баевского увеличен - прединфарктное состояние.")
        elif sib >= 900:
            conclusion.append("Индекс напряжения Баевского сильно увеличен - прединфарктное состояние.")
        elif sib < 50:
            conclusion.append("Индекс напряжения Баевского понижен - ваготония.")
    except (KeyError, TypeError) as e:
        pass

    conclusion_text = '\n'.join(conclusion)

    # Save to a file
    if (export_to_txt):

        if output_dir is None:
            raise ValueError("Укажите директорию для сохранения файла.")

        output_path = os.path.join(output_dir, 'conclusion.txt')
        with open(output_path, 'w', encoding='utf-8') as file:
            file.write(conclusion_text)

    return conclusion_text