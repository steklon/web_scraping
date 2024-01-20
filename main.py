import json
from pprint import pprint

import requests
from bs4 import BeautifulSoup
import fake_headers


def gen_headers():
    headers_gen = fake_headers.Headers(os='win', browser='chrome')
    return headers_gen.generate()


def get_common_list(url):
    main_response = requests.get(
        url,
        headers=gen_headers())

    main_html_data = main_response.text
    main_soup = BeautifulSoup(main_html_data, 'lxml')
    vacancy_list_tag = main_soup.find('main', class_='vacancy-serp-content')
    return vacancy_list_tag


def get_page_links(url):
    url_list = [url]
    vacancy_list_tag = get_common_list(url)
    for page_list in vacancy_list_tag.find('div', class_='pager'):
        page = page_list.find_all('a', {'data-qa': 'pager-page'})
        if page:
            url_list.append(f"https://spb.hh.ru{page[0]['href']}")
    get_result_list(url_list)


def get_result_list(url_list):
    result_list = list()

    for link in url_list:
        for data in get_data(link):
            result_list.append(data)

    write_to_json(result_list)
    pprint(result_list)
    pprint(len(result_list))


def get_data(url):
    vacancy_list_tag = get_common_list(url)
    parsed_data = list()
    for vacancy_tag in vacancy_list_tag.find_all(
            'div', class_='vacancy-serp-item-body__main-info'):
        title_tag = vacancy_tag.find('span', class_='serp-item__title')
        a_tag = vacancy_tag.find('a', class_='bloko-link')
        company_name_tag = vacancy_tag.find(
            'a', class_='bloko-link bloko-link_kind-tertiary')
        city_tag = vacancy_tag.find(
            'div', {'data-qa': 'vacancy-serp__vacancy-address'})
        salary_tag = vacancy_tag.find(
            'span', class_='bloko-header-section-2')

        header = title_tag.text.strip()
        link = a_tag['href']
        company = company_name_tag.text
        city = city_tag.text
        if salary_tag is None:
            salary = 'зарплата не указана'
        else:
            salary = salary_tag.text

        parsed_data.append({
            'title': header,
            'company': company.replace("\xa0", " "),
            'city': city.replace(
                "\xa01\xa0", " ").replace(
                "\xa02\xa0", " ").replace(
                "\xa03\xa0", " "),
            'salary': salary.replace("\u202f", " "),
            'url': link
        })

    return parsed_data


def write_to_json(data):
    with open("parsed.json", "wt", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)


if __name__ == '__main__':
    link_ = ('https://spb.hh.ru/search/vacancy?L_save_area=true&'
             'search_field=description&area=1&area=2&items_on_page=20&'
             'enable_snippets=false&text=Python+django+flask')
    get_page_links(link_)
