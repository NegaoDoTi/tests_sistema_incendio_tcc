from utils.waits import Waits
from time import sleep
from selenium.webdriver.remote.webdriver import WebDriver
from datetime import datetime
import pytest

@pytest.mark.parametrize("dados_teste", ["parameters\\valid_users.json"], indirect=True)
def test_delete_acount(driver:WebDriver, waits:Waits, dados_teste) -> None:
    """Teste de deletar conta de usuario CT4

    Args:
        driver (WebDriver): Driver Selenium
        waits (Waits): Waits Selenium
    """
    duracoes = []
    for index, dados in enumerate(dados_teste):
        inicio = datetime.now()
        
        index = index + 1
        
        print(index)
        
        user_name, user_email, user_password = dados
        
        url = "http://medidasincendio.test/login"
        
        driver.get(url)
        
        email_input = waits.wait_visibility({"css_selector" : 'input#email'})
        email_input.click()
        
        email_input.send_keys(user_email)
            
        password_input = waits.wait_visibility({"css_selector" : 'input#password'})
        password_input.click()
        
        password_input.send_keys(user_password)
        
        button_register = waits.wait_visibility({"css_selector" : 'button[type="submit"]'})
        
        button_register.click()
        
        sleep(5)
        
        try:
        
            driver.get("http://medidasincendio.test/profile")
            
            waits.wait_visibility(
                {
                    "css_selector" : 'body > div > main > div > div > div:nth-child(3) > div > section > button'
                }
            ).click()
            
            input_password = waits.wait_visibility(
                {
                    "css_selector" : 'form[action="http://medidasincendio.test/profile"] input[id="password"]'
                }
            )
            
            driver.execute_script(
                f'arguments[0].value = `{user_password}`', input_password
            )
            
            
            waits.wait_clickable(
                {
                    "css_selector" : 'form[action="http://medidasincendio.test/profile"] div[class="mt-6 flex justify-end"] button:nth-child(2)'
                }
            ).click()
            
            sleep(3)
        
            assert driver.current_url == "http://medidasincendio.test/"
 
        except:
            pass
        
        fim = datetime.now()
        
        check = fim - inicio
        
        duracoes.append(f"{check.seconds}:{check.microseconds}")
    
    print(duracoes)
        