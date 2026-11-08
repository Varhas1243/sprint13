import time

from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from .models import CustomUser

PAUSE = 1

VALID_EMAIL = "test@gmail.com"
VALID_PASSWORD = "test12345"

INVALID_EMAIL = "wrong@gmail.com"
INVALID_PASSWORD = "wrongpassword"

LOGOUT_BUTTON = (By.XPATH, "//nav//button[text()='Вийти']")
LOGIN_LINK = (By.LINK_TEXT, "Увійти")
ERROR_MESSAGE = (By.XPATH, "//p[text()='Неправильний email або пароль']")


class LoginSeleniumTest(LiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.browser = webdriver.Chrome()
        cls.browser.maximize_window()
        cls.wait = WebDriverWait(cls.browser, 10)

    @classmethod
    def tearDownClass(cls):
        cls.browser.quit()
        super().tearDownClass()

    def setUp(self):
        CustomUser.objects.create_user(
            email=VALID_EMAIL,
            password=VALID_PASSWORD,
            first_name="Тест",
            last_name="Користувач",
            middle_name="Селеніум",
            role=0,
            is_active=True,
        )

    def pause(self):
        time.sleep(PAUSE)

    def login(self, email, password):
        self.browser.find_element(By.NAME, "email").send_keys(email)
        self.browser.find_element(By.NAME, "password").send_keys(password)
        self.pause()
        self.browser.find_element(By.CSS_SELECTOR, "form button[type='submit']").click()

    def test_login_with_valid_and_invalid_credentials(self):
        self.browser.get(self.live_server_url + "/")
        self.pause()

        self.browser.find_element(*LOGIN_LINK).click()
        self.wait.until(EC.url_contains("/login/"))
        self.pause()

        self.login(VALID_EMAIL, VALID_PASSWORD)

        logout_button = self.wait.until(EC.visibility_of_element_located(LOGOUT_BUTTON))
        self.assertIn("/books/", self.browser.current_url)
        self.assertFalse(self.browser.find_elements(*LOGIN_LINK))
        self.pause()

        logout_button.click()

        self.wait.until(EC.url_contains("/login/"))
        self.assertTrue(self.browser.find_element(*LOGIN_LINK).is_displayed())
        self.assertFalse(self.browser.find_elements(*LOGOUT_BUTTON))
        self.pause()

        self.login(INVALID_EMAIL, INVALID_PASSWORD)

        error = self.wait.until(EC.visibility_of_element_located(ERROR_MESSAGE))
        self.assertEqual(error.text, "Неправильний email або пароль")
        self.assertIn("/login/", self.browser.current_url)
        self.assertFalse(self.browser.find_elements(*LOGOUT_BUTTON))
        self.pause()
