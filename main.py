from typing import Any

from config import ROOT_DIR
from src.hh import HeadHunterAPI
from src.json_saver import JSONSaver
from src.vacancies_hh import Vacancy


def user_interaction() -> Any:
    platform = HeadHunterAPI()
    storage = JSONSaver(f"{ROOT_DIR}/data/vacancies.json")
    while True:
        print("\n1. Ввести поисковый запрос")
        print("2. Получить топ N вакансий по зарплате")
        print("3. Найти вакансии по ключевому слову в описании")
        print("4. Выход")

        choice = input("Выберите действие: ")

        if choice == "1":
            query = input("Введите поисковый запрос: ")
            vacancies = platform.receiving_vacancies(query)
            vacancies_list = Vacancy.receiving_vacancies_list(vacancies)
            storage.add_vacancy(vacancies_list)
            print(f"Добавлено {len(vacancies_list)} вакансий.")

        elif choice == "2":
            try:
                n = int(input("Сколько вакансий вывести?: "))
                if n <= 0:
                    raise ValueError
            except ValueError:
                print("Пожалуйста, введите корректное положительное число")
                continue
            info = storage.load_data()
            vacancies_list = [Vacancy(**vacancy) for vacancy in info]  # Преобразуем словари в объекты Vacancy
            sorted_vacancies = sorted(
                vacancies_list,
                key=lambda x: (isinstance(x.salary_from, int) + isinstance(x.salary_to, int)) / 2,
                reverse=True,
            )
            for vacancy in sorted_vacancies[:n]:
                print(vacancy.__repr__())

        elif choice == "3":
            keyword = input("Введите ключевое слово: ").lower()
            all_vacancies = storage.load_data()

            filtered_vacancies = [
                Vacancy(**vacancy)
                for vacancy in all_vacancies
                if vacancy.get("requirement") is not None and keyword in vacancy.get("requirement", "").lower()
            ]

            for vacancy in filtered_vacancies:
                print(vacancy)

        elif choice == "4":
            break

        else:
            print("Неверный выбор, попробуйте снова.")


if __name__ == "__main__":
    user_interaction()
