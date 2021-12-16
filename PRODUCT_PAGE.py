from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains


class Product_Page:
    def __init__(self, driver: webdriver):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 5)
        # create an object of ActionChains in order to have a better control in the mouse
        self.actions = ActionChains(self.driver)


    def product(self):
        # wait till the url change from the main page url
        while True:
            if self.driver.current_url != 'https://www.advantageonlineshopping.com/#/':
                break
            else:
                pass
        # wait till the products appear on the page
        self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '[class="cell categoryRight"]')))
        # catch the element of all the products
        products_element = self.driver.find_element(By.CSS_SELECTOR, "[class = 'cell categoryRight']>ul")
        # create a list of the products elements and return it
        list_of_products = products_element.find_elements(By.TAG_NAME, 'li')
        return list_of_products

    def return_to_home_page(self):
        # return to the main page
        self.driver.find_element(By.CSS_SELECTOR, "a>span.roboto-medium").click()

    def move_mouse_to_cart_icon(self):
        # use action chains to move the mouse pointer to the cart icon
        self.actions.move_to_element(self.driver.find_element(By.ID, 'menuCart'))
        self.actions.perform()
        # wait till the panel cart open
        self.wait.until(EC.visibility_of_element_located((By.ID, "checkOutPopUp")))


