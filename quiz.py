import json
import os

def get_directory():
    """
    Запрашивает у пользователя путь к директории с викторинами

    :return: Путь к директории с викторинами
    """
    while True:
        directory = input("Введите путь к директории с викторинами (quiz_directory): ")
        
        if os.path.isdir(directory):  
            return directory
        else:
            print("Некорректный ввод")

def choose_quiz(directory):
    """
    Позволяет пользователю выбрать викторину из списка 

    :param directory: Директория с викторинами
    :return: Путь к выбранной викторине
    """
    quizzes = [f for f in os.listdir(directory) if f.endswith('.json')]  # cписок файлов викторин

    if not quizzes:
        print("В директории нет викторин")
        return None

    print("\nВикторины:")
    for i, quiz in enumerate(quizzes, start=1):
        print(f"{i}. {quiz}")

    ind_chose = None
    while ind_chose is None:
        try:
            choice = int(input("Выберите викторину, введя её номер: ")) - 1
            if 0 <= choice < len(quizzes):
                ind_chose = choice
            else:
                print("Некорректный ввод")
        except ValueError:
            print("Некорректный ввод")

    return os.path.join(directory, quizzes[ind_chose])

def load_quiz(path_q):
    """
    Загружает викторину из JSON файла

    :param path_q: Путь к файлу с викториной
    :return: Викторина в виде словаря
    """
    try:
        with open(path_q, 'r', encoding='utf-8') as file:
            return json.load(file) 
    except:
        print("Ошибка при загрузке")
        return None
    
def ask(data, num):
    """
    Задает вопрос пользователю и получает ответ

    :param data: Словарь с вопросом, вариантами ответов, правильным ответом и баллом
    :param num: Номер текущего вопроса
    :return: Правильный ответ или нет, баллы, выбранный вариант, правильный вариант
    """
    print(f"\nВопрос {num}: {data['question']}")
    for i, a in enumerate(data['options']):
        print(f"{i + 1}. {a}")  # вывод вариантов

    chosen = None
    while chosen is None:  # проверка на ввод
        try:
            print("Введите номер вашего ответа: ")
            chosen = int(input()) - 1 

            if chosen < 0 or chosen >= len(data["options"]):
                print("Некорректный ввод")
                chosen = None  

        except ValueError:
            print("Некорректный ввод")

    is_corr = chosen == data["correct_option"]  # проверка правильно ли
    score_one = data["score"] if is_corr else 0  # плюс баллы

    return is_corr, score_one, chosen, data["correct_option"]

def show_report(report):
    """
    Выводит подробный отчет 

    :param report: Список словарей с вопросами, вариантами и ответами
    :return: None
    """
    print("\nПодробный отчет:")
    for a, b in enumerate(report, start=1):
        print(f"\nВопрос {a}: {b['question']}")
        for i, option in enumerate(b["options"]):
            print(f"{i + 1}. {option}")  
        if b["chosen_option"] is not None:
            print(f"Ваш ответ: {b['options'][b['chosen_option']]}")  
        print(f"Правильный ответ: {b['options'][b['correct_option']]}")  

def run(quiz_data):
    """
    Запускает викторину и обрабатывает вопросы

    :param quiz_data: Словарь с данными викторины
    :return: None
    """
    cor_ans = 0  # счетчик правильных ответов
    inc_ans = 0  # счетчик неправильных ответов
    score = 0  # общий счет
    report = []  # отчет

    print(f"\nВикторина '{quiz_data['quiz_name']}' начинается!")

    for i, q in enumerate(quiz_data['questions'], start=1):
        is_corr, score_one, chosen, corr_opt = ask(q, i)

        # сохраняем для отчета
        report.append({
            "question": q["question"],
            "options": q["options"],
            "chosen_option": chosen,
            "correct_option": corr_opt
        })

        if is_corr:
            cor_ans += 1  
        else:
            inc_ans += 1 
        score += score_one 

    # итог
    print("\nВикторина завершена!")
    print(f"Правильных ответов: {cor_ans}/{len(quiz_data['questions'])}")
    print(f"Неправильных ответов: {inc_ans}/{len(quiz_data['questions'])}")
    print(f"Общий счет: {score}")

    # отчет
    show_report(report)

def play():
    """
    Главная функция для выбора и запуска викторины

    :return: None
    """
    directory = get_directory() 

    quiz_file = choose_quiz(directory)

    if quiz_file:
        quiz_data = load_quiz(quiz_file)

        if quiz_data:
            run(quiz_data)  

play()