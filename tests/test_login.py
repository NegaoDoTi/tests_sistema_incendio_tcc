from utils.waits import Waits
from time import sleep
from selenium.webdriver.remote.webdriver import WebDriver
from datetime import datetime
import pytest

@pytest.mark.parametrize("dados_teste", ["users.json"], indirect=True)
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
    
    for nome, email, senha, esperado in dados_teste:
        inicio = datetime.now()
        
        user_name = nome
        
        user_email = email
        
        user_password = senha
        
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
        
        sleep(5)
        
        try:
            name_logged = waits.wait_visibility(
                {
                    "css_selector" : "div.hidden.sm\\:flex.sm\\:items-center.sm\\:ml-6 > div > div:nth-child(1) > button > div:nth-child(1)"
                }, time=3
            )
            
            name_logged = name_logged.text
            
        except:
            name_logged = None
        
        name_check = name_logged == user_name 
        
        print(nome, email, senha, esperado)
        
        if esperado:
            
            assert name_check == esperado
            assert driver.current_url == "http://medidasincendio.test/dashboard"
            
            sair = waits.wait_presence(
                {"css_selector" : 'a[href="http://medidasincendio.test/logout"]'}
            )

            driver.execute_script(
                "arguments[0].click()",
                sair
            )
            
        else:
             assert name_check == esperado
            
        fim = datetime.now()
        
        check = fim - inicio
        
        duracoes.append(check)
        
    print(duracoes)