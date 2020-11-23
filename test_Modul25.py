from selenium import webdriver
from settings import email, password

driver = webdriver.Firefox()
url = 'https://petfriends1.herokuapp.com/login'


def test_petfriends():
    driver.get(url)

    field_email = driver.find_element_by_id('email')
    field_email.clear()
    field_email.send_keys(email)

    field_pass = driver.find_element_by_id('pass')
    field_pass.clear()
    field_pass.send_keys(password)

    btn_submit = driver.find_element_by_xpath("//button[@type='submit']")
    btn_submit.click()

    my_pets_link = driver.find_element_by_link_text(u"Мои питомцы")
    my_pets_link.click()

# Проверка пункта 1. Присутствуют все питомцы.
# pets_count - количество питомцев, подсчитанное системой
    pets_count = driver.find_element_by_css_selector(".\\.col-sm-4.left")
    txt = pets_count.get_attribute('textContent')
    pets_count = int(txt.split('Друзей')[0].split(': ')[-1])
# pets_count_tab - реальное количество питомцев
    pets_count_table = driver.find_elements_by_css_selector("tr")[1:]
    pets_count_tab = len(pets_count_table)
    assert pets_count_tab == pets_count, 'Количество питомцев не совпадает!'
    print('\nПункт 1. Количество питомцев в таблице совпадает с количеством в левом столбце.')

# Проверка пункта 2. Хотя бы у половины питомцев есть фото.
    pets_no_photo = driver.find_elements_by_xpath("//img[@src='']")
    assert len(pets_no_photo) <= int(pets_count/2), 'Питомцев без фото больше половины!'
    print(f'\nПункт 2. Хотя бы у половины питомцев есть фото. Всего питомцев - {pets_count}. '
          f'Без фото - {len(pets_no_photo)}')

# Проверка пункта 3. У всех питомцев есть имя, возраст и порода.
    names = []   # список имен для пункта 4
    my_pets = []   # список списков атрибутов питомцев для пункта 5
    for i in range(len(pets_count_table)):
        curr_pet_attr = pets_count_table[i].find_elements_by_tag_name("td")
        names.append(curr_pet_attr[0].get_attribute('textContent'))
        tmp = []
        for a in range(0, 3):
            tmp.append(curr_pet_attr[a].get_attribute('textContent').strip())
            assert curr_pet_attr[a].get_attribute('textContent') != '', 'У питомца нет атрибута!'
        my_pets.append(tmp)
    print('\nПункт 3. У всех питомцев есть имя, порода и возраст.')

# Проверка пункта 4. У всех питомцев разные имена.
    assert len(names) == len(set(names)), 'Есть одинаковые имена!'
    print('\nПункт 4. У всех питомцев разные имена.')

# Проверка пункта 5. В списке нет повторяющихся питомцев.
    for i in range(1, len(pets_count_table) - 1):
        assert my_pets[i-1] not in my_pets[i:], 'Есть питомцы с одинаковыми данными!'
    print('\nПункт 5. Повторяющиеся питомцы не идентифицированы.')
