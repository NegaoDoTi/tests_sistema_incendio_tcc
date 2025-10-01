from utils.waits import Waits
from time import sleep
from selenium.webdriver.remote.webdriver import WebDriver
from json import load
from datetime import datetime
import pytest

@pytest.mark.parametrize("dados_teste", ["users.json"], indirect=True)

def test_register(driver:WebDriver, waits:Waits, dados_teste) -> None:
    """Teste de registro de usuarios CT2
 
    Args:
        driver (WebDriver): Driver Selenium
        waits (Waits): Waits Selenium
    
    """
    
    duracoes = []
    
    for nome, email, senha, esperado in dados_teste:
        inicio = datetime.now()
    
        user_name = nome
        
        user_email = email
        
        user_password = senha
        
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
        
        print(name_logged, user_name, name_check)
        
        print(nome, email, senha, esperado)
        
        if esperado:
            
            
            assert name_check == esperado
            assert driver.current_url == "http://medidasincendio.test/dashboard"
            
            sair = waits.wait_presence(
                {"css_selector" : 'a[href="http://medidasincendio.test/logout"]'},
                time=3
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