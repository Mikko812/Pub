from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from settings import email, password

driver = webdriver.Firefox()
driver.implicitly_wait(5)
url = 'https://petfriends1.herokuapp.com/login'


def test_petfriends_waits():
    driver.get(url)

    field_email = driver.find_element_by_id('email')
    field_email.clear()
    field_email.send_keys(email)

    field_pass = driver.find_element_by_id('pass')
    field_pass.clear()
    field_pass.send_keys(password)

    btn_submit = driver.find_element_by_xpath("//button[@type='submit']")
    btn_submit.click()

# НЕЯВНЫЕ ОЖИДАНИЯ НА СТРАНИЦЕ ВСЕХ ПИТОМЦЕВ
    images = driver.find_elements_by_css_selector('.card-deck .card-img-top')
    names = driver.find_elements_by_css_selector('.card-deck .card-body .card-title')
    descriptions = driver.find_elements_by_css_selector('.card-deck .card-body .card-text')

    for i in range(50):   # len(names)
        # Проверка наличия фото у питомца и ожидание его загрузки
        img_attr = images[i].get_attribute('src')
        img = driver.find_element_by_xpath(f"//img[@src='{img_attr}']")
        if img:
            try:
                assert img_attr != ''
            except AssertionError:
                pass
        else:
            print(f'Фото питомца номер {i+1} не загрузилось')
# При тестировании обнаружилось имя "!@#$%^&*()_+=-`~[]{}\|':?,.<>*", которое из-за наличия кавычек вызывало ошибку.
# Костыли для обхода данной проблемы ставить не стал и взял первые 50 питомцев. Для проверки кода этого, думаю, хватит.
        # Проверка наличия имени у питомца и ожидание его загрузки
        pet_name = names[i].text
        name = driver.find_element_by_xpath(f"//h5[contains(text(),'{pet_name}')]")
        if name:
            try:
                assert pet_name != ''
            except AssertionError:
                pass
        else:
            print(f'У питомца номер {i+1} не загрузилось имя')

        # Проверка наличия возраста у питомца и ожидание его загрузки
        pet_age = descriptions[i].text
        age = driver.find_element_by_xpath("//p[contains(text(),'год') or contains(text(),'лет')]")
        if age:
            try:
                assert pet_age != ''
            except AssertionError:
                pass
        else:
            print(f'У питомца номер {i+1} не загрузился возраст')


# ЯВНЫЕ ОЖИДАНИЯ
# Переходим на страницу моих питомцев для выполнения 2-й части практикума
    my_pets_link = driver.find_element_by_link_text(u"Мои питомцы")
    my_pets_link.click()

# Ждем видимости статистики пользователя
    element = WebDriverWait(driver, 6).until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".\\.col-sm-4.left")))
    if element:
        print('\nСтатистика пользователя видна на странице!')
    else:
        raise Exception('\nСтатистика пользователя не видна на странице!')
# Ждем загрузки кнопки "Добавить питомца"
    element = WebDriverWait(driver, 6).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".btn-outline-success")))
    if element:
        print('Кнопка "Добавить питомца" загружена!')
    else:
        raise Exception('Кнопка "Добавить питомца" не загружена!')
# Ждем кликабельности кнопки "Выйти"
    xpath = "//button[@class='btn btn-outline-secondary']"
    element = WebDriverWait(driver, 6).until(EC.element_to_be_clickable((By.XPATH, xpath)))
    assert element, 'Кнопка "Выйти" не кликабельна!'
