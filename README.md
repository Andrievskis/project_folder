# Проект: Система для работы с вакансиями и базой данных.
_Проект представляет собой набор инструментов для взаимодействия с базой данных вакансий 
и API HeadHunter. Система позволяет получать, обрабатывать и анализировать данные о вакансиях._

## Описание:

# Цель проекта
_Создание удобного инструмента для работы с вакансиями, который позволяет:
Получать данные из базы данных.
Интегрироваться с API HeadHunter.
Анализировать информацию о вакансиях.
Формировать отчёты._

#  Основные функции
_Работа с БД: получение списка компаний, вакансий, средней зарплаты.
Фильтрация данных: поиск вакансий по ключевым словам и компаниям.
Интеграция с API: получение актуальных данных с HeadHunter.
Анализ данных: расчёт средней зарплаты, фильтрация по условиям._

## Установка
Установленные зависимости (requirements.txt)
```
pip install -r requirements.txt
```

# Настройка
_Создайте файл конфигурации с параметрами подключения к БД.
Настройте параметры API HeadHunter.
Установите необходимые права доступа._

## Использование

## Работа с базой данных
```
from src.dbmanager import DBManager

db = DBManager(database_name="your_db", params={
    "user": "your_user",
    "password": "your_password",
    "host": "localhost",
    "port": "5432"
})
```

# Получение списка компаний
```
companies = db.get_companies_and_vacancies_count()
```

# Получение всех вакансий
```
vacancies = db.get_all_vacancies()
```

# Получение средней зарплаты
```
avg_salary = db.get_avg_salary()
```

## Работа с API HeadHunter
```
from src.api import HeadHunterAPI

hh_api = HeadHunterAPI()
```

# Получение вакансий по ключевому слову
```
vacancies = hh_api.receiving_vacancies(keyword="Python", pages=2)
```

# Получение вакансий по компаниям
```
hh_api.set_company_names(["Company1", "Company2"])
company_vacancies = hh_api.receiving_vacancies(company_names=["Company1", "Company2"])
```

