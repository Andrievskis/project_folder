import json
from pathlib import Path
from typing import Dict, List, Union

from src.base_json import BaseClass
from src.vacancies_hh import Vacancy


class JSONSaver(BaseClass):
    """Класс, который реализовывает методы для добавления вакансий в файл,
    получения данных из файла по указанным критериям и удаления информации о вакансиях. """
    def __init__(self, file_path: str = "data/vacancies.json") -> None:
        self.__file_path = Path(file_path)
        if not self.__file_path.exists():
            self.save_data([])

    def save_data(self, data: List[Dict]) -> None:
        """Метод для сохранения данных в JSON-файл."""
        try:
            with open(self.__file_path, "w", encoding="utf-8") as file:
                json.dump(data, file, ensure_ascii=False, indent=4)
        except Exception as e:
            print(f"Ошибка при сохранении данных в файл: {e}")

    def load_data(self) -> List[Dict]:
        """Метод для загрузки данных из JSON-файла."""
        try:
            with open(self.__file_path, "r", encoding="utf-8") as file:
                content = file.read().strip()
                data = json.loads(content) if content else []
                return data
        except FileNotFoundError:
            return []
        except Exception as e:
            print(f"Ошибка при чтении файла: {e}")
            return []

    def add_vacancy(self, vacancies: Union[Vacancy, List[Vacancy]]) -> None:
        """Метод для добавления вакансий в JSON-файл."""
        if isinstance(vacancies, Vacancy):
            vacancies = [vacancies]

        data = self.load_data()
        for vacancy in vacancies:
            vacancy_dict = vacancy.to_dict()
            if vacancy_dict not in data:
                data.append(vacancy_dict)
        self.save_data(data)

    def get_vacancy(self, criteria: Union[Dict, Vacancy]) -> list:
        """Метод для получения данных из файла по заданным критериям."""
        if isinstance(criteria, Vacancy):
            criteria = criteria.to_dict()

        data = self.load_data()
        result = []
        for item in data:
            if all(item.get(key) == value for key, value in criteria.items()):
                result.append(item)
        return result

    def delete_vacancy(self, criteria: Union[Dict, Vacancy]) -> None:
        """Метод для удаления вакансии."""
        if isinstance(criteria, Vacancy):
            criteria = criteria.to_dict()

        data = self.load_data()
        data = [item for item in data if not all(item.get(key) == value for key, value in criteria.items())]
        self.save_data(data)
