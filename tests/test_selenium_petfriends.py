import time
from selenium.webdriver.common.by import By


def test_petfriends(web_browser):
    web_browser.get('https://petfriends.skillfactory.ru/')
    time.sleep(5)

    btn_new_user = web_browser.find_element(By.XPATH, "//button[@onclick=\"document.location='/new_user';\"]")
    btn_new_user.click()

    btn_exist_akk = web_browser.find_element(By.LINK_TEXT, u"У меня уже есть аккаунт")
    btn_exist_akk.click()

    field_email = web_browser.find_element(By.ID, "email")
    field_email.clear()
    field_email.send_keys("solomonslava1991@gmail.com")

    field_pass = web_browser.find_element(By.ID, "pass")
    field_pass.clear()
    field_pass.send_keys("solomon0204")

    btn_submit = web_browser.find_element(By.XPATH, "//button[@type='submit']")
    btn_submit.click()

    time.sleep(10)
    if web_browser.current_url == 'https://petfriends.skillfactory.ru/all_pets':
        web_browser.save_screenshot("result_petfriends.png")
    else:
        raise Exception("login error")