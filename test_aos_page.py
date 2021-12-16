from random import randint
from unittest import TestCase
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from DETAILS_FROM_EXCEL import Details_From_Excel
from openpyxl import load_workbook
from MAIN_PAGE import AOS_Main_Page
from PRODUCT_PAGE import Product_Page
from ITEM_PAGE import Item_Page
from CART_PANEL import Cart_Panel
from CART_PAGE import Cart_Page
from REGISTRATION_PAGE import Registration_Page
from MY_ORDERS_PAGE import My_Orders_Page


class TestAOS_Main_Page(TestCase):
    def category_from_excel(self):
        # dictionary of the categories and their order
        dic = {'SPEAKERS': 0, 'TABLETS': 1, 'LAPTOPS': 2, 'MICE': 3, 'HEADPHONES': 4}
        # the dictionary get the category name from the excel file and the var get the number of the category
        category_number = dic[self.details_from_excel.categories()]
        # got list of categories
        categories = self.main_aos_page.category()
        # element of chosen category
        category = categories[category_number]
        # click on category
        category.click()

    def product_from_excel(self):
        # create object from Product_Page type
        product_page = Product_Page(self.driver)
        # get a list of products in the specific category
        products = product_page.product()
        # the var get the number of the product from the chosen category
        x = self.details_from_excel.product_numbers()
        # click on the product in order to move to its page
        products[x].click()

    def quantity_1to5(self):
        # take quantity number between 1 to 5 from the excel file
        x = self.details_from_excel.quantities()
        # get the element of the clean quantity box
        amount_box = self.item.quantity_box()
        # send quantity to the box
        amount_box.send_keys(str(x))
        # add the quantity that we buy from the product to variable  in order to make sure that we buy the right amount
        self.quantity += int(x)
        # add also to list in order to make sure that every product got its exactly quantity
        self.quantity_list.append(int(x))

    def color_from_excel(self):
        # get all the colors elements that the product can have
        colors = self.item.all_colors()
        # create list that get the colors names which available to this product
        text_colors = []
        for y in colors:
            text_colors.append(y.get_attribute("title"))
        # get the color of the product from the excel
        color = self.details_from_excel.colors()
        # run on the colors of the product
        for i in range(len(colors)):
            # if the color from the excel is finding here choose it
            if color == text_colors[i]:
                self.item.color_items.append(color)
                colors[i].click()
                break
        # if the color from the excel not found choose random color
        else:
            # choose random number between the number of the colors
            x = randint(0, len(colors) - 1)
            # choose the random color
            self.item.color_items.append(colors[x].get_attribute("title"))
            # click on the random color
            colors[x].click()

    def click_on_add_to_cart(self):
        # click on add to cart button
        self.item.click_add_to_cart()

    def return_to_home_page(self):
        # move to the main page
        self.item.return_to_home_page()

    def setUp(self):
        # define the selenium object
        service = Service(r"C:\selen\chromedriver.exe")
        self.driver = webdriver.Chrome(service=service)
        self.driver.implicitly_wait(3)
        self.wait = WebDriverWait(self.driver, 10)
        # open the AOS web in maximize window
        self.driver.get("https://www.advantageonlineshopping.com/#/")
        self.driver.maximize_window()
        # define objects for the tests
        self.main_aos_page = AOS_Main_Page(self.driver)
        self.product_page = Product_Page(self.driver)
        self.item = Item_Page(self.driver)
        self.quantity, self.quantity_list = 0, []
        self.cart_panel = Cart_Panel(self.driver)
        self.cart_page = Cart_Page(self.driver)
        self.my_order_page = My_Orders_Page(self.driver)
        # open the excel file
        self.workbook = load_workbook(filename="AOS.xlsx")
        self.sheet = self.workbook.active

    def tearDown(self):
        # save the changes on the excel file at the end of each test
        self.workbook.save("AOS.xlsx")
        # close the web
        self.driver.close()

    def add_product(self, n=1):
        # function that add products to the cart
        for i in range(n):
            # get the category from the excel and click on it
            self.category_from_excel()
            # get the product from the category and click on it
            self.product_from_excel()
            # check if the product is not sold out
            if not self.item.sold_out_item():
                # get number of items from the product between 1 to 5 from the excel
                self.quantity_1to5()
                # get color to the product,
                # if not exist choose random color between the colors that the specific product can have
                self.color_from_excel()
                # click on add to cart
                self.click_on_add_to_cart()
                # return to the home page after the product added to the cart
                self.return_to_home_page()

    def test_exact_amount_1(self):
        # define object of the excel file and send the test number in order to get the specific details for the test
        self.details_from_excel = Details_From_Excel(1)
        # fill x in the excel file (if the text will fail in the running or has a bug)
        self.sheet['C28'] = "X"
        # add the amount of products from the excel file to cart
        self.add_product(self.details_from_excel.products_amount)
        # compare between the number of items which appear after account added the first product
        # and the number of items at the moment the account choose
        self.assertEqual(int(self.main_aos_page.number_on_the_cart_icon()), self.quantity)
        # if test passed fill V in the excel file
        self.sheet['C28'] = "V"

    def test_correct_products_2(self):
        # define object of the excel file and send the test number in order to get the specific details for the test
        self.details_from_excel = Details_From_Excel(2)
        # fill x in the excel file (if the text will fail in the running or has a bug)
        self.sheet['D28'] = 'X'
        # add the products
        self.add_product(self.details_from_excel.products_amount)
        # open the cart panel with action chains, without click the cart icon
        self.product_page.move_mouse_to_cart_icon()
        # call to function which returns the colors of the products as it shows in the panel cart
        colorsFromPanel = self.cart_panel.colors_from_panel()
        # call to function which returns the names of the products as it shows in the panel cart
        namesFromPanel = self.cart_panel.names_from_panel()
        # call to function which returns the quantities of the products as it shows in the panel cart
        quantity_from_panel_cart = self.cart_panel.products_quantity_from_panel()
        # compare the sum of the items in the panel cart with the real quantity by the purchase
        self.assertEqual(self.quantity, quantity_from_panel_cart)
        # compare the colors of the items in the panel cart with the colors of the items by the purchase
        self.assertListEqual(self.item.color_items, colorsFromPanel)
        # the name in the panel cart sometimes shorter so for each name from the panel cart
        # the loop checks if the name(that may be shorter) is in the original full name
        # only if all the names / short names exist in the full name the test pass
        for i in range(len(self.item.name_items)):
            if namesFromPanel[i] not in self.item.name_items[i]:
                self.assertTrue(False)
                break
        else:
            self.assertTrue(True)
        # check if the sum of the prices from the panel equal to the total price from the panel
        # if equal the function return True, else the function return False
        self.assertTrue(self.cart_panel.prices_from_panel())
        # if test passed fill V in the excel file
        self.sheet['D28'] = 'V'


    def test_the_remove_3(self):
        # define object of the excel file and send the test number in order to get the specific details for the test
        self.details_from_excel = Details_From_Excel(3)
        # fill x in the excel file (if the text will fail in the running or has a bug)
        self.sheet['E28'] = 'X'
        self.add_product(self.details_from_excel.products_amount)
        # move the mouse to the cart panel icon and wait until it open
        self.product_page.move_mouse_to_cart_icon()
        # call function which remove random product by click on x in cart panel
        self.cart_panel.remove_random_product_by_cart_panel()
        # take the amount of products in the panel cart after the removing
        products_from_the_panel = len(self.cart_panel.names_from_panel())
        # decrease by 1 because 1 remove
        all_items_include_removes = len(self.item.name_items) - 1
        # check if the amount of products after the remove of 1 product
        # equal to the amount of all the products before the removing minus 1
        self.assertEqual(products_from_the_panel, all_items_include_removes)
        # if test passed fill V in the excel file
        self.sheet['E28'] = 'V'

    def test_move_to_cart_page_4(self):
        # define object of the excel file and send the test number in order to get the specific details for the test
        self.details_from_excel = Details_From_Excel(4)
        # fill x in the excel file (if the text will fail in the running or has a bug)
        self.sheet['F28'] = 'X'
        self.add_product(self.details_from_excel.products_amount)
        # click on the cart icon in order to move to the cart page
        self.main_aos_page.click_cart_icon()
        # check if the headline of the cart page appears
        self.assertTrue(self.cart_page.shopping_cart_appears())
        # if test passed fill V in the excel file
        self.sheet['F28'] = 'V'

    def test_correct_prices_5(self):
        # define object of the excel file and send the test number in order to get the specific details for the test
        self.details_from_excel = Details_From_Excel(5)
        # fill x in the excel file (if the text will fail in the running or has a bug)
        self.sheet['G28'] = 'X'
        self.add_product(self.details_from_excel.products_amount)
        # moving to the cart page
        self.main_aos_page.click_cart_icon()
        # take the total price
        total = self.cart_page.get_price()
        # printing each item with the quantities amount the account bought and the price per unit
        for i in range(len(self.item.name_items)):
            print(f'{self.item.name_items[i]}, {self.quantity_list[i]} quantities, cost per unit: {self.item.price_item[i]}')
        # under the details about the products print the total price
        print('total of the purchase is: ', total)
        total_by_calculating = 0
        # the loop calculate (price per unit * quantities) for all the products
        for i in range(len(self.item.name_items)):
            total_by_calculating += self.quantity_list[i] * self.item.price_item[i]
        # check if the price that show in the cart page is the exactly price
        self.assertEqual(total, round(total_by_calculating, 2))
        # if test passed fill V in the excel file
        self.sheet['G28'] = 'V'

    def test_edit_from_cart_page_6(self):
        # define object of the excel file and send the test number in order to get the specific details for the test
        self.details_from_excel = Details_From_Excel(6)
        # fill x in the excel file (if the text will fail in the running or has a bug)
        self.sheet['H28'] = 'X'
        self.add_product(self.details_from_excel.products_amount)
        # moving to the cart page
        self.main_aos_page.click_cart_icon()
        # function wait till the hidden edit button is visible
        self.cart_page.wait_the_edit_buttons()
        # amount of the items per product in list before the edit
        quantities_before_edit = self.cart_page.quantity_of_products_in_cart_page()
        # add 2 quantities for each product
        self.cart_page.add_2_quantities_each_product()
        # amount of the items per product in list after the edit
        quantities_after_edit = self.cart_page.quantity_of_products_in_cart_page()
        # the loop check for each product if the amount after the adding is greater by 2
        for i in range(len(quantities_after_edit)):
            if quantities_after_edit[i] != quantities_before_edit[i] + 2:
                self.assertTrue(False)
                break
        else:
            self.assertTrue(True)
            # if test passed fill V in the excel file
            self.sheet['H28'] = 'V'

    def test_back_option_7(self):
        # define object of the excel file and send the test number in order to get the specific details for the test
        self.details_from_excel = Details_From_Excel(7)
        # fill x in the excel file (if the text will fail in the running or has a bug)
        self.sheet['I28'] = 'X'
        # enter to tablet page
        self.main_aos_page.click_tablet_category()
        # choose random tablet from the options and move to it page
        self.product_from_excel()
        # go back
        self.driver.back()
        # check if the url of current page is the url of the tablets page
        self.assertEqual(self.driver.current_url, 'https://www.advantageonlineshopping.com/#/category/Tablets/3')
        # another back
        self.driver.back()
        # check if the url of current page is the url of the main page
        self.assertEqual(self.driver.current_url, 'https://www.advantageonlineshopping.com/#/')
        # if test passed fill V in the excel file
        self.sheet['I28'] = ' V'

    # username = change everytime, password = Liav10, email liav@liav.com
    # safepay liavb20 Liavb20
    # need to chang username every use
    def test_create_account_pay_safepay_check_the_order_8(self):
        # define object of the excel file and send the test number in order to get the specific details for the test
        self.details_from_excel = Details_From_Excel(8)
        # fill x in the excel file (if the text will fail in the running or has a bug)
        self.sheet['J28'] = 'X'
        self.add_product(self.details_from_excel.products_amount)
        # move to cart page
        self.main_aos_page.click_cart_icon()
        # click on check out button
        self.cart_page.click_checkout_button()
        # move to registration
        self.cart_page.click_registration_button()
        self.registration_page = Registration_Page(self.driver)
        # send username that we have to change every run in the excel and fill all the details for the registration
        # finish the order and returns the order number
        order_id = self.registration_page.fill_details_and_finish_order()
        # move to my orders page
        self.main_aos_page.go_to_my_orders()
        # because its new account is the only order that exist in the orders page
        page_orderid = self.my_order_page.get_orderid()
        # check if order number at the buying moment equal to the order number in the page of "my orders"
        self.assertEqual(page_orderid, order_id)
        self.main_aos_page.click_cart_icon()
        # make sure the cart is empty
        self.assertEqual(self.cart_panel.products_quantity_from_panel(), 0)
        # if test passed fill V in the excel file
        self.sheet['J28'] = 'V'

    # default username 'liav10' password 'Liav10'
    def test_login_credit_card_order_exist_9(self):
        # define object of the excel file and send the test number in order to get the specific details for the test
        self.details_from_excel = Details_From_Excel(9)
        # fill x in the excel file (if the text will fail in the running or has a bug
        self.sheet['K28'] = 'X'
        self.add_product(self.details_from_excel.products_amount)
        # move to cart page
        self.main_aos_page.click_cart_icon()
        # click on check out button
        self.cart_page.click_checkout_button()
        # fill default login details (you can fill in the excel another username and password) and make the login
        self.cart_page.fill_login_details_and_click_login_button()
        # press the continue button, make sure the account pay by credit card and finish the order
        # return the order number
        order_id = self.cart_page.continue_to_finish_order()
        # move to my orders page
        self.main_aos_page.go_to_my_orders()
        # call to function that returns list of order id
        order_id_from_list = self.my_order_page.get_list_orderid()
        # check if the order number exist in the list of the orders in my orders page
        self.assertIn(order_id, order_id_from_list)
        # check if the cart is empty after the account finish the order
        self.main_aos_page.click_cart_icon()
        self.assertEqual(0, self.cart_panel.products_quantity_from_panel())
        # if test passed fill V in the excel file
        self.sheet['K28'] = 'V'

    def test_login_logout_10(self):
        # define object of the excel file and send the test number in order to get the specific details for the test
        self.details_from_excel = Details_From_Excel(10)
        # fill x in the excel file (if the text will fail in the running or has a bug
        self.sheet['L28'] = 'X'
        # make sure the whole web is opened
        self.main_aos_page.wait_for_the_web_and_click_account_icon()
        # fill the login details by default, there is option to send username and password
        self.main_aos_page.fill_username_password_and_login()
        # call to function which check if the login works and return True or False
        self.assertTrue(self.main_aos_page.check_if_login())
        # wait the web is opened and than click the account icon
        self.main_aos_page.wait_for_the_web_and_click_account_icon()
        # click the sign out button
        self.main_aos_page.logout_click()
        # make sure that the sing out worked
        self.assertTrue(self.main_aos_page.check_if_logout())
        # if test passed fill V in the excel file
        self.sheet['L28'] = 'V'
