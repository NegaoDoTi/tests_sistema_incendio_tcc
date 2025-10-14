from utils.waits import Waits
from time import sleep
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import Select
from random import choices, randint
from string import ascii_lowercase
from datetime import datetime
from pathlib import Path
import pytest

@pytest.mark.parametrize("dados_teste", ["parameters\\invalid_local.json"], indirect=True)
def test_cadastrar_local_fail(
    driver:WebDriver, 
    waits:Waits,
    dados_teste,
    user_email:str = "teste@email.com" , 
    user_password:str = "teste123456789@teste"
) -> None:
    
    """Testa a funcionalidade cadastramento de locais CT3

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
    for index, dados in enumerate(dados_teste):
        
        inicio = datetime.now()
        
        index = index + 1
        
        nome, tipo, capacidade, foto_local, foto_mapa = dados
        
        print(index)
        
        sleep(3)
        
        driver.get('http://medidasincendio.test/locais/cadastrar')

        local_name_input = waits.wait_visibility({'css_selector' : 'input[id="nome"]'})
        
        local_name_input.send_keys(nome)
        
        sleep(0.5)
        
        select_tipo_local = waits.wait_visibility({"css_selector" : 'select[name="tipo_id"]'})
        
        select_tipo_local = Select(select_tipo_local)
        
        if tipo == "":
            pass
        else:
            select_tipo_local.select_by_visible_text(f"{tipo}")
        
        sleep(0.5)
        
        if capacidade != "":
            capacity_input = waits.wait_visibility({'css_selector' : 'input[name="capacidade"]'})
            
            capacity_input.send_keys(capacidade)
            
            sleep(0.5)
        
        
        if foto_local != "":
            photo_button = waits.wait_visibility({"css_selector" : '''button[onclick="openOverlay('overlayAddImagem')"]'''})
        
            photo_button.click()
            sleep(0.5)
            
            local_image_path = Path(Path(__file__).parent.parent.parent, "images", f'{foto_local}')
            
            add_photo = waits.wait_presence({"css_selector" : 'input[id="nova_foto"]'})
            
            add_photo.send_keys(f"{local_image_path}")
            
            sleep(0.5)
        
            confirm_img_button = waits.wait_visibility({"css_selector" : '''div[class="overlay active"] button[onclick="closeOverlay('overlayAddImagem')"]'''})
            
            confirm_img_button.click()
        
        if foto_mapa != "":
            map_image_path = Path(Path(__file__).parent.parent.parent, "images", f'{foto_mapa}')
            
            image_map_input = waits.wait_visibility({"css_selector" : 'input[id="mapa"]'})
            
            image_map_input.send_keys(f"{map_image_path}")
            
            sleep(0.5)
            
        
        cadastrar_button =  waits.wait_visibility({"css_selector" : 'div[class="mt-2"] button[type="submit"]'})
        
        cadastrar_button.click()
        
        sleep(0.5)
        
        if tipo == "" and capacidade != "":
            is_invalid = driver.execute_script('return document.getElementById("tipo_id").checkValidity();')

            assert not is_invalid
            
        if foto_mapa == "" and foto_local != "":
            message_mapa = waits.wait_visibility(
                {
                    "css_selector" : "div.p-4.sm\:p-8.bg-white.shadow.sm\:rounded-lg > form > div > section > div:nth-child(4) > label > span"
                },
                time=5
            )
            
            assert "Mapa do local é obrigatório para prosseguir" in message_mapa.text 
        
        if foto_mapa != "" and foto_local == "" and nome != "":
            
            message_local = waits.wait_visibility(
                {
                    "css_selector" : "div.p-4.sm\:p-8.bg-white.shadow.sm\:rounded-lg > form > div > aside > span"
                },
                time=3
            )
        
            assert "Escolha uma foto existente ou cadastre uma nova para prosseguir" in message_local.text
            
        
        if nome == "" and tipo != "":
            is_invalid = driver.execute_script("return arguments[0].checkValidity();", local_name_input)

            assert not is_invalid
            
        if capacidade == "" and tipo != "":
            
            message_capacidae = waits.wait_visibility(
                {
                    "css_selector" : "label[for='capacidade'].block.font-medium.text-sm.text-gray-700"
                },
                time=5
            )
            
            assert "A capacidade deve ser informada para esse tipo de local" in message_capacidae.text
            
        
        if nome == "" and tipo == "" and capacidade == "" and foto_local  == "" and foto_mapa == "":
            is_invalid = driver.execute_script("return arguments[0].checkValidity();", local_name_input)

            assert not is_invalid
            
        if nome == "" and tipo == "" and capacidade == "" and foto_local  == "" and foto_mapa != "":
            is_invalid = driver.execute_script("return arguments[0].checkValidity();", local_name_input)

            assert not is_invalid

        fim = datetime.now()
        
        check = fim - inicio
        
        duracoes.append(f"{check.seconds}:{check.microseconds}")
    
    print(duracoes)