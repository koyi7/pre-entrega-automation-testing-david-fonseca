from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class LoginPage:
    def __init__(self, driver, base_url):
        self.driver = driver
        self.url = base_url

        self.username_field = (By.ID, "user-name")
        self.password_field = (By.ID, "password")
        self.login_button = (By.ID, "login-button")
        self.title_products = (By.CLASS_NAME, "title")
        self.error_message = (By.CSS_SELECTOR, "[data-test='error']")

    def open(self):
        self.driver.get(self.url)

    def login(self, user, password):
        wait = WebDriverWait(self.driver, 10)

        user_input = wait.until(EC.visibility_of_element_located(self.username_field))
        user_input.clear()
        user_input.send_keys(user)

        password_input = wait.until(EC.visibility_of_element_located(self.password_field))
        password_input.clear()
        password_input.send_keys(password)

        wait.until(EC.element_to_be_clickable(self.login_button)).click()

    def get_title(self):
        wait = WebDriverWait(self.driver, 10)
        titulo = wait.until(EC.visibility_of_element_located(self.title_products))
        return titulo.text

    def get_error_message(self):
        wait = WebDriverWait(self.driver, 10)
        mensaje = wait.until(EC.visibility_of_element_located(self.error_message))
        return mensaje.text
