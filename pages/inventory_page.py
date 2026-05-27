from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class InventoryPage:
    def __init__(self, driver):
        self.driver = driver

        self.title = (By.CLASS_NAME, "title")
        self.product_names = (By.CLASS_NAME, "inventory_item_name")
        self.sort_dropdown = (By.CLASS_NAME, "product_sort_container")
        self.cart_link = (By.CLASS_NAME, "shopping_cart_link")
        self.cart_badge = (By.CLASS_NAME, "shopping_cart_badge")

    def get_title(self):
        wait = WebDriverWait(self.driver, 10)
        return wait.until(EC.visibility_of_element_located(self.title)).text

    def get_product_names(self):
        wait = WebDriverWait(self.driver, 10)
        wait.until(EC.visibility_of_all_elements_located(self.product_names))
        elementos = self.driver.find_elements(*self.product_names)
        return [elemento.text for elemento in elementos]

    def product_exists(self, nombre_producto):
        nombres = self.get_product_names()
        return any(nombre_producto in nombre for nombre in nombres)

    def sort_by(self, valor_filtro):
        wait = WebDriverWait(self.driver, 10)
        dropdown = wait.until(EC.visibility_of_element_located(self.sort_dropdown))
        Select(dropdown).select_by_value(valor_filtro)

    def get_first_product_name(self):
        nombres = self.get_product_names()
        return nombres[0] if nombres else ""

    def add_product_to_cart(self, product_slug):
        locator = (By.CSS_SELECTOR, f"[data-test='add-to-cart-{product_slug}']")
        wait = WebDriverWait(self.driver, 10)
        boton = wait.until(EC.element_to_be_clickable(locator))
        boton.click()

    def get_cart_badge_count(self):
        badges = self.driver.find_elements(*self.cart_badge)
        if not badges:
            return "0"
        return badges[0].text

    def go_to_cart(self):
        wait = WebDriverWait(self.driver, 10)
        wait.until(EC.element_to_be_clickable(self.cart_link)).click()
