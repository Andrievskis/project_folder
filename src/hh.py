from typing import Any, Dict, List, Optional

import requests
from requests import HTTPError, RequestException

from src.base_api import BaseApi


class HeadHunterAPI(BaseApi):
    """Класс для работы с API с HeadHunter."""

    def __init__(self) -> None:
        super().__init__()
        self.__url: str = "https://api.hh.ru/vacancies"
        self.__headers: Dict[str, str] = {"User-Agent": "HH-User-Agent"}
        self.__params: Dict[str, Any] = {"text": "", "page": 0, "per_page": 100}
        self.__vacancies: List[Dict[str, Any]] = []
        self.__company_names: List[str] = []

    def __repr__(self) -> str:
        """Строковое представление списка вакансий."""
        return f"{self.__vacancies}"

    @property
    def _BaseApi__connect_to_api(self) -> str:
        return ""

    def set_company_names(self, company_names: List[str]) -> None:
        """Установка списка названий компаний для фильтрации."""
        self.__company_names = company_names

    def __connect_to_api(
        self, keyword: Optional[str] = None, company_names: Optional[List[str]] = None, pages: int = 1
    ) -> None:
        """Метод подключения к API hh.ru."""
        search_text = keyword
        if company_names:
            company_filter = " OR ".join([f'COMPANY_NAME:"{name}"' for name in company_names])
            if keyword:
                search_text = f"{keyword} AND ({company_filter})"
            else:
                search_text = company_filter

        self.__params["text"] = search_text

        try:
            current_page: int = self.__params.get("page", 0)
            while current_page < pages:
                response = requests.get(self.__url, headers=self.__headers, params=self.__params)
                if response.status_code == 200:
                    vacancies = response.json().get("items", [])
                    if not vacancies:
                        print(f"Страница {current_page} пуста")

                    if company_names:
                        filtered_vacancies = [
                            vacancy
                            for vacancy in vacancies
                            if "employer" in vacancy
                            and "name" in vacancy["employer"]
                            and vacancy["employer"]["name"] in company_names
                        ]
                    else:
                        filtered_vacancies = vacancies

                    self.__vacancies.extend(filtered_vacancies)
                    current_page += 1
                    self.__params["page"] = current_page
                else:
                    print(f"Получен статус: {response.status_code}")
                    break
        except HTTPError as e:
            print(f"HTTP ошибка: {e}")
        except RequestException as e:
            print(f"Сетевая ошибка: {e}")

    def receiving_vacancies(
        self, keyword: Optional[str] = None, company_names: Optional[List[str]] = None, pages: int = 1
    ) -> List[Dict]:
        """Метод получения вакансий с hh.ru."""
        self.__params["page"] = 0
        self.__vacancies = []
        if keyword is None:
            self.__params.pop("text", None)
        else:
            self.__params["text"] = keyword

        if company_names is not None:
            self.set_company_names(company_names)

        self.__connect_to_api(keyword, company_names, pages)
        return self.__vacancies
