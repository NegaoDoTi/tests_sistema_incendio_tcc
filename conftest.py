import pytest
from utils.driver import Driver  
from utils.waits import Waits

@pytest.fixture(scope="function")
def driver():
    """
    Esta fixture cria uma instância do driver antes de cada teste
    e a destrói (fecha o navegador) ao final.
    """
    # --- SETUP (Executa antes do teste) ---
    driver_instance = Driver().get_chrome_driver()

    if isinstance(driver_instance, dict):
        pytest.fail(f"Erro ao iniciar o driver: {driver_instance.get('exception')}")

    # A palavra 'yield' entrega o driver para o teste
    yield driver_instance

    # --- TEARDOWN (Executa depois do teste) ---
    print("\nFechando o navegador...")
    driver_instance.quit()


@pytest.fixture(scope="function")
def waits(driver):
    """
    Fixture que cria uma instância da sua classe Waits,
    já recebendo o driver da fixture anterior.
    """
    return Waits(driver)