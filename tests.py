from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

class AddStockTestCase(LiveServerTestCase):
    def test_add_stock(self):
        selenium = webdriver.Firefox()
        selenium.get("http://0.0.0.0:8005/pos/stock")

        add_button = selenium.find_element(by=By.CLASS_NAME, value="btn-primary2")
        add_button.click()

        amount_added_textbox = selenium.find_element(by=By.ID, value="amount_added")
        amount_added_textbox.send_keys("1")

        outer_container = selenium.find_element(by=By.CLASS_NAME, value="modal-content")
        submit_button = outer_container.find_element(by=By.CLASS_NAME, value="btn-primary")
        submit_button.click()

        assert 'Product 10' in selenium.page_source
        selenium.quit()

class AddProductTestCase(LiveServerTestCase):
    def test_add_product(self):
        selenium = webdriver.Firefox()
        selenium.get("http://0.0.0.0:8005/pos/save_product")
        
        name_text_box = selenium.find_element(by=By.ID, value="name")
        quantity_text_box = selenium.find_element(by=By.ID, value="quantity")
        price_text_box = selenium.find_element(by=By.ID, value="unit_price")
        description_text_box = selenium.find_element(by=By.ID, value="description")

        outer_container = selenium.find_element(by=By.CLASS_NAME, value="modal-content")
        submit_button = outer_container.find_element(by=By.CLASS_NAME, value="btn-primary")

        name_text_box.send_keys("Product 10")
        quantity_text_box.send_keys("10")
        price_text_box.send_keys("2000")
        description_text_box.send_keys("Quality Product")

        selenium.implicitly_wait(3000)
        submit_button.click()

        message = selenium.find_element(by=By.CLASS_NAME, value="message")
        text = message.text

        assert 'Product 10' in selenium.page_source
        selenium.quit()
