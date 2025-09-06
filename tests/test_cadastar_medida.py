from utils.waits import Waits
from time import sleep
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import Select
from random import choices, randint
from string import ascii_lowercase
from pathlib import Path

def test_cadastrar_medida(
    driver:WebDriver, 
    waits:Waits, 
    user_email:str = "teste@email.com" , 
    user_password:str = "teste123456789@teste"
) -> None:
    
    """Testa cadastrar medida de incendio CT5

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
    
    driver.get('http://medidasincendio.test/locais/cadastrar')
    
    'form section button[type="submit"]'
    
    local_name = user_name = "".join(choices(ascii_lowercase, k=randint(8, 15)))
    
    local_name_input = waits.wait_visibility({'css_selector' : 'input[id="nome"]'})
    
    local_name_input.send_keys(local_name)
    
    sleep(0.5)
    
    select_tipo_local = waits.wait_visibility({"css_selector" : 'select[name="tipo_id"]'})
    
    select_tipo_local = Select(select_tipo_local)
    
    select_tipo_local.select_by_value("1")
    
    sleep(0.5)
    
    capacity_input = waits.wait_visibility({'css_selector' : 'input[name="capacidade"]'})
    
    capacity_input.send_keys(50)
    
    sleep(0.5)
    
    photo_button = waits.wait_visibility({"css_selector" : '''button[onclick="openOverlay('overlayAddImagem')"]'''})
    
    photo_button.click()
    sleep(0.5)
    
    photo = waits.wait_clickable({"css_selector" : 'label[id="imagem-1"] img'})
    
    photo.click()
    
    sleep(0.5)
    
    confirm_img_button = waits.wait_visibility({"css_selector" : '''div[class="overlay active"] button[onclick="closeOverlay('overlayAddImagem')"]'''})
    
    confirm_img_button.click()
    
    map_image_path = Path(Path(__file__).parent.parent, "images", 'map_image_test.jpg')
    
    image_map_input = waits.wait_visibility({"css_selector" : 'input[id="mapa"]'})
    
    image_map_input.send_keys(f"{map_image_path.absolute()}")
    
    sleep(0.5)
    
    cadastrar_button =  waits.wait_visibility({"css_selector" : 'div[class="mt-2"] button[type="submit"]'})
    
    cadastrar_button.click()
    
    sleep(0.5)
    
    tipo_medida = waits.wait_visibility(
        {
            "css_selector" : 'select[id="tipo_id"]'
        }
    )
    
    tipo_medida_select = Select(tipo_medida)
    
    tipo_medida_select.select_by_value("6")
    
    input_quantidade_medida = waits.wait_clickable(
        {
            "css_selector" : 'input[name="quantidade[]"]'
        }
    )
    
    input_quantidade_medida.send_keys(1)
    
    waits.wait_visibility(
        {
            "css_selector" : 'div[class="p-4 sm:p-8 flex flex-col bg-white shadow sm:rounded-lg"] div[class="mt-2"] button[type="submit"]'
        }
    ).click()
    
    
    sucess_medida = waits.wait_visibility(
        {
            "css_selector" : 'div p.text-sm.text-gray-600'
        }
    )
    
    assert sucess_medida.text == 'Medida cadastrada com sucesso.'