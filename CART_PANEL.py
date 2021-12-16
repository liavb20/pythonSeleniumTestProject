from selenium.webdriver.common.by import By
from random import randint


class Cart_Panel:
    def __init__(self, driver):
        self.driver = driver
        self.colors = []
        self.names = []
        self.prices = []

    def colors_from_panel(self):
        # catch the object of the element
        colors_obj = self.driver.find_elements(By.CSS_SELECTOR, 'span[class="ng-binding"]')
        # insert the colors into a list
        for i in colors_obj:
            self.colors.append(i.text)
        # sort the colorsFromPanel to be ordered from the begin to end
        temp = [self.colors[len(self.colors) - 1 - i] for i in range(len(self.colors))]
        return temp

    def names_from_panel(self):
        # catch the elements of the product names from the cart panel
        names_obj = self.driver.find_elements(By.CSS_SELECTOR, 'h3[class="ng-binding"]')
        # sort the names from the begin to the end and switch the elements to text
        for i in range(len(names_obj), 0, -1):
            self.names.append(names_obj[i-1].text)
        # part of the names that appear in the cart panel are shorter and have ending of 3 points (...)
        # the loop cut that points
        for i in range(len(self.names)):
            self.names[i] = self.names[i][:-3]
        return self.names

    def products_quantity_from_panel(self):
        # use try because the if the element not found i want the function to return 0
        try:
            # catch the colors and quantity of the products in the cart panel
            quantity_list_temp = self.driver.find_elements(By.CSS_SELECTOR, "label[class='ng-binding']")
            # save only the elements of the quantity
            quantity_list = [quantity_list_temp[i] for i in range(0, len(quantity_list_temp), 2)]
            # make the list has the value and not the element
            quantity_list = [i.text for i in quantity_list]
            # the text is for instance 'QTY: 5' and the program need only the number so the loop cut the rest
            number_quantity_list = [i[5:] for i in quantity_list]
            # change the list from string to int
            int_list_quantity = [int(i) for i in number_quantity_list]
            # return the sum of the list
            total = sum(int_list_quantity)
            return total
        except:
            return 0

    def prices_from_panel(self):
        # catch the price of each product in the cart panel
        temp = self.driver.find_elements(By.CSS_SELECTOR, 'p[class="price roboto-regular ng-binding"]')
        # change the elements to text
        temp = [i.text for i in temp]
        temp2 = []
        # for each price, cut the $ mark at the first character of the string
        for i in range(len(temp)):
            temp[i] = temp[i][1:]
        # move the temp list into temp2 and order the list from the begin to the end
        for i in range(len(temp), 0, -1):
            temp2.append(temp[i-1])
        # check if there is comma in each price, if there is so cut it, than change the type fromm string to float
        for i in range(len(temp2)):
            if ',' in temp2[i]:
                temp2[i] = temp2[i].replace(',', '')
            temp2[i] = float(temp2[i])
        # move temp2 into self.prices
        self.prices = [i for i in temp2]
        # catch the text of the element of the total price in the panel cart
        total = self.driver.find_element(By.CSS_SELECTOR, '[class="roboto-medium cart-total ng-binding"]').text
        # if there is comma in the total price so cut it
        if ',' in total:
            total = total.replace(',', '')
        # cut the $ mark
        total = total[1:]
        # change the string to float
        total = float(total)
        # return true if the prices equal else false
        return round(sum(self.prices), 2) == round(total, 2)

    def remove_random_product_by_cart_panel(self):
        # catch the elements of the remove buttons
        buttons = self.driver.find_elements(By.CSS_SELECTOR, '[class="removeProduct iconCss iconX"]')
        # rand number between the products amount
        x = randint(0, len(buttons) - 1)
        # remove random product
        remove_product = buttons[x]
        remove_product.click()

