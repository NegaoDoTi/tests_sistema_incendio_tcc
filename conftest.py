import pytest
from utils.driver import Driver  
from utils.waits import Waits
from pathlib import Path
from json import load

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


def load_data(arquivo):

    caminho = Path(Path(__file__).parent, arquivo)
    if not caminho.exists():
        raise FileNotFoundError(f"Arquivo de dados não encontrado: {caminho}")


    elif caminho.suffix == ".json":
        with open(caminho, encoding="utf-8") as f:
            dados = load(f)
            if not isinstance(dados, list):
                raise ValueError("O JSON precisa ser uma lista de objetos")
            return [tuple(d.values()) for d in dados]

    else:
        raise ValueError("Formato de arquivo não suportado use JSON)")
    
    
@pytest.fixture
def dados_teste(request):
    """
    Fixture que recebe o caminho do arquivo via `pytest.mark.parametrize(indirect=True)`.
    """
    return load_data(request.param)