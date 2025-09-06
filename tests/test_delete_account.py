from utils.waits import Waits
from time import sleep
from selenium.webdriver.remote.webdriver import WebDriver
from random import choices, choice, randint
from string import ascii_lowercase, digits


def test_delete_acount(driver:WebDriver, waits:Waits) -> None:
    """Teste de registro de usuarios

    Args:
        driver (WebDriver): Driver Selenium
        waits (Waits): Waits Selenium
    """
    
    user_name = "".join(choices(ascii_lowercase, k=randint(8, 15)))
    
    emails_domains = ["gmail.com", "hotmail.com", "yahoo.com.br", "outlook.com", "example.com"]
    
    domain = choice(emails_domains)
    
    user_email = f"{user_name}@{domain}"
    
    user_password = "".join(choice(ascii_lowercase + digits) for i in range(15))
    
    print(user_password)
    
    url = "http://medidasincendio.test/register"
    
    driver.get(url)
    
    name_input = waits.wait_visibility({"css_selector" : 'input[id="name"]'}) 
    
    name_input.send_keys(user_name)
    
    email_input = waits.wait_visibility({"css_selector" : 'input#email'})
    
    email_input.send_keys(user_email)
        
    password_input = waits.wait_visibility({"css_selector" : 'input#password'})
    
    password_input.send_keys(user_password)
    
    password_c_input = waits.wait_visibility({"css_selector" : 'input#password_confirmation'})
    
    password_c_input.send_keys(user_password)
    
    button_register = waits.wait_visibility({"css_selector" : 'button[type="submit"]'})
    
    button_register.click()
    
    sleep(5)
    
    name_logged = waits.wait_visibility(
        {
            "css_selector" : "div.hidden.sm\\:flex.sm\\:items-center.sm\\:ml-6 > div > div:nth-child(1) > button > div:nth-child(1)"
        }
    )
    
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