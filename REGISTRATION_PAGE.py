from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from DETAILS_FROM_EXCEL import Details_From_Excel


class Registration_Page:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 10)
        self.username = ''
        self.password = ''
        self.mail = ''

    def fill_details_and_finish_order(self, username='ABCDEFG123', password='Liav10', mail='liav@liav.liav'):
        # get details by default if in the test did not send details
        details_of_new_account = Details_From_Excel(8)
        # if the cell of new username is not empty take username from there
        if details_of_new_account.sheet['B20'].value != None:
            self.username = details_of_new_account.sheet['B20'].value
        # take username by default
        else:
            self.username = username
        # if the cell of new password is not empty take password from there
        if details_of_new_account.sheet['B21'].value != None:
            self.password = details_of_new_account.sheet['B21'].value
        # get details by default if in the test did not send details
        else:
            self.password = password
        # if the cell of new mail is not empty take mail from there
        if details_of_new_account.sheet['B22'].value != None:
            self.mail = details_of_new_account.sheet['B22'].value
        # get details by default if in the test did not send details
        else:
            self.mail = mail
        # send the username to the element of the username box
        self.driver.find_element(By.NAME, 'usernameRegisterPage').send_keys(self.username)
        # send the password to the element of the password box
        self.driver.find_element(By.NAME, 'passwordRegisterPage').send_keys(self.password)
        # send the password to the element of the password box
        self.driver.find_element(By.NAME, "confirm_passwordRegisterPage").send_keys(self.password)
        # send the mail to the element of the mail box
        self.driver.find_element(By.NAME, 'emailRegisterPage').send_keys(self.mail)
        # wait until the element of the "i agree" become visible
        self.wait.until(EC.visibility_of_element_located((By.NAME, "i_agree")))
        # wait until the element of the "i agree" become clickable
        self.wait.until(EC.element_to_be_clickable((By.NAME, "i_agree")))
        # click the "i agree" button
        while not self.driver.find_element(By.NAME, 'i_agree').is_selected():
            self.driver.find_element(By.NAME, "i_agree").click()
        # wait until the register button become clickable
        self.wait.until(EC.element_to_be_clickable((By.ID, "register_btnundefined")))
        # click the register button
        while True:
            try:
                self.driver.find_element(By.ID, "register_btnundefined").click()
                break
            except:
                pass
        # wait until the next button appears
        self.wait.until(EC.visibility_of_element_located((By.ID, "next_btn")))
        # click the next button
        self.driver.find_element(By.ID, "next_btn").click()

        # fill the safe pay username with the details "liavb20"
        if details_of_new_account.sheet['B23'] != None:
            self.driver.find_element(By.NAME, "safepay_username").send_keys(details_of_new_account.sheet['B23'].value)
        else:
            self.driver.find_element(By.NAME, "safepay_username").send_keys('liavb20')
        # fill the safe pay password with the details "liavb20"
        if details_of_new_account.sheet['B24'] != None:
            self.driver.find_element(By.NAME, "safepay_password").send_keys(details_of_new_account.sheet['B24'].value)
        else:
            self.driver.find_element(By.NAME, "safepay_password").send_keys('Liavb20')
        # click the pay now button
        self.driver.find_element(By.ID, "pay_now_btn_SAFEPAY").click()
        # wait until the order number appear
        self.wait.until(EC.visibility_of_element_located((By.ID, "orderNumberLabel")))
        # catch the element of the order number
        orderid = self.driver.find_element(By.XPATH, '//*[@id="orderNumberLabel"]')
        # return the text of the element
        return orderid.text