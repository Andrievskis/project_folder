import unittest
from typing import Any, Dict, List
from unittest.mock import MagicMock, patch

from psycopg2 import OperationalError

from src.dbmanager import DBManager


class TestDBManager(unittest.TestCase):
    def setUp(self) -> None:
        """Инициализация объекта DBManager с тестовыми параметрами."""
        self.db_manager = DBManager(
            database_name="test_db",
            params={
                "user": "test_user",
                "password": "test_password",
                "host": "localhost",
                "port": "5432"
            }
        )

    def test_connect_success(self) -> None:
        """Тест успешного подключения к базе данных."""
        with patch('psycopg2.connect') as mock_connect:
            self.db_manager.connect()
            mock_connect.assert_called_once_with(
                dbname="test_db",
                user="test_user",
                password="test_password",
                host="localhost",
                port="5432"
            )
            self.assertIsNotNone(self.db_manager.conn)

    def test_connect_failure(self) -> None:
        """Тест обработки ошибки подключения."""
        with patch('psycopg2.connect') as mock_connect:
            mock_connect.side_effect = OperationalError("Connection failed")
            with self.assertRaises(ConnectionError):
                self.db_manager.connect()

    def test_disconnect(self) -> None:
        """Тест закрытия соединения."""
        self.db_manager.conn = MagicMock()
        self.db_manager.conn.closed = False
        self.db_manager.disconnect()
        self.db_manager.conn.close.assert_called_once()

    def test_check_connection_success(self) -> None:
        """Тест, что проверка соединения проходит при активном подключении."""
        self.db_manager.conn = MagicMock()
        self.db_manager.conn.closed = False
        self.db_manager._check_connection()

    def test_check_connection_failure(self) -> None:
        """Тест, что при отсутствии соединения выбрасывается ошибка."""
        self.db_manager.conn = None
        with self.assertRaises(ConnectionError):
            self.db_manager._check_connection()

    @patch('src.dbmanager.psycopg2.connect')
    def test_get_companies_and_vacancies_count(self, mock_connect: MagicMock) -> None:
        """Тест получения списка компаний и количества вакансий.
        Проверяет корректность выполнения SQL-запроса и формирования результата."""
        mock_cursor = MagicMock()
        mock_cursor.fetchall.return_value = [
            ('Company A', 5),
            ('Company B', 3)
        ]

        mock_conn = MagicMock()
        mock_conn.closed = False
        mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
        mock_connect.return_value = mock_conn

        self.db_manager.conn = mock_conn

        result = self.db_manager.get_companies_and_vacancies_count()

        expected = [
            {'company': 'Company A', 'vacancies_count': 5},
            {'company': 'Company B', 'vacancies_count': 3}
        ]
        self.assertEqual(result, expected)

        actual_query = mock_cursor.mock_calls[0].args[0]

        expected_query = (
            "SELECT o.name_organization AS company, COUNT(v.vacancy_id) AS vacancies_count "
            "FROM organizations o LEFT JOIN vacancies v ON o.organization_id = v.organization_id "
            "GROUP BY o.organization_id, o.name_organization ORDER BY vacancies_count DESC;"
        )

        def normalize_query(query: str) -> str:
            normalized = query.replace(' ', '').replace('\n', '').replace('\t', '')
            return normalized

        self.assertEqual(
            normalize_query(actual_query),
            normalize_query(expected_query)
        )

        mock_cursor.execute.assert_called_once()

    @patch('src.dbmanager.psycopg2.connect')
    def test_get_avg_salary(self, mock_connect: MagicMock) -> None:
        """Тест получения средней зарплаты."""
        mock_cursor = MagicMock()
        mock_cursor.fetchone.return_value = (50000,)

        mock_conn = MagicMock()
        mock_conn.closed = False
        mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
        mock_connect.return_value = mock_conn

        self.db_manager.conn = mock_conn

        result = self.db_manager.get_avg_salary()

        self.assertEqual(result, 50000.0)
        mock_cursor.execute.assert_called_once()

    @patch('psycopg2.connect')
    def test_get_vacancies_with_higher_salary(self, mock_connect: MagicMock) -> None:
        """Тест получения вакансий с зарплатой выше средней."""
        mock_cursor = MagicMock()
        mock_conn = MagicMock()
        mock_conn.closed = False
        mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
        mock_connect.return_value = mock_conn

        mock_cursor.fetchall.return_value = [
            ('Company X', 'Python Developer', 100000, 150000, 'Москва', 'http://link1'),
            ('Company Y', 'Senior Developer', 120000, 180000, 'Санкт-Петербург', 'http://link2')
        ]

        self.db_manager.conn = mock_conn
        with patch.object(self.db_manager, 'get_avg_salary', return_value=90000.0):
            result: List[Dict[str, Any]] = self.db_manager.get_vacancies_with_higher_salary()

        expected: list[dict[str, Any]] = [
            {
                "company": "Company X",
                "vacancy": "Python Developer",
                "salary_from": 100000,
                "salary_to": 150000,
                "city": "Москва",
                "url": "http://link1"
            },
            {
                "company": "Company Y",
                "vacancy": "Senior Developer",
                "salary_from": 120000,
                "salary_to": 180000,
                "city": "Санкт-Петербург",
                "url": "http://link2"
            }
        ]

        self.assertEqual(result, expected)

        mock_cursor.execute.assert_called_once()
        args = mock_cursor.execute.call_args[0]
        query: str = args[0]
        avg_salary: tuple = args[1]

        self.assertEqual(avg_salary[0], 90000.0)

        expected_query = (
            "SELECT o.name_organization AS company, v.name_vacancy AS vacancy, "
            "v.salary_from, v.salary_to, v.city, v.url_vacancy AS url "
            "FROM vacancies v JOIN organizations o ON v.organization_id = o.organization_id "
            "WHERE v.salary_from IS NOT NULL AND v.salary_from ~ '^[0-9]+$' "
            "AND CAST(v.salary_from AS NUMERIC) > %s;"
        )

        def normalize_query(query: str) -> str:
            return query.replace(' ', '').replace('\n', '').replace('\t', '')

        self.assertEqual(
            normalize_query(query),
            normalize_query(expected_query)
        )


if __name__ == '__main__':
    unittest.main()
