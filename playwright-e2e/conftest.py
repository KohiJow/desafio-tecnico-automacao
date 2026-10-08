import pytest
from playwright.sync_api import expect

import config


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    """
    Yahoo e UOL respondem conforme regiao e idioma do navegador.
    Fixar locale e fuso deixa o resultado do teste igual em qualquer maquina.
    """
    return {
        **browser_context_args,
        "locale": config.LOCALE,
        "timezone_id": config.TIMEZONE,
    }


@pytest.fixture(autouse=True)
def timeouts_padrao(page):
    """Aplica os timeouts do config.py a cada pagina e ao expect()."""
    page.set_default_timeout(config.TIMEOUT_ACAO)
    page.set_default_navigation_timeout(config.TIMEOUT_NAVEGACAO)
    expect.set_options(timeout=config.TIMEOUT_ACAO)
