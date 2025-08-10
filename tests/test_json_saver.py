import json
from pathlib import Path
from typing import Generator
from unittest.mock import mock_open, patch

import pytest

from src.json_saver import JSONSaver  # Замените на реальный путь к вашему модулю
from src.vacancies_hh import Vacancy


# Подготовка тестовой среды
@pytest.fixture
def setup_saver() -> Generator[JSONSaver, None, None]:
    temp_file = Path("test_vacancies.json")
    saver = JSONSaver(file_path=str(temp_file))
    yield saver
    if temp_file.exists():
        temp_file.unlink()


@pytest.fixture
def vacancy1() -> Vacancy:
    """Тестовые данные."""
    return Vacancy(
        "Python Developer",
        "https://hh.ru/vacancy/123456",
        "100000",
        "300000",
        "Москва",
        "Знание основ программирования.",
        "Удалённо",
    )


@pytest.fixture
def vacancy2() -> Vacancy:
    """Тестовые данные."""
    return Vacancy(
        "Python",
        "https://hh.ru/vacancy/123789",
        "200000",
        "500000",
        "Екатеринбург",
        "Знание основ программирования.",
        "Гибрид",
    )


def test_save_data(setup_saver: JSONSaver) -> None:
    """Тест на сохранение данных в JSON-формат."""
    data = [{"test": "data"}]
    expected_json = json.dumps(data, indent=4)

    with patch("builtins.open", new_callable=mock_open) as mock_file:
        setup_saver.save_data(data)
        mock_file.assert_called_once()

        written_content = "".join(call.args[0] for call in mock_file().write.call_args_list)
        assert written_content == expected_json


def test_load_data_empty(setup_saver: JSONSaver) -> None:
    """Тест на загрузку данных из пустого файла."""
    result = setup_saver.load_data()
    assert result == []


def test_add_vacancy_single(setup_saver: JSONSaver, vacancy1: Vacancy) -> None:
    """Тест на добавление одной вакансии."""
    setup_saver.add_vacancy([vacancy1])
    data = setup_saver.load_data()
    assert len(data) == 1
    assert data[0]["name_vacancy"] == "Python Developer"


def test_add_vacancy_multiple(setup_saver: JSONSaver, vacancy1: Vacancy, vacancy2: Vacancy) -> None:
    """Тест на добавление нескольких вакансий."""
    setup_saver.add_vacancy([vacancy1, vacancy2])
    data = setup_saver.load_data()
    assert len(data) == 2
    assert data[0]["name_vacancy"] == "Python Developer"
    assert data[1]["name_vacancy"] == "Python"


def test_get_vacancy_by_criteria(setup_saver: JSONSaver, vacancy1: Vacancy) -> None:
    """Тест на поиск вакансии по критериям."""
    setup_saver.add_vacancy([vacancy1])
    criteria = {"name_vacancy": "Python Developer"}
    result = setup_saver.get_vacancy(criteria)
    assert len(result) == 1
    assert result[0]["name_vacancy"] == "Python Developer"


def test_delete_vacancy(setup_saver: JSONSaver, vacancy1: Vacancy) -> None:
    """Тест на удаление вакансии."""
    setup_saver.add_vacancy([vacancy1])
    criteria = {"name_vacancy": "Python Developer"}
    setup_saver.delete_vacancy(criteria)
    result = setup_saver.load_data()
    assert result == []


def test_delete_nonexistent_vacancy(setup_saver: JSONSaver) -> None:
    """Тест для проверки удаления несуществующей вакансии."""
    criteria = {"name_vacancy": "Nonexistent Job"}
    setup_saver.delete_vacancy(criteria)
    result = setup_saver.load_data()
    assert result == []


def test_add_duplicate_vacancy(setup_saver: JSONSaver, vacancy1: Vacancy) -> None:
    """Тест для проверки добавления дублирующейся вакансии."""
    setup_saver.add_vacancy([vacancy1])
    setup_saver.add_vacancy([vacancy1])
    data = setup_saver.load_data()
    assert len(data) == 1
