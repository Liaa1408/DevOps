
import os
import time
import pytest

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.alert import Alert
from webdriver_manager.chrome import ChromeDriverManager


BASE_URL = os.environ.get(
    "TEST_URL", "http://127.0.0.1:5001/"
)


@pytest.fixture
def setup_teardown():
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    driver.implicitly_wait(3)

    yield driver

    driver.quit()


def get_alert_text(driver):
    alert = Alert(driver)
    text = alert.text
    alert.accept()
    return text


def test_empty_username(setup_teardown):
    driver = setup_teardown
    driver.get(BASE_URL)

    driver.find_element(By.NAME, "username").clear()
    driver.find_element(By.NAME, "pwd").send_keys("Password123")
    driver.find_element(By.NAME, "sb").click()

    time.sleep(0.5)
    assert get_alert_text(driver) == "Username cannot be empty."


def test_empty_password(setup_teardown):
    driver = setup_teardown
    driver.get(BASE_URL)

    driver.find_element(By.NAME, "username").send_keys("")
    driver.find_element(By.NAME, "pwd").clear()
    driver.find_element(By.NAME, "sb").click()

    time.sleep(0.5)
    assert get_alert_text(driver) == "Password cannot be empty."


def test_short_password(setup_teardown):
    driver = setup_teardown
    driver.get(BASE_URL)

    driver.find_element(By.NAME, "username").send_keys("suhitha")
    driver.find_element(By.NAME, "pwd").send_keys("abc1")
    driver.find_element(By.NAME, "sb").click()

    time.sleep(0.5)
    assert get_alert_text(driver) == (
        "Password must be at least 6 characters long."
    )




def test_valid_input(setup_teardown):
    driver = setup_teardown
    driver.get(BASE_URL)

    username = driver.find_element(By.NAME, "username")
    username.clear()
    username.send_keys("suhitha")

    password = driver.find_element(By.NAME, "pwd")
    password.clear()
    password.send_keys("MyPassword123")

    driver.find_element(By.NAME, "sb").click()

    # Wait for the result and verify the greeting
    from selenium.webdriver.support.ui import WebDriverWait

    WebDriverWait(driver, 5).until(
        lambda d: "Hello, suhitha!" in d.page_source
    )

    assert "Welcome to the website" in driver.page_source
