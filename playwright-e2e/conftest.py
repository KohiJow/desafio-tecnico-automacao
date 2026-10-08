import pytest


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    """
    Yahoo e UOL respondem conforme regiao e idioma do navegador.
    Fixar locale e fuso deixa o resultado do teste igual em qualquer maquina.
    """
    return {
        **browser_context_args,
        "locale": "pt-BR",
        "timezone_id": "America/Sao_Paulo",
    }
