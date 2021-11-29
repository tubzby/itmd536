from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import login

if __name__ == '__main__':
    driver = webdriver.Chrome()
    # replace it with the right username and password
    username = 'tubzby@gmail.com'
    password = '123456'

    login = login.Login(driver, username, password)
    login.run()

    time.sleep(1000)
