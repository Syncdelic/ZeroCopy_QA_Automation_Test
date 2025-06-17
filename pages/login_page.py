# pages/login_page.py
from selenium.webdriver.common.by import By
from .base_page import BasePage

class LoginPage(BasePage):
    URL = "https://the-internet.herokuapp.com/login"

    USERNAME  = (By.ID, "username")
    PASSWORD  = (By.ID, "password")
    LOGIN_BTN = (By.CSS_SELECTOR, "button[type='submit']")
    FLASH     = (By.ID, "flash") # green/red banner

    def login(self, user: str, pwd: str):
        self._find(self.USERNAME).send_keys(user)
        self._find(self.PASSWORD).send_keys(pwd)
        self._find(self.LOGIN_BTN).click()

    def banner_text(self) -> str:
        return self._find(self.FLASH).text.strip().rstrip("×").strip()

    def banner_type(self) -> str:           # “success” or “error”
        cls = self._find(self.FLASH).get_attribute("class")
        return "success" if "success" in cls else "error"

