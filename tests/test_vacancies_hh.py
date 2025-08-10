from unittest import mock

from src.vacancies_hh import Vacancy


def test_init() -> None:
    """Тест на инициализацию объекта."""
    Vacancy.list_vacancies = []

    vacancy = Vacancy(
        name_vacancy="Python Developer",
        url="https://example.com",
        salary_from=100000,
        salary_to=150000,
        city="Москва",
        requirement="Опыт от 3 лет",
        work_format="Удаленная",
    )

    assert vacancy.name_vacancy == "Python Developer"
    assert vacancy.url == "https://example.com"
    assert vacancy.salary_from == 100000
    assert vacancy.salary_to == 150000
    assert vacancy.city == "Москва"
    assert vacancy.requirement == "Опыт от 3 лет"
    assert vacancy.work_format == "Удаленная"
    assert len(Vacancy.list_vacancies) == 1


def test_repr() -> None:
    """Тест на строковое представление."""
    vacancy = Vacancy(
        name_vacancy="Python Developer",
        url="https://example.com",
        salary_from=100000,
        salary_to=150000,
        city="Москва",
        requirement="Опыт от 3 лет",
        work_format="Удаленная",
    )

    expected_output = (
        "\nНазвание вакансии: Python Developer\n"
        "Ссылка на вакансию: https://example.com\n"
        "Зарплата: 100000 - 150000\n"
        "Город: Москва\n"
        "Требования: Опыт от 3 лет\n"
        "Формат работы: Удаленная\n"
    )

    assert repr(vacancy) == expected_output


def test_comparison() -> None:
    """Тест на сравнение вакансий."""
    vacancy1 = Vacancy(
        "Python Developer", "https://example.com", 100000, 150000, "Москва", "Опыт от 3 лет", "Удаленная"
    )

    vacancy2 = Vacancy(
        "Junior Developer", "https://example.com", 80000, 120000, "Москва", "Опыт от 1 года", "Удаленная"
    )

    assert vacancy2 < vacancy1
    assert not (vacancy2 > vacancy1)


def test_validate() -> None:
    """Тест на валидации."""
    try:
        Vacancy("", "https://example.com", 100000, 150000, "Москва", "Опыт от 3 лет", "Удаленная")
    except ValueError:
        pass
    else:
        assert False, "Должен быть вызван ValueError при пустом названии"

    try:
        Vacancy("Python Developer", "", 100000, 150000, "Москва", "Опыт от 3 лет", "Удаленная")
    except ValueError:
        pass
    else:
        assert False, "Должен быть вызван ValueError при пустом URL"


def test_to_dict() -> None:
    """Тест на создание вакансии в виде словаря."""
    vacancy_data = {
        "name_vacancy": "Python Developer",
        "url": "https://example.com",
        "salary_from": 100000,
        "salary_to": 150000,
        "city": "Москва",
        "requirement": "Опыт от 3 лет",
        "work_format": "Удаленная",
    }

    vacancy = Vacancy.from_dict(vacancy_data)
    result_dict = vacancy.to_dict()

    assert result_dict["name_vacancy"] == "Python Developer"
    assert result_dict["url"] == "https://example.com"
    assert result_dict["salary_from"] == 100000
    assert result_dict["salary_to"] == 150000
    assert result_dict["city"] == "Москва"
    assert result_dict["requirement"] == "Опыт от 3 лет"
    assert result_dict["work_format"] == "Удаленная"


test_vacancies_list = [
    {
        "professional_roles": [{"name": "Программист, разработчик"}],
        "area": {"url": "https://api.hh.ru/areas/160", "name": "Алматы"},
        "snippet": {
            "requirement": "Знание Git. Знание JS/HTML/CSS. Знание Vue.js, React, vite. "
                           "Умение писать SQL. Умение подключать API, асинхронная подгрузка, кеширование. "
        },
        "work_format": [{"name": "На месте работодателя"}],
        "salary": {"from": None, "to": None},
    },
    {
        "professional_roles": [{"name": "Программист, разработчик"}],
        "area": {"url": "https://api.hh.ru/areas/2759", "name": "Ташкент"},
        "snippet": {
            "requirement": "Минимум 2 года опыта в frontend web-разработке. "
                           "Участие минимум в 5 реальных веб-проектах. Опыт работы с REST API. "
        },
        "work_format": [{"name": "На месте работодателя"}],
        "salary": {"from": 400, "to": 600},
    },
]


def test_receiving_vacancies_list() -> None:
    """Тест на получение списка вакансий."""
    with mock.patch.object(Vacancy, "receiving_vacancies_list", return_value=[]):
        empty_vacancies = Vacancy.receiving_vacancies_list([])
        assert len(empty_vacancies) == 0

    vacancies = Vacancy.receiving_vacancies_list(test_vacancies_list)
    assert len(vacancies) == 2

    first_vacancy = vacancies[0]
    assert first_vacancy.name_vacancy == "Программист, разработчик"
    assert first_vacancy.url == "https://api.hh.ru/areas/160"
    assert first_vacancy.city == "Алматы"
    assert first_vacancy.work_format == "На месте работодателя"
    assert first_vacancy.salary_from == "Стартовая зарплата не указана"
    assert first_vacancy.salary_to == "Итоговая зарплата не указана"
    assert (
        first_vacancy.requirement
        == "Знание Git. Знание JS/HTML/CSS. Знание Vue.js, React, vite. Умение писать SQL. "
           "Умение подключать API, асинхронная подгрузка, кеширование. "
    )

    second_vacancy = vacancies[1]
    assert second_vacancy.name_vacancy == "Программист, разработчик"
    assert second_vacancy.url == "https://api.hh.ru/areas/2759"
    assert second_vacancy.city == "Ташкент"
    assert second_vacancy.work_format == "На месте работодателя"
    assert second_vacancy.salary_from == 400
    assert second_vacancy.salary_to == 600
    assert second_vacancy.requirement == (
        "Минимум 2 года опыта в frontend web-разработке. "
        "Участие минимум в 5 реальных веб-проектах. Опыт работы с REST API. "
    )
