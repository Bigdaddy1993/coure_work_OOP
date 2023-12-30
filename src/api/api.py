import os
from abc import ABC, abstractmethod
from typing import Any

import requests
from dotenv import load_dotenv

load_dotenv()


class BaseAPI(ABC):
    @abstractmethod
    def get_vacancies(self) -> Any:
        """ Абстрактный класс для работы с API сайтов с вакансиями """
        pass


class ParamsAPI:
    """ Параметры для поиска """

    def __init__(self, name: str, filtered: Any, salary: int, no_salary: int):
        self.name = name  # название вакансии
        self.filtered = filtered  # фильтрация по дате или сумме
        self.salary = salary  # зарплата от и выше
        self.no_salary = no_salary  # исключить вакансии без оклада

    def __repr__(self):
        """ Вывод названия вакансии """
        return self.name


class HeadHunterAPI(BaseAPI, ParamsAPI):
    """Инициализация"""

    def __init__(self, name: str, filtered: Any, salary: int, no_salary: int):
        super().__init__(name, filtered, salary, no_salary)
        self.url = 'https://api.hh.ru/vacancies'

    def get_vacancies(self) -> Any:
        """ Подключение к API HeadHunter и получение данных в json формате """
        try:
            response = requests.get(self.url,
                                    params={'text': self.name, 'order_by': self.filtered,
                                            'salary': self.salary, 'only_with_salary': self.no_salary,
                                            'per_page': 100}).json()
            return response
        except Exception as e:
            raise e


class SuperJobAPI(BaseAPI, ParamsAPI):
    """Инициализация"""

    def __init__(self, name: str, filtered: Any, salary: int, no_salary: int):
        super().__init__(name, filtered, salary, no_salary)
        self.headers = {'X-Api-App-Id': os.getenv('API_KEY')}
        self.url = 'https://api.superjob.ru/2.0/vacancies'

    def get_vacancies(self) -> Any:
        """ Подключение к API SuperJob и получение данных в json формате """
        try:
            response = requests.get(self.url, headers=self.headers,
                                    params={'keywords': self.name, 'order_field': self.filtered,
                                            'payment_from': self.salary, 'no_agreement': self.no_salary,
                                            'per_page': 100}).json()
            return response
        except Exception as e:
            raise e
