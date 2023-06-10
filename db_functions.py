import psycopg2
from typing import Any
from confyg import config


def create_database(db_name, params: dict):
    """Создание базы данных и таблиц для сохранения данных о работодателях и вакансиях."""

    # db_name = input("Укажите имя для сохранения базы данных: ").capitalize()
    params = config()
    conn = psycopg2.connect(dbname='postgres', **params)
    conn.autocommit = True
    cur = conn.cursor()

    cur.execute(f"DROP DATABASE IF EXISTS {db_name}")
    cur.execute(f"CREATE DATABASE {db_name}")

    conn.close()

    conn = psycopg2.connect(dbname=db_name, **params)
    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE employers (
            company_id INT PRIMARY KEY,
            company_name VARCHAR(100) NOT NULL,
            company_url TEXT,
            vacancies_url TEXT,
            amount_of_vacancies INT
            );
        """)

    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE vacancies (
                        vacancy_id INT PRIMARY KEY,
                        vacancy_name VARCHAR(100) NOT NULL,
                        vacancy_url TEXT,
                        salary_from INT DEFAULT 0,
                        currency VARCHAR(5),
                        requirements TEXT,
                        responsibilities TEXT,
                        company_id INT REFERENCES employers(company_id)
            );
        """)

    conn.commit()
    conn.close()


def save_emp_to_database(data: list[dict[str, Any]], database_name: str, params: dict):
    """Сохранение данных о работодателях в базу данных."""

    params = config()
    conn = psycopg2.connect(dbname=database_name, **params)

    with conn.cursor() as cur:
        for emp in data:
            cur.execute(
                """
                INSERT INTO employers (company_id, company_name, company_url, vacancies_url, amount_of_vacancies) 
                VALUES (%s, %s, %s, %s, %s) 
                RETURNING company_id
                """,
                (emp['id'], emp['name'], emp['url'], emp['vacancies_url'], emp['open_vacancies'])
            )
    conn.commit()
    conn.close()


def save_vac_to_database(data: list[dict[str, Any]], database_name: str, params: dict):
    """Сохранение данных о вакансиях базу данных."""

    params = config()
    conn = psycopg2.connect(dbname=database_name, **params)

    with conn.cursor() as cur:
        for vacancy in data['items']:
            cur.execute(
                """
                INSERT INTO vacancies (vacancy_id, vacancy_name, vacancy_url, 
                requirements, responsibilities, company_id)
                VALUES (%s, %s, %s, %s, %s, %s)
                """,
                (vacancy['id'], vacancy['name'], vacancy['url'], vacancy['snippet']['requirement'],
                 vacancy['snippet']['responsibility'], vacancy['employer']['id'])
            )

            if vacancy['salary']['from'] is not None:
                cur.execute(
                    """
                    INSERT INTO vacancies (salary_from) VALUES vacancy['salary']['from'])
                    """
                )
            else:
                cur.execute(
                    """
                    INSERT INTO vacancies (salary_from) VALUES 0
                    """
                )

            if vacancy['salary']['currency'] is not None:
                cur.execute(
                    """
                    INSERT INTO vacancies (currency) VALUES vacancy['salary']['currency']
                    """
                )
            else:
                cur.execute(
                    """
                    INSERT INTO vacancies (salary_from) VALUES 'RUR'
                    """
                )

    conn.commit()
    conn.close()
