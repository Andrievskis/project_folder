from abc import ABC, abstractmethod
from typing import Dict, List, Optional


class BaseApi(ABC):
    """Абстрактный класс для работы с API сервиса с вакансиями."""

    @abstractmethod
    def __repr__(self) -> str:
        """Строковое представление информации."""
        pass

    @abstractmethod
    def __connect_to_api(self, keyword: str, pages: int = 1) -> None:
        """Метод подключения к API."""
        pass

    @abstractmethod
    def receiving_vacancies(
        self, keyword: Optional[str] = None, company_names: Optional[List[str]] = None, pages: int = 1
    ) -> List[Dict]:
        """Метод получения вакансий."""
        pass
