from typing import Dict, List, Union

import pandas as pd
from pandas.errors import EmptyDataError

from src.base_json import BaseClass
from src.vacancies_hh import Vacancy


class ExcelFile(BaseClass):
    """Класс, который обязывает реализовать методы для добавления вакансий в файл,
    получения данных из файла по указанным критериям и удаления информации о вакансиях."""

    def __init__(self, filename: str = "vacancies.xlsx") -> None:
        self.__filename: str = filename

    def add_vacancy(self, vacancies: Union[Vacancy, List[Vacancy]]) -> None:
        """Метод для добавления вакансий в файл."""
        try:
            if isinstance(vacancies, Vacancy):
                vacancies = [vacancies]

            try:
                df = pd.read_excel(self.__filename, sheet_name=0)
            except FileNotFoundError:
                df = pd.DataFrame()
            except EmptyDataError:
                df = pd.DataFrame()

            new_data = []
            for vacancy in vacancies:
                vacancy_dict = vacancy.to_dict()
                if not df.equals(pd.DataFrame([vacancy_dict])):
                    new_data.append(vacancy_dict)
            if new_data:
                new_df = pd.DataFrame(new_data)
                df = pd.concat([df, new_df], ignore_index=True)
                df.to_excel(self.__filename, index=False)
        except Exception as e:
            print(f"Произошла ошибка: {str(e)}")
            raise

    def get_vacancy(self, criteria: Union[Dict, Vacancy]) -> list:
        """Метод для получения данных из файла по заданным критериям."""
        try:
            df = pd.read_excel(self.__filename, sheet_name=0)
            return df.to_dict('records')
        except FileNotFoundError:
            return []

    def delete_vacancy(self, criteria: Union[Dict, Vacancy]) -> None:
        """Метод для удаления вакансии."""
        if isinstance(criteria, Vacancy):
            criteria = criteria.to_dict()
        try:
            df = pd.read_excel(self.__filename, sheet_name=0)
            filtered_df = df
            for key, value in criteria.items():
                filtered_df = filtered_df[filtered_df[key] != value]

            filtered_df.to_excel(self.__filename, index=False)
        except FileNotFoundError:
            print(f"Файл {self.__filename} не найден.")


if __name__ == "__main__":
    vacancy = Vacancy(
        "Python Developer",
        "https://hh.ru/vacancy/123456",
        "50000",
        "100000",
        "Москва",
        "Знание основ программирования.",
        "Гибрид",
    )

    # Сохранение информации о вакансиях в файл
    # excel_saver = ExcelFile()
    # excel_saver.add_vacancy(vacancy)
    # print(excel_saver.get_vacancy(vacancy))
    # excel_saver.delete_vacancy(vacancy)
