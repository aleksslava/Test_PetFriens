import time
from selenium.webdriver.common.by import By
def test_search_selenium(selenium):
    selenium.get('https://google.com')
    time.sleep(5)

    search_input = selenium.find_element(By.NAME, 'q')
    search_input.clear()
    search_input.send_keys('first keys')

    time.sleep(5)

    search_button = selenium.find_element(By.NAME, 'btnK')

    search_button.click()
    time.sleep(10)
    selenium.save_screenshot('result.png')
