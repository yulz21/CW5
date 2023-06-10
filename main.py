from confyg import config
from utils import select_companies, choose_option
from classes import EmployerRequest, VacancyRequest
from db_functions import create_database, save_emp_to_database, save_vac_to_database
from db_manager import DBManager

if __name__ == '__main__':
    params = config()

    companies = select_companies()

    for company in companies:
        employer = EmployerRequest(company)
        emp_data = employer.get_data(company, 50)
        emp_ids = employer.get_id(emp_data)

    for item in emp_ids:
        vac = VacancyRequest(item)
        vac_data = vac.get_data(5)

    db_name = input("Укажите имя для сохранения базы данных: ").capitalize()

    create_database(db_name, params)

    save_emp_to_database(emp_data, db_name, params)
    save_vac_to_database(vac_data, db_name, params)

    print(f"База данных {db_name} успешно создана")


    action = choose_option()

    print(f"\n\n{'*' * 200}\n\n")

    data_manager = DBManager(db_name, **params)


    if action == "1":
        data = data_manager.get_companies_and_vacancies_count()
        for item in data:
            print(*item, sep=', ')

    elif action == '2':
        data = data_manager.get_all_vacancies()
        for item in data:
            print(*item, sep=', ')

    elif action == '3':
        data = data_manager.get_avg_salary()
        for item in data:
            print(*item, sep=', ')

    elif action == '4':
        data = data_manager.get_vacancies_with_higher_salary()
        for item in data:
            print(*item, sep=', ')
    else:
        k_word = input("Введите ключевое слово для поиска: ")
        data = data_manager.get_vacancies_with_keyword(k_word)
        for item in data:
            print(*item, sep=', ')
