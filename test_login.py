from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service 
from selenium.common.exceptions import UnexpectedAlertPresentException, NoAlertPresentException

import time

# Пути
CHROMEDRIVER_PATH = "/usr/bin/chromedriver"
CHROMIUM_BINARY = "/usr/bin/chromium-browser"

# Настройки опций
options = webdriver.ChromeOptions()
options.binary_location = CHROMIUM_BINARY
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
# options.add_argument("--headless")  # если нужен headless режим

# Сервис
service = Service(CHROMEDRIVER_PATH)


def test_guest_login():
    driver = webdriver.Chrome(service=service, options=options)
    driver.get("http://localhost:8080/login")

    guest_link = driver.find_element(By.LINK_TEXT, "Войти как гость")
    guest_link.click()

    time.sleep(2)
    assert "Каталог" in driver.page_source

    driver.quit()


def test_login_success():
    driver = webdriver.Chrome(service=service, options=options)
    driver.get("http://localhost:8080/login")

    username = driver.find_element(By.CSS_SELECTOR, 'input[type="text"]')
    password = driver.find_element(By.CSS_SELECTOR, 'input[type="password"]')
    login_button = driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]')

    username.send_keys("ivanov")
    password.send_keys("123")
    login_button.click()

    time.sleep(2)

    try:
        alert = driver.switch_to.alert
        print("Alert text:", alert.text)
        alert.accept()
        assert False, "Логин неуспешен: получен alert"
    except NoAlertPresentException:
        pass

    assert "Каталог" in driver.page_source
    driver.quit()



# Запуск тестов
test_guest_login()
test_login_success()