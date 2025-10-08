from utils.waits import Waits
from time import sleep
from selenium.webdriver.remote.webdriver import WebDriver
from datetime import datetime
import pytest

@pytest.mark.parametrize("dados_teste", ["parameters\\invalid_password_users.json"], indirect=True)
def test_login(
    driver:WebDriver, 
    waits:Waits,
    dados_teste
) -> None:
    
    """Testa se o login esta funcionando corretamente CT 1

    Args:
        driver (WebDriver): Driver selenium
        waits (Waits): Waits selenium
        user_name (str, optional): . Defaults to "teste fulano".
        user_email (str, optional): . Defaults to "teste@email.com".
        user_password (str, optional): . Defaults to "teste123456789@teste".
    """
    duracoes = []
    
    for index, dados in enumerate(dados_teste):
        inicio = datetime.now()
        
        index = index + 1
        
        print(f"{index}")
        
        user_email, user_password = dados
        
        url = "http://medidasincendio.test/login"
        
        driver.get(url)
        
        email_input = waits.wait_visibility({"css_selector" : 'input[id="email"]'}, time=3)
        email_input.click()
        
        email_input.send_keys(user_email)
        
        password_input = waits.wait_visibility({"css_selector" : 'input#password'}, time=3)
        password_input.click()
        
        password_input.send_keys(user_password)
        
        button_login = waits.wait_visibility({"css_selector" : 'button[type="submit"]'}, time=3)
        
        button_login.click()
        
        sleep(4)

        auth_message = waits.wait_visibility(
            {"css_selector" : 'ul[class="text-sm text-red-600 space-y-1 mt-2"] li'},
            time=3
        )
    
        auth_message = auth_message.text
        
        assert auth_message == "auth.failed"
            
        fim = datetime.now()
        
        check = fim - inicio
        
        duracoes.append(f"{check.seconds}:{check.microseconds}")
        
    print(duracoes)