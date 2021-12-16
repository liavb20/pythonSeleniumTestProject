from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC
from DETAILS_FROM_EXCEL import Details_From_Excel


class AOS_Main_Page:
    def __init__(self, driver: webdriver):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 10)

    def category(self):
        # wait till the categories are visible
        self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'div[id="tabletsImg"]')))
        # return list of objects of each category
        return self.driver.find_elements(By.CSS_SELECTOR, ".rowSection>[role = 'link']")

    def number_on_the_cart_icon(self):
        # check if there is a number near the cart icon and returns it, if there is no number return zero
        if self.check_exists_by_CSS('#shoppingCartLink>[class="cart ng-binding"]'):
            return self.driver.find_element(By.CSS_SELECTOR, '#shoppingCartLink>[class="cart ng-binding"]').text
        return 0

    def check_exists_by_CSS(self, css_selector):
        # if the element exists return True
        try:
            self.driver.find_element(By.CSS_SELECTOR, css_selector)
        except NoSuchElementException:
            return False
        return True

    def click_cart_icon(self):
        # click the cart icon in order to move to the cart page
        self.driver.find_element(By.ID, 'menuCart').click()

    def click_tablet_category(self):
        # wait till the tablet category appears
        self.wait.until(EC.element_to_be_clickable((By.ID, "tabletsTxt")))
        # click on the tablet category in order to move to the tablet products page
        self.driver.find_element(By.ID, "tabletsTxt").click()

    def go_to_my_orders(self):
        # click on the user icon and its open some options
        self.driver.find_element(By.ID, 'menuUser').click()
        # click on 'my orders' button and move to my orders page
        self.driver.find_element(By.CSS_SELECTOR, '[id="loginMiniTitle"]>label[class="option ng-scope"]').click()


    def wait_to_login_window_open(self):
        # wait till the login window open
        self.wait.until(EC.visibility_of_element_located((By.NAME, "username")))

    def fill_username_password_and_login(self, username='liav10', password='Liav10'):
        details_of_exist_account = Details_From_Excel(10)
        # clear the username and password fields than fill them with the details
        self.driver.find_element(By.NAME, "username").clear()
        if details_of_exist_account.sheet['B18'].value != None:
            username = details_of_exist_account.sheet['B18'].value
        self.driver.find_element(By.NAME, "username").send_keys(username)
        self.driver.find_element(By.NAME, "password").clear()
        if details_of_exist_account.sheet['B19'].value != None:
            password = details_of_exist_account.sheet['B19'].value
        self.driver.find_element(By.NAME, "password").send_keys(password)
        # wait till the login button clickable
        self.wait.until(EC.element_to_be_clickable((By.ID, "sign_in_btnundefined")))
        # make sure - click the sign in button
        while True:
            try:
                self.driver.find_element(By.ID, "sign_in_btnundefined").click()
                break
            except:
                pass

    def click_account_icon(self):
        # click on tha user icon and its open some options
        self.driver.find_element(By.ID, 'menuUser').click()

    def check_if_login(self):
        # catch the element of the username near the user icon
        name_code = '''[data-ng-mouseleave="miniTitleOut('loginMiniTitle')"]>[data-ng-show="userCookie.response"]'''
        # wait until the username appears
        self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, name_code)))
        # convert the name element to the name
        name_near_icon = self.driver.find_element(By.CSS_SELECTOR, name_code).text
        # if the name length more than zero than the login succeed and return true
        if len(name_near_icon) > 0:
            return True
        else:
            return False

    def logout_click(self):
        # click the button sign out
        self.driver.find_element(By.CSS_SELECTOR, '[id="loginMiniTitle"]>[translate="Sign_out"]').click()

    def wait_for_the_web_and_click_account_icon(self):
        # try click the account icon
        while True:
            try:
                self.driver.find_element(By.ID, 'menuUser').click()
                break
            except:
                pass

    def check_if_logout(self):
        # catch the name of the username  that appears near the user icon
        name_to_disappear = '''[data-ng-mouseleave="miniTitleOut('loginMiniTitle')"]>[data-ng-show="userCookie.response"]'''
        # wait until the username disappear, if it doesn't disappear the account still login and we get False
        # if the name disappear the logout succeed and we get True
        try:
            self.wait.until(EC.invisibility_of_element_located((By.CSS_SELECTOR, name_to_disappear)))
        except TimeoutError:
            return False
        return True
