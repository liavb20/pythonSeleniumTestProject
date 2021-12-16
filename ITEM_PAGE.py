from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException


class Item_Page:
    def __init__(self, driver: webdriver):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 10)
        self.name_items = []
        self.color_items = []
        self.price_item = []

    # clean the quantity box and return the element
    def quantity_box(self):
        # find the element of the quantity box
        amount_box = self.driver.find_element(By.NAME, 'quantity')
        # click on the quantity box
        amount_box.click()
        # clean the quantity box
        amount_box.send_keys(Keys.BACKSPACE)
        # return the clean quantity box object
        return amount_box

    def all_colors(self):
        # there are two types of elements for the colors so the if check if the colors from the first type
        # if its the first type the function return the all colors of the specific product
        # if its the second type the function also return the all colors of the specific product
        if self.check_exists_by_CSS('[ng-show="firstImageToShow"]>span'):
            return self.driver.find_elements(By.CSS_SELECTOR, '[ng-show="firstImageToShow"]>span')
        else:
            return self.driver.find_elements(By.CSS_SELECTOR, '[ng-show="!firstImageToShow"]>span')

    def add_item_price(self):
        # the element of the price
        price_element = self.driver.find_element(By.CSS_SELECTOR,'[class = "max-width "]>div>div>h2[class="roboto-thin screen768 ng-binding"]')
        # grab the text of the element without the $ remark
        price_element = price_element.text[1:]
        # check if the price have comma and delete it
        if ',' in price_element:
            price_element = price_element.replace(',', '')
        # change the price type from string to float
        price = float(price_element)
        # add the price to list of prices
        self.price_item.append(price)

    def click_add_to_cart(self):
        # call the function to insert the price to the list
        self.add_item_price()
        # click the add to cart button
        self.driver.find_element(By.NAME, 'save_to_cart').click()

    def return_to_home_page(self):
        # return to home page
        self.driver.find_element(By.CSS_SELECTOR, "a>span.roboto-medium").click()

    def sold_out_item(self):
        # check if the product is sold out
        if not self.check_exists_by_CSS('[class="roboto-thin screen768 ng-binding"]>[class="roboto-medium ng-scope"]'):
            prodname = self.driver.find_element(By.CSS_SELECTOR, 'h1[class = "roboto-regular screen768 ng-binding"]')
            # if it not sold out check if the product had already chosen
            if prodname.text in self.name_items:
                return True
            self.name_items.append(prodname.text)
            return False
        else:
            # if the product sold out we return to the home page
            self.return_to_home_page()
            return True

    def check_exists_by_CSS(self, css_selector):
        # if the element exists return true
        try:
            self.driver.find_element(By.CSS_SELECTOR, css_selector)
        except NoSuchElementException:
            return False
        return True
