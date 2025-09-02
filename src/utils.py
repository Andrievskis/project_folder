from typing import List

import psycopg2

from src.hh import HeadHunterAPI


def create_database(database_name: str, params: dict) -> None:
    """Создание базы данных и таблиц для хранения данных о вакансиях."""
    try:
        conn = psycopg2.connect(dbname="postgres", **params)
        conn.autocommit = True
        cur = conn.cursor()

        cur.execute(f"DROP DATABASE IF EXISTS {database_name}")
        cur.execute(f"CREATE DATABASE {database_name}")

        cur.close()
        conn.close()

        conn = psycopg2.connect(dbname=database_name, **params)

        with conn.cursor() as cur:
            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS organizations (
                    organization_id INTEGER PRIMARY KEY,
                    name_organization VARCHAR(100) NOT NULL,
                    url_organization TEXT
                )
            """
            )

        with conn.cursor() as cur:
            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS vacancies (
                    vacancy_id INTEGER PRIMARY KEY,
                    name_vacancy VARCHAR(200) NOT NULL,
                    salary_from VARCHAR(100),
                    salary_to VARCHAR(100),
                    city VARCHAR(100),
                    url_vacancy TEXT,
                    organization_id INTEGER REFERENCES organizations(organization_id)
                )
            """
            )

        conn.commit()
        conn.close()
    except psycopg2.Error as e:
        print(f"Ошибка при создании базы данных: {e}")


def data_entry(database_name: str, params: dict, companies: List[str]) -> None:
    """Заполнение базы данных данными с HeadHunter."""
    hh = HeadHunterAPI()
    vacancies = hh.receiving_vacancies(company_names=companies)
    vacancies_count = 0

    try:
        conn = psycopg2.connect(dbname=database_name, **params)

        with conn:
            with conn.cursor() as cur:
                for vacancy in vacancies:
                    employer = vacancy.get("employer", {})
                    employer_id = employer.get("id")
                    employer_name = employer.get("name")
                    employer_url = employer.get("url")

                    if employer:
                        try:
                            cur.execute(
                                """
                                INSERT INTO organizations (organization_id, name_organization, url_organization)
                                VALUES (%s, %s, %s)
                                ON CONFLICT (organization_id) DO NOTHING;
                                """,
                                (employer_id, employer_name, employer_url)
                            )
                        except psycopg2.Error as e:
                            print(f"Ошибка при вставке организации: {e}")

                for vacancy in vacancies:
                    employer = vacancy.get("employer", {})
                    employer_id = employer.get("id")
                    vacancy_id = vacancy.get("id")
                    vacancy_name = vacancy.get("name")
                    area = vacancy.get("area", {})
                    city = area.get("name") if area else None

                    salary = vacancy.get("salary")
                    if salary is not None:
                        salary_from = str(salary.get("from")) if salary.get("from") is not None else None
                        salary_to = str(salary.get("to")) if salary.get("to") is not None else None
                    else:
                        salary_from = None
                        salary_to = None

                    url = vacancy.get("alternate_url")

                    try:
                        cur.execute(
                            """INSERT INTO vacancies
                            (vacancy_id, name_vacancy, salary_from, salary_to, city, url_vacancy, organization_id)
                            VALUES (%s, %s, %s, %s, %s, %s, %s)
                            ON CONFLICT (vacancy_id) DO NOTHING;
                            """,
                            (vacancy_id, vacancy_name, salary_from, salary_to, city, url, employer_id)
                        )
                        vacancies_count += 1
                    except psycopg2.Error as e:
                        print(f"Ошибка при вставке вакансии: {e}")
        conn.commit()
        conn.close()

        print(f"Успешно добавлено {vacancies_count} вакансий")

    except psycopg2.Error as e:
        print(f"Произошла ошибка при записи данных: {e}")
