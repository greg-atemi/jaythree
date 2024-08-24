from selenium import webdriver
from selenium.webdriver.common.by import By

driver = webdriver.Firefox()

driver.get("http://35.241.207.130:8000/pos/stock")

driver.implicitly_wait(0.5)

add_button = driver.find_element(by=By.CLASS_NAME, value="btn-primary2")
add_button.click()

amount_added_textbox = driver.find_element(by=By.ID, value="amount_added")
amount_added_textbox.send_keys("1")

outer_container = driver.find_element(by=By.CLASS_NAME, value="modal-content")
submit_button = outer_container.find_element(by=By.CLASS_NAME, value="btn-primary")
submit_button.click()