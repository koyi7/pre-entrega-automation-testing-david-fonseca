from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from utils.logger import get_logger

logger = get_logger(__name__)


class CheckoutPage:
    """Page Object para el flujo de checkout de Sauce Demo."""

    def __init__(self, driver):
        self.driver = driver

        self.checkout_button = (By.ID, "checkout")
        self.first_name = (By.ID, "first-name")
        self.last_name = (By.ID, "last-name")
        self.postal_code = (By.ID, "postal-code")
        self.continue_button = (By.ID, "continue")
        self.finish_button = (By.ID, "finish")
        self.complete_header = (By.CLASS_NAME, "complete-header")
        self.summary_total = (By.CLASS_NAME, "summary_total_label")
        self.title = (By.CLASS_NAME, "title")

    def click_checkout(self):
        wait = WebDriverWait(self.driver, 10)
        wait.until(EC.element_to_be_clickable(self.checkout_button)).click()
        logger.info("Se inició el checkout")

    def fill_checkout_info(self, nombre, apellido, codigo_postal):
        wait = WebDriverWait(self.driver, 10)
        wait.until(EC.visibility_of_element_located(self.first_name)).send_keys(nombre)
        self.driver.find_element(*self.last_name).send_keys(apellido)
        self.driver.find_element(*self.postal_code).send_keys(codigo_postal)
        wait.until(EC.element_to_be_clickable(self.continue_button)).click()
        logger.info("Se completaron los datos de checkout")

    def get_summary_total(self):
        wait = WebDriverWait(self.driver, 10)
        return wait.until(EC.visibility_of_element_located(self.summary_total)).text

    def finish_order(self):
        wait = WebDriverWait(self.driver, 10)
        wait.until(EC.element_to_be_clickable(self.finish_button)).click()
        logger.info("Se finalizó la orden")

    def get_success_message(self):
        wait = WebDriverWait(self.driver, 10)
        return wait.until(EC.visibility_of_element_located(self.complete_header)).text
