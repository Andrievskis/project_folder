from typing import Any, Dict, List


class Vacancy:
    """Класс для работы с вакансиями."""
    __slots__ = ('name_vacancy', 'url', 'salary_from', 'salary_to', 'city',
                 'requirement', 'work_format')
    list_vacancies: list['Vacancy'] = []

    def __init__(self, name_vacancy: str, url: str, salary_from: Any, salary_to: Any,
                 city: str, requirement: str, work_format: str):
        self.name_vacancy = name_vacancy
        self.url = url
        self.salary_from = salary_from
        self.salary_to = salary_to
        self.city = city
        self.requirement = requirement
        self.work_format = work_format
        self.list_vacancies.append(self)
        self.__validate()

    def __repr__(self) -> str:
        """Строковое представление итоговой информации вакансий."""
        return (f'\nНазвание вакансии: {self.name_vacancy}\n'
                f'Ссылка на вакансию: {self.url}\n'
                f'Зарплата: {self.salary_from} - {self.salary_to}\n'
                f'Город: {self.city}\n'
                f'Требования: {self.requirement}\n'
                f'Формат работы: {self.work_format}\n')

    def __lt__(self, other: "Vacancy") -> Any:
        """Метод сравнения вакансий по минимальной зарплате"""
        return (self.salary_from + self.salary_to) / 2 < (other.salary_from + other.salary_to) / 2

    def __gt__(self, other: "Vacancy") -> Any:
        """Метод сравнения вакансий по максимальной зарплате"""
        return (self.salary_from + self.salary_to) / 2 > (other.salary_from + other.salary_to) / 2

    def __validate(self) -> None:
        """Приватный метод для валидации данных вакансии"""
        if not self.name_vacancy or not self.url:
            raise ValueError("Название вакансии и URL обязательны.")

    @classmethod
    def receiving_vacancies_list(cls, list_vacancies: List[Dict[str, Any]]) -> list['Vacancy']:
        """Метод получения данных по каждой вакансии."""
        cls.list_vacancies = []
        for vacancy in list_vacancies:
            name_vacancy = vacancy['professional_roles'][0]['name'] if vacancy['professional_roles'] else 'Не указано'
            url = vacancy['area']['url']
            requirement = vacancy['snippet']['requirement']
            work_format = vacancy['work_format'][0]['name'] if vacancy['work_format'] else 'Не указано'
            city = vacancy['area']['name']
            salary_from = vacancy['salary']['from'] if vacancy['salary'] else 'Зарплата не указана'
            if not salary_from:
                salary_from = 'Стартовая зарплата не указана'
            salary_to = vacancy['salary']['to'] if vacancy['salary'] else 'Зарплата не указана'
            if not salary_to:
                salary_to = 'Итоговая зарплата не указана'
            cls(name_vacancy, url, salary_from, salary_to, city, requirement, work_format)
        return cls.list_vacancies

    @classmethod
    def from_dict(cls, data: dict) -> "Vacancy":
        return cls(
            name_vacancy=data["name_vacancy"],
            url=data["url"],
            salary_from=data["salary_from"],
            salary_to=data["salary_to"],
            city=data["city"],
            requirement=data["requirement"],
            work_format=data["work_format"]
        )

    def to_dict(self) -> Dict[str, Any]:
        """Преобразует экземпляр класса Vacancy в словарь."""
        return {'name_vacancy': self.name_vacancy,
                'url': self.url,
                'salary_from': self.salary_from,
                'salary_to': self.salary_to,
                'city': self.city,
                'requirement': self.requirement,
                'work_format': self.work_format}
