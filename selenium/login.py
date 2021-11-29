from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


class Login:
    def __init__(self, driver, email, password):
        self.driver = driver
        self.email = email
        self.password = password

    def login_no_user(self):
        self.driver.get("http://hellboycc.cn/auth/login")
        # find all the element
        usernameElement = self.driver.find_element(By.ID, 'email')
        passwordElement = self.driver.find_element(By.ID, 'password')
        submitBtnElement = self.driver.find_element(By.ID, 'submit')

        # send input values
        passwordElement.send_keys(self.password)
        # click login button
        submitBtnElement.click()

        elem = WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located(
                (By.XPATH, '/html/body/main/div[1]'))  # This is a dummy element
        )

        if 'The email can\'t be empty.' not in elem.text:
            print('invalid alert message')
            return False
        print('login_no_user passed')
        return True

    def login(self):
        self.driver.get("http://hellboycc.cn/auth/login")

        # find all the element
        usernameElement = self.driver.find_element(By.ID, 'email')
        passwordElement = self.driver.find_element(By.ID, 'password')
        submitBtnElement = self.driver.find_element(By.ID, 'submit')

        # send input values
        usernameElement.send_keys(self.email)
        passwordElement.send_keys(self.password)
        # click login button
        submitBtnElement.click()

        # wait 5 seconds for a server to process

        elem = WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located(
                (By.XPATH, '/html/body/main/div[1]'))  # This is a dummy element
        )
        if 'Welcome back' not in elem.text:
            print('test failed')
            return False

        print('login test passed')
        return True

    def run(self):
        if self.login_no_user() != True:
            print('login_no_user test failed')
        if self.login() != True:
            print('login test failed')
