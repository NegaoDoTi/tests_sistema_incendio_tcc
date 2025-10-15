from utils.waits import Waits
from time import sleep
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import Select
from datetime import datetime
import pytest

@pytest.mark.parametrize("dados_teste", ["parameters\\valid_extintores.json"], indirect=True)
def test_cadastrar_extintor(
    driver:WebDriver, 
    waits:Waits,
    dados_teste,
    user_email:str = "teste@email.com" , 
    user_password:str = "teste123456789@teste"
) -> None:
    
    """Testa de cadastrar extintor CT6

    Args:
        driver (WebDriver): Driver selenium
        waits (Waits): Waits selenium
        user_name (str, optional): . to "teste fulano".
        user_email (str, optional):   to "teste@email.com".
        user_password (str, optional): . to "teste123456789@teste".
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
    
    duracoes = []
    
    for i, dados in enumerate(dados_teste):
        inicio = datetime.now()
        
        i = i + 1
        
        selo, capacidade, validade, localizacao, tipo_extintor  = dados
        
        driver.get("http://medidasincendio.test/locais/74")
        
        sleep(1.5)
        
        cadastrar = waits.wait_clickable(
            {"css_selector" : 'h2:nth-child(7) >  a > button'},
            time=5
        )
        
        cadastrar.click()
        
        sele_input = waits.wait_visibility(
            {
                "css_selector" : 'input[name="selo"]'
            },
            time=3
        )
        
        sele_input.send_keys(selo)
        
        capacidade_input = waits.wait_visibility(
            {
                "css_selector" : 'input[name="capacidade"]'
            },
            time=3
        )
        
        capacidade_input.send_keys(capacidade)
        
        validade_input = waits.wait_visibility(
            {"css_selector" : 'input[id="validade"]'},
            time=3
        )
        
        validade_str = datetime.strptime(validade, "%Y-%m-%d")
        
        validade_str = validade_str.strftime("%d/%m/%Y")
        
        validade_input.send_keys(validade_str)
        
        if tipo_extintor == "Agua":
            input_tipo = waits.wait_clickable(
                {
                    "css_selector" : 'input[id="1"]'
                },
                time=3
            )
            
            input_tipo.click()
            
        if tipo_extintor == "Gás Carbônico":
            input_tipo = waits.wait_clickable(
                {
                    "css_selector" : 'input[id="2"]'
                },
                time=3
            )
            
            input_tipo.click()
            
        if tipo_extintor == "Pó Químico B/C":
            input_tipo = waits.wait_clickable(
                {
                    "css_selector" : 'input[id="3"]'
                },
                time=3
            )
            
            input_tipo.click()
            
        if tipo_extintor == "Espuma mecânica":
            input_tipo = waits.wait_clickable(
                {
                    "css_selector" : 'input[id="5"]'
                },
                time=3
            )
            
            input_tipo.click()
            
        if tipo_extintor == "Pó Químico A/B/C":
            input_tipo = waits.wait_clickable(
                {
                    "css_selector" : 'input[id="5"]'
                },
                time=3
            )
            
            input_tipo.click()
            
        waits.wait_clickable({"css_selector" : 'button[type="submit"]'}).click()
        
        sucess_msg = waits.wait_visibility(
            {
                "css_selector" : 'div.alert.alert-danger > ul > li'
            }
        )
        
        assert "validation.unique" == sucess_msg.text
        
        fim = datetime.now()
        
        check = fim - inicio
        
        duracoes.append(f"{check.seconds}:{check.microseconds}")
        
    print(duracoes)
    