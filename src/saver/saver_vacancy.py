import json
from abc import ABC, abstractmethod


class Vacancy(ABC):
    @abstractmethod
    def save_vacancies(self) -> None:
        """ Сохранение вакансий в файл """
        pass

    @abstractmethod
    def delete_vacancies(self, user_id: str) -> None:
        """ Удаление вакансий из файла по id """
        pass

    @abstractmethod
    def add_vacancy(self) -> None:
        """ Добавление вакансий в существующий файл """
        pass


class ReadData(Vacancy):
    def __init__(self, data: list) -> None:
        self.data = data

    def save_vacancies(self) -> None:
        with open('vacancy.json', 'w', encoding='utf-8') as file:
            json.dump(self.data, file, ensure_ascii=False, indent=2)

    def delete_vacancies(self, user_id: str) -> None:
        """Удаление вакансий"""
        try:
            initial_data = json.load(open("vacancy.json", encoding='utf-8'))
            new_list = [vacancy for vacancy in initial_data if vacancy.get('id') != user_id]
            with open("vacancy.json", 'w', encoding='utf-8') as file:
                json.dump(new_list, file, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Ошибка: {e}")

    def add_vacancy(self) -> None:
        """ Добавление вакансий к списку в файле json """
        try:
            initial_data = json.load(open("vacancy.json", encoding='utf-8'))
            new_list = initial_data + self.data
            with open("vacancy.json", 'w', encoding='utf-8') as file:
                json.dump(new_list, file, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Ошибка: {e}")
