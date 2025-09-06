from utils.waits import Waits
from time import sleep
from selenium.webdriver.remote.webdriver import WebDriver

def test_login(
    driver:WebDriver, 
    waits:Waits, 
    user_name:str = "teste fulano", 
    user_email:str = "teste@email.com" , 
    user_password:str = "teste123456789@teste"
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
    
    sleep(5)
    
    name_logged = waits.wait_visibility(
        {
            "css_selector" : "div.hidden.sm\\:flex.sm\\:items-center.sm\\:ml-6 > div > div:nth-child(1) > button > div:nth-child(1)"
        }
    )
    
    
    assert driver.current_url == "http://medidasincendio.test/dashboard"
    assert name_logged.text == user_name
