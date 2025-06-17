import pytest
from pages.login_page import LoginPage

@pytest.mark.parametrize(
    "user,pwd,exp_type,exp_msg_snippet,exp_path",
    [
        # happy-path
        ("tomsmith", "SuperSecretPassword!", "success", "You logged into a secure area!", "/secure"),
        # invalid username
        ("baduser",  "SuperSecretPassword!", "error",   "Your username is invalid!",      "/login"),
        # invalid password
        ("tomsmith", "BadPassword!",         "error",   "Your password is invalid!",      "/login"),
        # missing both fields
        ("",         "",                     "error",   "Your username is invalid!",      "/login"),
    ],
)
def test_login_variants(driver, user, pwd, exp_type, exp_msg_snippet, exp_path):
    page = LoginPage(driver)
    page.open()
    page.login(user, pwd)

    assert exp_path in driver.current_url
    assert page.banner_type() == exp_type
    assert page.banner_text().startswith(exp_msg_snippet)

