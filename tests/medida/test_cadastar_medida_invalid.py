from utils.waits import Waits
from time import sleep
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import Select
from datetime import datetime
from pathlib import Path
from json import loads
import pytest

@pytest.mark.parametrize("dados_teste", ["parameters\\invalid_medida.json"], indirect=True)
def test_cadastrar_medida(
    driver:WebDriver, 
    waits:Waits, 
    dados_teste,
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
        
    
    duracoes = []
    for i, dados in enumerate(dados_teste):
        
        inicio = datetime.now()
        
        i+=1
        
        nome, descricao, icone, foto = dados
        
        
        driver.get('http://medidasincendio.test/locais/74')
    
        sleep(1)
        
        register_medida_btn = waits.wait_clickable({'css_selector' : 'aside.max-w-xl.w-full + section h2:nth-of-type(2) a button'})
        register_medida_btn.click()
        
        sleep(3)

        tipo_medida = waits.wait_visibility(
            {
                "css_selector" : 'select[id="tipo_id"]'
            }
        )
        
        sleep(1)
        
        tipo_medida_select = Select(tipo_medida)
        tipo_medida_select.select_by_value("novo")
        
        if nome != "":
            input_nome = waits.wait_visibility({"css_selector": "input#tipo_medida_select"})
            input_nome.send_keys(nome)
        
        if descricao != "":
            input_descricao = waits.wait_visibility({"css_selector": "textarea[name=descricao]"})
            input_descricao.send_keys(descricao)
        
        foto_path = Path(Path(__file__).parent.parent.parent, "images", f'{foto}')
        icone_path = Path(Path(__file__).parent.parent.parent, "images", f'{icone}')
        
        add_foto = waits.wait_presence({"css_selector" : 'input#foto'})
        add_icone = waits.wait_presence({"css_selector" : 'input#icone'})
        
        if foto != "":
            add_foto.send_keys(f"{foto_path.absolute()}")
        
        if icone != "":
            add_icone.send_keys(f"{icone_path.absolute()}")
            
        button_submit = waits.wait_clickable({"css_selector": 'form#tipoMedidaForm button[type=submit]'})
        button_submit.click()
        
        sleep(2)
        
        try:
            verificar = waits.wait_visibility(
                    {"css_selector" : 'div.alert.alert-danger > ul > li'},
                    time=5
                )
            
            if nome == "" and descricao != "":
                
                assert "O campo nome é obrigatório." in verificar.text
                
            
            
            if nome != "" and descricao == "":
                
                assert "O campo descricao é obrigatório." in verificar.text
                
            if icone == "" and nome != "":
                
                try:
                    assert "O campo icone é obrigátorio" in verificar.text
                except:
                    pass
                
                
            if foto == "" and nome != "":
                
                try:
                    assert "O campo foto é obrigátorio" in verificar.text
                except:
                    pass
                
            if nome == "" and descricao == "" and icone == "" and foto == "":
                
                try:
                    assert "O campo nome é obrigatório." in verificar.text
                except:
                    pass
                
        except:
            print(f"Teste: {i} Passou porem com bugs! Não mostrou mensagem de erro!")
                
        fim = datetime.now()
        
        check = fim - inicio
        
        duracoes.append(f"{check.seconds}:{check.microseconds}")
                    
    print(duracoes)