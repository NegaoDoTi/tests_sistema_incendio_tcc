import pytest
from utils.driver import Driver  
from utils.waits import Waits

@pytest.fixture(scope="function")
def driver():
    """Função que cria o driver para os testes do pytest

    Yields:
        WebDriver: Driver chrome do selenium
    """
    driver_instance = Driver().get_chrome_driver()

    if isinstance(driver_instance, dict):
        pytest.fail(f"Erro ao iniciar o driver: {driver_instance.get('exception')}")

    yield driver_instance

    driver_instance.quit()


@pytest.fixture(scope="function")
def waits(driver):
    """Função que cria classe de Waits para os tests do Pytest

    Args:
        driver (WebDriver): Driver chrome do selenium

    Returns:
        Waits: classe de waits para selenium
    """
    return Waits(driver)