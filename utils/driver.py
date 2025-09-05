from selenium.webdriver.chrome.webdriver import WebDriver as ChromeWebdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from traceback import format_exc

class Driver():
    """Classe responsavel pro gerenciar driver selenium que o robo irá utilizar!
    """
    
    def __init__(self):
        self.__driver:ChromeWebdriver
        
    def get_chrome_driver(self) -> ChromeWebdriver | dict:
        """Responsavel por conectar Python ao driver Selenium, e definir as opções 

        Returns:
        
            ChromeWebdriver | dict: {bool, str, str}
        """
        
        
        try:
        
            
            self.__options = ChromeOptions()
                        
            self.__service = ChromeService(executable_path=ChromeDriverManager().install())
            
            self.__driver = ChromeWebdriver(options=self.__options, service=self.__service)

            self.__driver.maximize_window()

            return self.__driver
        
        except Exception:
            return {'error' : True, "type" : "Erro inesperado ao iniciar o Navegador", "exception" : f'{format_exc()}'}
