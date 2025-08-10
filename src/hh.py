from typing import Any, Dict, List

import requests
from requests import HTTPError, RequestException

from src.base_api import BaseApi


class HeadHunterAPI(BaseApi):
    """Класс для работы с API с HeadHunter."""

    def __init__(self) -> None:
        super().__init__()
        self.__url: str = 'https://api.hh.ru/vacancies'
        self.__headers: Dict[str, str] = {'User-Agent': 'HH-User-Agent'}
        self.__params: Dict[str, Any] = {'text': '', 'page': 0, 'per_page': 100}
        self.__vacancies: List[Dict[str, Any]] = []

    def __repr__(self) -> str:
        """Строковое представление списка вакансий."""
        return f'{self.__vacancies}'

    @property
    def _BaseApi__connect_to_api(self) -> str:
        return ""

    def __connect_to_api(self, keyword: str, pages: int = 1) -> None:
        """Метод подключения к API hh.ru."""
        self.__params['text'] = keyword
        try:
            current_page: int = self.__params.get('page', 0)
            while current_page < pages:
                response = requests.get(self.__url, headers=self.__headers, params=self.__params)
                if response.status_code == 200:
                    vacancies = response.json().get('items', [])
                    self.__vacancies.extend(vacancies)
                    current_page += 1
                    self.__params['page'] = current_page
                else:
                    print(f'Получен статус: {response.status_code}')
                    break
        except HTTPError as e:
            print(f'HTTP ошибка: {e}')
        except RequestException as e:
            print(f'Сетевая ошибка: {e}')

    def receiving_vacancies(self, keyword: str, pages: int = 1) -> List[Dict]:
        """Метод получения вакансий с hh.ru."""
        self.__connect_to_api(keyword, pages)
        return self.__vacancies
