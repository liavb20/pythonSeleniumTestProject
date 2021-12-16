from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class My_Orders_Page:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 5)

    def get_orderid(self):
        # wait until the page open
        self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '[class="roboto-regular sticky fixedImportant ng-scope"]')))
        # catch the order id (for new account that have only one order)
        obj_orderid= self.driver.find_element(By.XPATH, '//*[@id="myAccountContainer"]/div/table/tbody/tr[2]/td[1]/label').text
        return obj_orderid

    def get_list_orderid(self):
        # catch the table of the orders in the page
        table = self.driver.find_element(By.CSS_SELECTOR, '[class="cover"]>table>tbody')
        # catch the rows in the table
        rows = table.find_elements(By.TAG_NAME, 'tr')
        # cancel the row of the headlines
        rows = rows[1:]
        orders_list = []
        # loop run for each row and insert the order numbers to list
        for i in range(len(rows)):
            orders_list.append(rows[i].find_element(By.CSS_SELECTOR, 'td>label[class="ng-binding"]').text)
        return orders_list
