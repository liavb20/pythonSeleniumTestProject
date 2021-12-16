from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains
from DETAILS_FROM_EXCEL import Details_From_Excel


class Cart_Page:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 10)
        self.actions = ActionChains(self.driver)

    def shopping_cart_appears(self):
        # catch element which exist only in shopping cart page
        shopping_obj = self.driver.find_element(By.CSS_SELECTOR, '[class="select  ng-binding"]')
        # make sure the object text is SHOPPING CART
        if shopping_obj.text == "SHOPPING CART":
            return True
        return False

    def get_price(self):
        # catch the total price element
        price_element = self.driver.find_element(By.CSS_SELECTOR, 'table[class="fixedTableEdgeCompatibility"]>tfoot>tr>td[colspan="2"]>span[class="roboto-medium ng-binding"]')
        # change the element to text and cut the $ mark
        price_element = price_element.text[1:]
        # if there is comma in the price then cut it
        if ',' in price_element:
            price_element = price_element.replace(',', '')
        # change the price type from string to float
        price_element = float(price_element)
        return price_element

    def wait_the_edit_buttons(self):
        # wait till the cart panel disappear and the top edit button visible
        self.wait.until(EC.visibility_of_element_located((By.XPATH, "//*[@id='shoppingCart']/table/tbody/tr[1]/td[6]/span/a[1]")))

    def quantity_of_products_in_cart_page(self):
        # catch the quantities element for each product
        quantities = self.driver.find_elements(By.CSS_SELECTOR, 'td[class="smollCell quantityMobile"]>label[class="ng-binding"]')
        # change the element text and then to int
        list_quantities = [int(i.text) for i in quantities]
        return list_quantities

    def add_2_quantities_each_product(self):
        # wait until all the edit buttons appear
        self.wait.until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, 'a[class="edit ng-scope"]')))
        # catch the elements of the edit buttons
        edit_buttons = self.driver.find_elements(By.CSS_SELECTOR, 'a[class="edit ng-scope"]')
        len_buttons = len(edit_buttons)
        # run loop for each edit button
        for i in range(len_buttons):
            # wait till the elements of the cart panel be invisible
            self.wait.until(EC.invisibility_of_element_located((By.CSS_SELECTOR, 'h3.ng-binding')))
            # catch the elements of the edit buttons
            edit_buttons = self.driver.find_elements(By.CSS_SELECTOR, 'a[class="edit ng-scope"]')
            # for each loop click on edit button
            edit_buttons[i].click()
            # click twice on the plus button in order to increase the quantity by two
            self.driver.find_element(By.CLASS_NAME, 'plus').click()
            self.driver.find_element(By.CLASS_NAME, 'plus').click()
            # click on add to cart button
            self.driver.find_element(By.NAME, 'save_to_cart').click()

    def click_checkout_button(self):
        # click the check out button
        self.driver.find_element(By.ID, 'checkOutButton').click()

    def click_registration_button(self):
        # click the registration button
        self.driver.find_element(By.ID, 'registration_btnundefined').click()

    def check_if_the_cart_empty(self):
        # tru to catch element which appears only when the cart is empty
        try:
            self.driver.find_element(By.CLASS_NAME, 'roboto-bold ng-scope')
        except NoSuchElementException:
            return False
        return True

    def fill_login_details_and_click_login_button(self, username='liav10', password='Liav10'):
        details_of_exist_account = Details_From_Excel(9)
        # check if the cell of the username login is exist and put him in the username var
        if details_of_exist_account.sheet['B18'].value != None:
            username = details_of_exist_account.sheet['B18'].value
        # if the cell is empty, username var get the default
        else:
            username = username
        # check if the cell of the password login is exist and put him in the password var
        if details_of_exist_account.sheet['B19'].value != None:
            password = details_of_exist_account.sheet['B19'].value
        # if the cell is empty, password var get the default
        else:
            password = password
        # catch the element of the username and send it to the login box
        self.driver.find_element(By.NAME, "usernameInOrderPayment").send_keys(username)
        # catch the element of the password and send it to the login box
        self.driver.find_element(By.NAME, "passwordInOrderPayment").send_keys(password)
        # wait until the sign in button become clickable
        self.wait.until(EC.element_to_be_clickable((By.ID, "login_btnundefined")))
        # click on the sign in button
        self.driver.find_element(By.ID, 'login_btnundefined').click()

    def continue_to_finish_order(self):
        details_of_exist_account = Details_From_Excel(9)
        # click the continue button in the confirm details
        self.driver.find_element(By.ID, "next_btn").click()
        # click on master card option to pay with credit card
        self.driver.find_element(By.NAME, "masterCredit").click()
        # try fill the details of the credit card except click continue(if the details had already saved
        try:
            # take the credit card number from the excel if the cell not empty
            if details_of_exist_account.sheet['B25'].value != None:
                self.driver.find_element(By.ID, "creditCard").send_keys(details_of_exist_account.sheet['B25'].value)
            else:
                # if empty use default
                self.driver.find_element(By.ID, "creditCard").send_keys(999999999999)
            # take the credit card CVV number from the excel if the cell not empty
            if details_of_exist_account.sheet['B26'].value != None:
                self.driver.find_element(By.NAME, "cvv_number").send_keys(details_of_exist_account.sheet['B26'].value)
            # if empty use default
            else:
                self.driver.find_element(By.NAME, "cvv_number").send_keys(123)
            # take the credit card holder name from the excel if the cell not empty
            if details_of_exist_account.sheet['B27'].value != None:
                self.driver.find_element(By.NAME, "cardholder_name").send_keys(details_of_exist_account.sheet['B27'].value)
            # if empty use default
            else:
                self.driver.find_element(By.NAME, "cardholder_name").send_keys("moshe")
            # click the pay now button
            self.driver.find_element(By.ID, "pay_now_btn_ManualPayment").click()
        except:
            # if all the details had already saved, just click the pay now button
            self.driver.find_element(By.NAME, "pay_now_btn_MasterCredit").click()
        # wait until the number order appears
        self.wait.until(EC.visibility_of_element_located((By.ID, "orderNumberLabel")))
        # return the text of the element of the number order
        return self.driver.find_element(By.ID, 'orderNumberLabel').text

