
import psycopg2


class DBManager:
    """Обеспечивает взаимодействие с базой данных"""
    def __init__(self, dbname: str, user: str, password: str, host: str = 'localhost', port: str = '5432') -> None:
        """При инициализации объекта создаётся соединение и курсор"""

        self.dbname = dbname
        self.user = user
        self.password = password
        self.host = host
        self.port = port

        # Создаем соединение
        self.conn = psycopg2.connect(host=self.host, database=self.dbname, user=self.user, password=self.password, port=self.port)
        # Создаем курсор
        self.cur = self.conn.cursor()
        # Создаем автокоммит
        self.conn.autocommit = True
    def get_companies_and_vacancies_count(self) -> list[tuple]:
        """Возвращает список всех компаний и количество вакансий у каждой компании"""
        with self.conn:
            self.cur.execute(f"""SELECT company_name, amount_of_vacancies FROM employers""")
            empl_and_vac_count = self.cur.fetchall()
            return empl_and_vac_count

    def get_all_vacancies(self) -> list[tuple]:
        """Возвращает список всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на вакансию"""
        with self.conn:
            self.cur.execute(f"""SELECT vacancy_name, salary_from, currency, vacancy_url
                                 FROM vacancies
                                 """)
            all_vacancies = self.cur.fetchall()
            return all_vacancies

    def get_avg_salary(self) -> tuple:
        """Возвращает среднюю зарплату по вакансиям"""
        with self.conn:
            self.cur.execute(f"""SELECT (AVG(salary_from)) AS average_salary FROM vacancies""")
            avg_salary = self.cur.fetchone()
            return avg_salary

    def get_vacancies_with_higher_salary(self) -> list[tuple]:
        """Возвращает список всех вакансий, у которых зарплата выше средней по всем вакансиям"""
        with self.conn:
            self.cur.execute(f"""SELECT * FROM vacancies 
                                 WHERE salary_from > (SELECT (AVG(salary_from)) FROM vacancies)
                                 """)
            higher_salary = self.cur.fetchall()
            return higher_salary

    def get_vacancies_with_keyword(self, keyword: str) -> list[tuple]:
        """Возвращает список всех вакансий, в названии которых содержится ключевое слово"""
        with self.conn:
            self.cur.execute(f"""SELECT * FROM vacancies 
                                 WHERE vacancy_name LIKE '%{keyword}%'
                                 """)
            vac_key_word = self.cur.fetchall()
            return vac_key_word


