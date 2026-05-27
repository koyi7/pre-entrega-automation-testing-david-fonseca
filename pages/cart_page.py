from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class CartPage:
    def __init__(self, driver):
        self.driver = driver

        self.title = (By.CLASS_NAME, "title")
        self.cart_item_names = (By.CLASS_NAME, "inventory_item_name")

    def get_title(self):
        wait = WebDriverWait(self.driver, 10)
        return wait.until(EC.visibility_of_element_located(self.title)).text

    def get_cart_product_names(self):
        wait = WebDriverWait(self.driver, 10)
        wait.until(EC.visibility_of_element_located(self.title))
        elementos = self.driver.find_elements(*self.cart_item_names)
        return [elemento.text for elemento in elementos]

    def product_in_cart(self, nombre_producto):
        return nombre_producto in self.get_cart_product_names()

    def remove_product(self, product_slug):
        locator = (By.CSS_SELECTOR, f"[data-test='remove-{product_slug}']")
        wait = WebDriverWait(self.driver, 10)
        boton = wait.until(EC.element_to_be_clickable(locator))
        boton.click()

    def is_cart_empty(self):
        return len(self.get_cart_product_names()) == 0
