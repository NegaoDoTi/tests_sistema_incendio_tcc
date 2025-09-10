import cv2
from utils.waits import Waits
from time import sleep
from selenium.webdriver.remote.webdriver import WebDriver
from requests import get
from uuid import uuid4
from pathlib import Path

def test_gerar_qrcode(
    driver:WebDriver, 
    waits:Waits, 
    user_name:str = "teste fulano", 
    user_email:str = "teste@email.com" , 
    user_password:str = "teste123456789@teste"
) -> None:
    
    """Teste de gerar qr code CT7

    Args:
        driver (WebDriver): Driver selenium
        waits (Waits): Waits selenium
        user_name (str, optional): . Defaults to "teste fulano".
        user_email (str, optional): . Defaults to "teste@email.com".
        user_password (str, optional): . Defaults to "teste123456789@teste".
    """
    
    
    qrcodes_path = Path(Path(__file__).parent.parent, "qrcodes")
    
    if not qrcodes_path.exists():
        qrcodes_path.mkdir()     

    url = "http://medidasincendio.test/login"
    
    driver.get(url)
    
    email_input = waits.wait_visibility({"css_selector" : 'input[id="email"]'})
    
    email_input.send_keys(user_email)
    
    password_input = waits.wait_visibility({"css_selector" : 'input#password'})
    
    password_input.send_keys(user_password)
    
    button_login = waits.wait_visibility({"css_selector" : 'button[type="submit"]'})
    
    button_login.click()
    
    sleep(5)
    
    driver.get("http://medidasincendio.test/locais")
    
    local_a = waits.wait_visibility_all(
        {
            "css_selector" : 'div[class="grid"] a'
        }
    )[-1]
    
    local_a.click()
    
    local_id = driver.current_url.split("/")[-1]
    
    waits.wait_clickable(
        {
            "css_selector" : "button[onclick=\"openOverlay('qr-code')\"]"
        }
    ).click()
    
    img = waits.wait_visibility(
        {
            "css_selector" : 'div[id="qr-code"] img'
        }
    )
    
    url_img = img.get_attribute("src")
    
    response  = get(url_img, verify=False, stream=True)
    
    assert response.status_code == 200
    
    qrcode_image_path = Path(f"{qrcodes_path}/{uuid4()}.png")
    
    with open(f"{qrcode_image_path}", "wb") as qrcode_image:
        for chunk in response.iter_content(chunk_size=8192):
            qrcode_image.write(chunk)
        
        qrcode_image.close()
        
    assert qrcode_image_path.exists()
    
    assert qrcode_image_path.suffix == ".png"

    img = cv2.imread(str(qrcode_image_path))

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    _, binarized = cv2.threshold(gray, 128, 255, cv2.THRESH_BINARY)

    binarized = cv2.bitwise_not(binarized)

    detector = cv2.QRCodeDetector()

    data, bbox, straight_qrcode = detector.detectAndDecode(binarized)
    
    for file in qrcodes_path.iterdir():
            if file.is_file():
                file.unlink()
    
    assert data == f"http://medidasincendio.test/mobile/locais/{local_id}"
    
    