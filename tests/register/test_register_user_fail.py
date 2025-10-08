from utils.waits import Waits
from time import sleep
from selenium.webdriver.remote.webdriver import WebDriver
from datetime import datetime
import pytest

@pytest.mark.parametrize("dados_teste", ["parameters\\valid_users.json"], indirect=True)

def test_register(driver:WebDriver, waits:Waits, dados_teste) -> None:
    """Teste de registro de usuarios CT2
 
    Args:
        driver (WebDriver): Driver Selenium
        waits (Waits): Waits Selenium
    
    """
    
    duracoes = []
    
    for index, dados in enumerate(dados_teste):
        index = index + 1
        
        print(f"{index}")
        
        user_name, user_email, user_password = dados
        
        inicio = datetime.now()
        
        url = "http://medidasincendio.test/register"
        
        driver.get(url)
        
        name_input = waits.wait_visibility({"css_selector" : 'input[id="name"]'}) 
        name_input.click()
        
        name_input.send_keys(user_name)
        
        email_input = waits.wait_visibility({"css_selector" : 'input#email'})
        email_input.click()
        
        email_input.send_keys(user_email)
            
        password_input = waits.wait_visibility({"css_selector" : 'input#password'})
        password_input.click()
        
        password_input.send_keys(user_password)
        
        password_c_input = waits.wait_visibility({"css_selector" : 'input#password_confirmation'})
        password_c_input.click()
        
        password_c_input.send_keys(user_password)
        
        button_register = waits.wait_visibility({"css_selector" : 'button[type="submit"]'})
        
        button_register.click()
        
        sleep(3)
        
        email_message = waits.wait_visibility(
            {
                "css_selector" : 'ul.text-sm.text-red-600.space-y-1.mt-2 li'
            }
        ).text
            
        assert email_message == "validation.unique"
        
        fim = datetime.now()
        
        check = fim - inicio
        
        duracoes.append(f"{check.seconds}:{check.microseconds}")
        
    print(duracoes)