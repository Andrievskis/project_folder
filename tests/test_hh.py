from unittest.mock import MagicMock, patch

import pytest
import requests

from src.hh import HeadHunterAPI


@pytest.fixture
def hh_api() -> HeadHunterAPI:
    return HeadHunterAPI()


@patch("requests.get")
def test_receiving_vacancies_success(mock_get: MagicMock, hh_api: HeadHunterAPI) -> None:
    """Тестовые данные."""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "items": [{"id": 1, "name": "Тестовая вакансия 1"}, {"id": 2, "name": "Тестовая вакансия 2"}]
    }
    mock_get.return_value = mock_response

    vacancies = hh_api.receiving_vacancies("python", pages=1)

    assert len(vacancies) == 2
    assert vacancies[0]["name"] == "Тестовая вакансия 1"
    assert vacancies[1]["name"] == "Тестовая вакансия 2"


@patch("requests.get")
def test_receiving_vacancies_multiple_pages(mock_get: MagicMock, hh_api: HeadHunterAPI) -> None:
    """Тестовые данные для двух страниц."""
    mock_response1 = MagicMock()
    mock_response1.status_code = 200
    mock_response1.json.return_value = {
        "items": [{"id": 1, "name": "Страница 1, вакансия 1"}, {"id": 2, "name": "Страница 1, вакансия 2"}]
    }

    mock_response2 = MagicMock()
    mock_response2.status_code = 200
    mock_response2.json.return_value = {
        "items": [{"id": 3, "name": "Страница 2, вакансия 1"}, {"id": 4, "name": "Страница 2, вакансия 2"}]
    }

    mock_get.side_effect = mock_response1, mock_response2

    vacancies = hh_api.receiving_vacancies("python", pages=2)

    assert len(vacancies) == 4
    assert vacancies[0]["name"] == "Страница 1, вакансия 1"
    assert vacancies[3]["name"] == "Страница 2, вакансия 2"


@patch("requests.get")
def test_receiving_vacancies_http_error(mock_get: MagicMock, hh_api: HeadHunterAPI) -> None:
    """Тестовые данные с ошибкой."""
    mock_response = MagicMock()
    mock_response.status_code = 404
    mock_get.return_value = mock_response

    vacancies = hh_api.receiving_vacancies("python")

    assert len(vacancies) == 0


@patch("requests.get")
def test_receiving_vacancies_network_error(mock_get: MagicMock, hh_api: HeadHunterAPI) -> None:
    """Тестовые данные с сетевой ошибкой."""
    mock_get.side_effect = requests.exceptions.RequestException("Сетевая ошибка")

    vacancies = hh_api.receiving_vacancies("python")

    assert len(vacancies) == 0


def test_receiving_vacancies_mock(hh_api: HeadHunterAPI) -> None:
    """Проверка через мокинг внутреннего метода."""
    with patch.object(hh_api, "_HeadHunterAPI__connect_to_api") as mock_connect:
        mock_connect.return_value = None
        result = hh_api.receiving_vacancies("python", 1)
        mock_connect.assert_called_once_with("python", 1)
        assert result == []
