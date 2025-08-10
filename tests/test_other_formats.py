from unittest.mock import patch

import pandas as pd

from src.other_formats import ExcelFile
from src.vacancies_hh import Vacancy

# Создаем тестовый объект ExcelFile
excel_file = ExcelFile("test_vacancies.xlsx")

# Создаем тестовую вакансию
test_vacancy = Vacancy(
    "Python Developer",
    "https://hh.ru/vacancy/123456",
    "50000",
    "100000",
    "Москва",
    "Знание основ программирования.",
    "Гибрид",
)


def test_add_vacancy_single() -> None:
    """Тест на добавление одной вакансии."""
    with patch("pandas.read_excel") as mock_read_excel:
        mock_read_excel.return_value = pd.DataFrame()
        with patch("pandas.DataFrame.to_excel") as mock_to_excel:
            excel_file.add_vacancy(test_vacancy)
            mock_read_excel.assert_called_once()
            mock_to_excel.assert_called_once()


def test_add_vacancy_multiple() -> None:
    """Тест на добавление нескольких вакансий."""
    vacancies = [test_vacancy, test_vacancy]
    with patch("pandas.read_excel") as mock_read_excel:
        mock_read_excel.return_value = pd.DataFrame()  # Имитируем пустой DataFrame
        with patch("pandas.DataFrame.to_excel") as mock_to_excel:
            excel_file.add_vacancy(vacancies)
            mock_read_excel.assert_called_once()
            mock_to_excel.assert_called_once()


def test_add_vacancy_file_not_found() -> None:
    """Тест на обработку ошибки FileNotFoundError."""
    with patch("pandas.read_excel", side_effect=FileNotFoundError):
        excel_file.add_vacancy(test_vacancy)


def test_get_vacancy_empty_file() -> None:
    """Тест на получение данных из пустого файла."""
    with patch("pandas.read_excel", side_effect=FileNotFoundError):
        result = excel_file.get_vacancy({})
        assert result == []


def test_get_vacancy_existing_file() -> None:
    """Тест на получение данных из существующего файла."""
    mock_data = pd.DataFrame([test_vacancy.to_dict()])
    with patch("pandas.read_excel", return_value=mock_data):
        result = excel_file.get_vacancy({})
        assert len(result) == 1


def test_delete_vacancy() -> None:
    """Тест на удаление вакансии."""
    mock_data = pd.DataFrame([test_vacancy.to_dict()])
    with patch("pandas.read_excel", return_value=mock_data):
        with patch("pandas.DataFrame.to_excel") as mock_to_excel:
            excel_file.delete_vacancy(test_vacancy)
            mock_to_excel.assert_called_once()


def test_delete_vacancy_file_not_found() -> None:
    """Тест на обработку ошибки FileNotFoundError при удалении."""
    with patch("pandas.read_excel", side_effect=FileNotFoundError):
        excel_file.delete_vacancy(test_vacancy)
