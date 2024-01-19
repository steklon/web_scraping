from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver import Chrome
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions


def wait_element(browser, delay_second=1, by=By.TAG_NAME, value=None):
    return WebDriverWait(browser, delay_second).until(
        expected_conditions.presence_of_element_located((by, value))
    )


path = ChromeDriverManager().install()
browser_service = Service(executable_path=path)
browser = Chrome(service=browser_service)
browser.get('https://spb.hh.ru/search/vacancy?'
            'L_save_area=true&search_field=description&'
            'area=1&area=2&items_on_page=50&enable_snippets=false&text=Python+django+flask')
parsed_data = list()

vacancy_list_tag = wait_element(browser, 1, By.TAG_NAME, 'main')

count = 0
for page_list_tag in vacancy_list_tag.find_elements(By.CLASS_NAME, 'vacancy-serp-item-body__main-info'):
    title_tag = wait_element(page_list_tag, 1, By.TAG_NAME, 'h3')
    company_name_tag = page_list_tag.find_element(By.CLASS_NAME, 'vacancy-serp-item__meta-info-company')
    city_tag = page_list_tag.find_element(By.XPATH, '//div[@data-qa="vacancy-serp__vacancy-address"]')

    print(title_tag.text)
    print(company_name_tag.text)
    print(city_tag.text)
    count += 1
    print("**************************")

print(count)
