import json
from pprint import pprint

from src.api.api import HeadHunterAPI, SuperJobAPI
from src.engine.engine_vacancy import Validate
from src.saver.saver_vacancy import ReadData


def receiving_data_from_the_user() -> None:
    """ Функция для взаимодействия с пользователем """
    while True:
        platforms = input("""Выберете цифру для поиска:
        1 - HeadHunter
        2 - SuperJob
        """)
        name = input("""Укажите профессию
        """)
        salary = int(input("""Укажите минимальную желаемую сумму зарплаты
        """))
        no_salary = int(input("""Нужно ли выводить вакансии без указания заработной платы (По договоренности)?
        1 - Нет
        2 - Да
        """))
        filtered = input("""Укажите сортировку: Дата/Зарплата
        """).lower()

        if platforms == '1':
            if filtered == "дата":
                filtered = 'publication_time'
            else:
                filtered = 'salary_desc'
            activation_class = HeadHunterAPI(name, filtered, salary, no_salary)
            sending_request = activation_class.get_vacancies()
            creation_of_vacancies = Validate(sending_request)
            vacancy_data = creation_of_vacancies.data_vacancy_hh()
        else:
            if filtered == "дата":
                filtered = 'date'
            else:
                filtered = 'payment'
            activation_class = SuperJobAPI(name, filtered, salary, no_salary)  # type: ignore
            sending_request = activation_class.get_vacancies()
            creation_of_vacancies = Validate(sending_request)
            vacancy_data = creation_of_vacancies.data_vacancy_sj()

        activating_class_for_record = ReadData(vacancy_data)

        data_status = input("""Выберите действие:
        1. Создать новый файл
        2. Дополнить прежний (при условии уже выполненого ранее 1 пункта)
        """)
        if data_status == '1':
            activating_class_for_record.save_vacancies()
            print("Файл создан успешно")
        else:
            activating_class_for_record.add_vacancy()
            print("Файл дополнен успешно")
        while True:
            choice_to_delete = input('''Хотите удалить какую-либо вакансию из файла? Да/Нет
            ''').lower()
            if choice_to_delete == "да":
                vacancy_for_removal = input("""Введите id вакансии для удаления
                """)
                activating_class_for_record.delete_vacancies(vacancy_for_removal)
                print("Успешно удалено")
            else:
                break
        continuation_of_the_cycle = input("""Хотите повторно сформировать список подходящих вакансий? Да/Нет
        """).lower()
        if continuation_of_the_cycle == "нет":
            break
    selecting_console_output = input("""Вывести топ-5 вакансии по заработной плате в консоль? Да/Нет
    """).lower()
    if selecting_console_output == "да":
        with open('vacancy.json', 'r', encoding='utf-8') as file:
            data = json.load(file)
            pprint(Validate(data).top_vacancies(data))


receiving_data_from_the_user()
