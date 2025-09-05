from utils.waits import Waits
from time import sleep
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import Select
from pathlib import Path

def test_cadastrar_local(
    driver:WebDriver, 
    waits:Waits, 
    user_email:str = "teste@email.com" , 
    user_password:str = "teste123456789@teste", 
    local_name:str = "Local Teste"
) -> None:
    
    """Testa o cadastramento de locais

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
    
    driver.get('http://medidasincendio.test/locais/cadastrar')
    
    'form section button[type="submit"]'
    
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
    
    driver.get("http://medidasincendio.test/locais")
    
    locais_name = waits.wait_visibility_all(
        {
            "css_selector" : 'div[class="font-thin drop-shadow-text font-display text-2xl mb-2 whitespace-nowrap text-center text-white"]'
        }
    )
    
    for local in locais_name:
        if local.text == f"Auditório: {local_name}":
            break
        
    assert local.text == f"Auditório: {local_name}"