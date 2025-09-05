import psycopg2
from typing import List, Dict, Any


class DBManager:
    """Класс для подключения к БД PostgreSQL и получения данных о вакансиях."""

    def __init__(self, database_name: str, params: Dict[str, Any]) -> None:
        """Инициализация подключения к базе данных."""
        self.database_name = database_name
        self.params = params
        self.conn: psycopg2.extensions.connection | None = None

    def connect(self) -> None:
        """Устанавливает соединение с базой данных."""
        try:
            self.conn = psycopg2.connect(dbname=self.database_name, **self.params)
        except psycopg2.Error as e:
            raise ConnectionError(f"Ошибка подключения к базе данных: {e}")

    def disconnect(self) -> None:
        """Закрывает соединение с базой данных."""
        if self.conn and not self.conn.closed:
            self.conn.close()

    def _check_connection(self) -> None:
        """Проверяет, установлено ли соединение."""
        if not self.conn or self.conn.closed:
            raise ConnectionError("Соединение с базой данных не установлено!")

    def get_companies_and_vacancies_count(self) -> List[Dict[str, Any]]:
        """Метод, получает список всех компаний и количество вакансий у каждой компании."""
        self._check_connection()
        assert self.conn is not None
        query = """
        SELECT o.name_organization AS company, COUNT(v.vacancy_id) AS vacancies_count
        FROM organizations o
        LEFT JOIN vacancies v ON o.organization_id = v.organization_id
        GROUP BY o.organization_id, o.name_organization
        ORDER BY vacancies_count DESC;
        """
        with self.conn.cursor() as cur:
            cur.execute(query)
            rows = cur.fetchall()
            return [{"company": row[0], "vacancies_count": row[1]} for row in rows]

    def get_all_vacancies(self) -> List[Dict[str, Any]]:
        """Метод, получает список всех вакансий с указанием названия компании,
        названия вакансии, зарплаты и ссылки на вакансию."""
        self._check_connection()
        assert self.conn is not None
        query = """
        SELECT
            o.name_organization AS company,
            v.name_vacancy AS vacancy,
            v.salary_from,
            v.salary_to,
            v.city,
            v.url_vacancy AS url
        FROM vacancies v
        JOIN organizations o ON v.organization_id = o.organization_id;
        """
        with self.conn.cursor() as cur:
            cur.execute(query)
            rows = cur.fetchall()
            return [
                {
                    "company": row[0],
                    "vacancy": row[1],
                    "salary_from": row[2],
                    "salary_to": row[3],
                    "city": row[4],
                    "url": row[5],
                }
                for row in rows
            ]

    def get_avg_salary(self) -> float:
        """Метод, получает среднюю зарплату по вакансиям (по полю salary_from)."""
        self._check_connection()
        assert self.conn is not None
        query = """
        SELECT AVG(CAST(salary_from AS NUMERIC))
        FROM vacancies
        WHERE salary_from IS NOT NULL AND salary_from ~ '^[0-9]+$';
        """
        with self.conn.cursor() as cur:
            cur.execute(query)
            result = cur.fetchone()
            if result and result[0] is not None:
                return float(result[0])
            return 0.0

    def get_vacancies_with_higher_salary(self) -> List[Dict[str, Any]]:
        """Метод, получает список всех вакансий, у которых зарплата выше средней по всем вакансиям."""
        self._check_connection()
        assert self.conn is not None
        try:
            avg_salary = self.get_avg_salary()
            query = """
            SELECT
                o.name_organization AS company,
                v.name_vacancy AS vacancy,
                v.salary_from,
                v.salary_to,
                v.city,
                v.url_vacancy AS url
            FROM vacancies v
            JOIN organizations o ON v.organization_id = o.organization_id
            WHERE v.salary_from IS NOT NULL
              AND v.salary_from ~ '^[0-9]+$'
              AND CAST(v.salary_from AS NUMERIC) > %s;
            """
            with self.conn.cursor() as cur:
                cur.execute(query, (avg_salary,))
                rows = cur.fetchall()
                return [
                    {
                        "company": row[0],
                        "vacancy": row[1],
                        "salary_from": row[2],
                        "salary_to": row[3],
                        "city": row[4],
                        "url": row[5],
                    }
                    for row in rows
                ]
        except Exception as e:
            print(f"Произошла ошибка при получении вакансий с высокой зарплатой: {e}")
            return []

    def get_vacancies_with_keyword(self, keyword: str) -> List[Dict[str, Any]]:
        """Метод, получает список всех вакансий, в названии которых
        содержатся переданные в метод слова, например python."""
        self._check_connection()
        assert self.conn is not None
        query = """
                SELECT
                    o.name_organization AS company,
                    v.name_vacancy AS vacancy,
                    v.salary_from,
                    v.salary_to,
                    v.city,
                    v.url_vacancy AS url
                FROM vacancies v
                JOIN organizations o ON v.organization_id = o.organization_id
                WHERE v.name_vacancy ILIKE %s;
                """
        with self.conn.cursor() as cur:
            cur.execute(query, (f"%{keyword}%",))
            rows = cur.fetchall()
            return [
                {
                    "company": row[0],
                    "vacancy": row[1],
                    "salary_from": row[2],
                    "salary_to": row[3],
                    "city": row[4],
                    "url": row[5],
                }
                for row in rows
            ]
