from datetime import datetime
from typing import Any


class Validate:
    def __init__(self, response: Any) -> None:
        self.response = response

    def data_vacancy_sj(self) -> list:
        vacancies = []
        try:
            for vacancy in self.response['objects']:
                date_vacancy = datetime.fromtimestamp(vacancy.get('date_published', ''))
                super_job = {
                    'id': vacancy['id'],
                    'name': vacancy.get('profession', ''),
                    'solary_from': vacancy.get('payment_from', '') if vacancy.get('payment_from') else None,
                    'responsibility': vacancy.get('candidat').replace('\n', '').replace('•', '')
                    if vacancy.get('candidat') else None,
                    'data': date_vacancy.strftime("%d.%m.%Y"),
                    'link': vacancy.get('link') if vacancy.get('link') else None
                }
                vacancies.append(super_job)
            return vacancies

        except Exception as e:
            print(f"Ошибка: {e}")
            return []

    def data_vacancy_hh(self) -> Any:
        """ Создание списка вакансий данными """
        vacancies = []
        try:
            for vacancy in self.response.get('items'):
                date_vacancy = datetime.strptime(vacancy['published_at'], "%Y-%m-%dT%H:%M:%S%z")
                vacancies_ = {
                    'id': vacancy['id'],
                    'name': vacancy['name'],
                    'solary_from': vacancy['salary']['from'] if vacancy.get('salary') else None,
                    'responsibility': vacancy['snippet']['responsibility'],
                    'data': date_vacancy.strftime("%d.%m.%Y"),
                    'link': vacancy['alternate_url'] if vacancy.get('alternate_url') else None
                }
                vacancies.append(vacancies_)
            return vacancies
        except Exception as e:
            print(f"Ошибка: {e}")

    @staticmethod
    def top_vacancies(vacancies: list) -> list:
        top_5_vacancies = sorted(vacancies, key=lambda x: x.get('salary', {}).get('from', 0), reverse=True)[:5]
        return top_5_vacancies
