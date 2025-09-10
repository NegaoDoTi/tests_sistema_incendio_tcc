from utils.waits import Waits
from time import sleep
from selenium.webdriver.remote.webdriver import WebDriver
import pytest
from random import choice
from string import ascii_lowercase, digits


def random_string(size=8):
    return "".join(choice(ascii_lowercase) for i in range(size))

def random_email():
    return random_string() + "@email.com"

@pytest.mark.parametrize("user_email,user_password", [
    (random_email(), random_string(15))
])

def test_login_nao_cadastrado(
    driver:WebDriver, 
    waits:Waits, 
    user_email,
    user_password,
    user_name:str = "teste fulano", 
) -> None:
    
    """Testa se o login esta funcionando corretamente CT 1

    Args:
        driver (WebDriver): Driver selenium
        waits (Waits): Waits selenium
        user_name (str, optional): . Defaults to "teste fulano".
        user_email (str, optional): . Defaults to "teste@email.com".
        user_password (str, optional): . Defaults to "teste123456789@teste".
    """
    
    url = "http://medidasincendio.test/login"
    
    driver.get(url)
    
    email_input = waits.wait_visibility({"css_selector" : 'input[id="email"]'})
    
    email_input.send_keys(user_email)
    
    password_input = waits.wait_visibility({"css_selector" : 'input#password'})
    
    password_input.send_keys(user_password)
    
    button_login = waits.wait_visibility({"css_selector" : 'button[type="submit"]'})
    
    button_login.click()
    
    sleep(1)
    
    message_login = waits.wait_visibility(
        {
            "css_selector" : 'ul[class="text-sm text-red-600 space-y-1 mt-2"] li'
        },
        time=2
    )
    
    assert message_login.text == "auth.failed"
