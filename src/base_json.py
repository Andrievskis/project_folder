from abc import ABC, abstractmethod
from typing import Dict, List, Union

from src.vacancies_hh import Vacancy


class BaseClass(ABC):
    """Абстрактный класс который обязывает реализовать методы
    для добавления вакансий в файл,
    получения данных из файла по указанным критериям
    и удаления информации о вакансиях."""

    @abstractmethod
    def add_vacancy(self, vacancies: Union[Vacancy, List[Vacancy]]) -> None:
        """Метод для добавления вакансий в файл."""
        pass

    @abstractmethod
    def get_vacancy(self, criteria: Union[Dict, Vacancy]) -> list:
        """Метод для получения данных из файла по заданным критериям."""
        pass

    @abstractmethod
    def delete_vacancy(self, criteria: Union[Dict, Vacancy]) -> None:
        """Метод для удаления вакансии."""
        pass
