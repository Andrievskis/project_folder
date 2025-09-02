from typing import Dict, TypedDict

import psycopg2

from config import config
from src.dbmanager import DBManager
from src.utils import create_database, data_entry


class DBParams(TypedDict, total=False):
    host: str
    database: str
    user: str
    password: str
    port: str


def main() -> None:
    """Функция взаимодействия с пользователем."""
    database_name = "hh_vacancies"
    params: Dict[str, str] = config("database.ini")

    try:
        conn = psycopg2.connect(**params)  # type: ignore[call-overload]
        conn.close()
        print("Подключение к PostgreSQL работает!")
    except Exception as e:
        print(f"Ошибка подключения: {e}")
        return

    favorite_organizations = [
        "СОГАЗ",
        "RentAuto",
        "МегаФон",
        "WebMasters Russia",
        "Hyper AdTech",
        "Data World",
        "ВкусВилл",
        "Т-Банк",
        "Headliner",
        "Ригла",
    ]

    print("Создаём базу данных и таблицы.")
    create_database(database_name, params)
    print("База данных создана.")

    print("Получаем вакансии с HeadHunter.")
    data_entry(database_name, params, favorite_organizations)
    print("Данные загружены.")

    db = DBManager(database_name, params)
    try:
        db.connect()
        print("\nДобро пожаловать! Здесь Вы можете получить данные " "о компаниях и вакансиях с сайта hh.ru\n")

        while True:
            print("\nВыберите действие:")
            print("1. Показать все компании и количество вакансий у каждой компании.")
            print(
                "2. Показать все вакансии с указанием названия компании, "
                "названия вакансии, зарплаты и ссылки на вакансию."
            )
            print("3. Показать среднюю зарплату по вакансиям.")
            print("4. Показать вакансии с зарплатой выше средней по всем вакансиям.")
            print("5. Поиск вакансий по ключевому слову.")
            print("0. Выход.")

            choice = input("\nВведите номер: ").strip()

            if choice == "1":
                print("\nВсе компании и количество вакансий у каждой компании:")
                companies = db.get_companies_and_vacancies_count()
                for item in companies:
                    print(f"  {item['company']} — {item['vacancies_count']} вакансий")

            elif choice == "2":
                print(
                    "\nВсе вакансии с указанием названия компании, "
                    "названия вакансии, зарплаты и ссылки на вакансию:"
                )
                vacancies = db.get_all_vacancies()
                for item in vacancies:
                    salary_from = item["salary_from"] if item["salary_from"] else "не указана"
                    salary_to = item["salary_to"] if item["salary_to"] else "не указана"
                    print(f"  {item['company']} | {item['vacancy']} | {salary_from} – {salary_to} | {item['url']}")

            elif choice == "3":
                avg = db.get_avg_salary()
                print(f"\nСредняя зарплата по вакансиям: {avg:,.0f} руб.")

            elif choice == "4":
                print("\nВакансии с зарплатой выше средней по всем вакансиям:")
                high_salary_vacancies = db.get_vacancies_with_higher_salary()
                if not high_salary_vacancies:
                    print("  Нет вакансий с указанной зарплатой.")
                for item in high_salary_vacancies:
                    salary_from = item["salary_from"] if item["salary_from"] else "не указана"
                    print(f"  {item['company']} — {item['vacancy']} — от {salary_from}")

            elif choice == "5":
                keyword = input("Введите ключевое слово (например python, разработчик): ").strip()
                if not keyword:
                    print("Ключевое слово не может быть пустым.")
                    continue
                print(f"\nВакансии с ключевым словом '{keyword}':")
                keyword_vacancies = db.get_vacancies_with_keyword(keyword)
                if not keyword_vacancies:
                    print("Ничего не найдено.")
                for item in keyword_vacancies:
                    salary_from = item["salary_from"] if item["salary_from"] else "не указана"
                    print(f"  {item['company']} — {item['vacancy']} — {salary_from} — {item['url']}")

            elif choice == "0":
                print("До встречи!")
                break

            else:
                print("Неверный выбор. Попробуйте снова.")

    except Exception as e:
        print(f"Произошла ошибка: {e}")
    finally:
        db.disconnect()


if __name__ == "__main__":
    main()


# from typing import Any
# from config import ROOT_DIR
# from src.hh import HeadHunterAPI
# from src.json_saver import JSONSaver
# from src.vacancies_hh import Vacancy


# def user_interaction() -> Any:
#     platform = HeadHunterAPI()
#     storage = JSONSaver(f"{ROOT_DIR}/data/vacancies.json")
#     while True:
#         print("\n1. Ввести поисковый запрос")
#         print("2. Получить топ N вакансий по зарплате")
#         print("3. Найти вакансии по ключевому слову в описании")
#         print("4. Выход")
#
#         choice = input("Выберите действие: ")
#
#         if choice == "1":
#             query = input("Введите поисковый запрос: ")
#             vacancies = platform.receiving_vacancies(query)
#             vacancies_list = Vacancy.receiving_vacancies_list(vacancies)
#             storage.add_vacancy(vacancies_list)
#             print(f"Добавлено {len(vacancies_list)} вакансий.")
#
#         elif choice == "2":
#             try:
#                 n = int(input("Сколько вакансий вывести?: "))
#                 if n <= 0:
#                     raise ValueError
#             except ValueError:
#                 print("Пожалуйста, введите корректное положительное число")
#                 continue
#             info = storage.load_data()
#             vacancies_list = [Vacancy(**vacancy) for vacancy in info]  # Преобразуем словари в объекты Vacancy
#             sorted_vacancies = sorted(
#                 vacancies_list,
#                 key=lambda x: (isinstance(x.salary_from, int) + isinstance(x.salary_to, int)) / 2,
#                 reverse=True,
#             )
#             for vacancy in sorted_vacancies[:n]:
#                 print(vacancy.__repr__())
#
#         elif choice == "3":
#             keyword = input("Введите ключевое слово: ").lower()
#             all_vacancies = storage.load_data()
#
#             filtered_vacancies = [
#                 Vacancy(**vacancy)
#                 for vacancy in all_vacancies
#                 if vacancy.get("requirement") is not None and keyword in vacancy.get("requirement", "").lower()
#             ]
#
#             for vacancy in filtered_vacancies:
#                 print(vacancy)
#
#         elif choice == "4":
#             break
#
#         else:
#             print("Неверный выбор, попробуйте снова.")


# if __name__ == "__main__":
#     user_interaction()
