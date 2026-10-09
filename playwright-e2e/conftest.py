import pytest
from playwright.sync_api import Browser, expect

import config


@pytest.fixture(scope="session")
def browser_type_launch_args(browser_type_launch_args, browser_name):
    """
    Abre o Chromium completo em vez do headless shell (ver config.CHROMIUM_CHANNEL).
    Um --browser-channel passado na linha de comando continua valendo.
    """
    if browser_name != "chromium":
        return browser_type_launch_args
    return {"channel": config.CHROMIUM_CHANNEL, **browser_type_launch_args}


def _user_agent_sem_marca_headless(browser: Browser) -> str:
    """
    O Yahoo responde HTTP 500 com corpo vazio, e a UOL 403, quando o user agent
    traz "HeadlessChrome". Le o user agent real do navegador e troca so essa
    marca, mantendo versao e sistema coerentes com o binario que esta rodando.
    """
    pagina = browser.new_page()
    try:
        user_agent = pagina.evaluate("navigator.userAgent")
    finally:
        pagina.close()
    return user_agent.replace("HeadlessChrome/", "Chrome/")


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args, browser: Browser):
    """
    Yahoo e UOL respondem conforme regiao e idioma do navegador.
    Fixar locale e fuso deixa o resultado do teste igual em qualquer maquina.
    """
    return {
        **browser_context_args,
        "locale": config.LOCALE,
        "timezone_id": config.TIMEZONE,
        "user_agent": _user_agent_sem_marca_headless(browser),
    }


@pytest.fixture(autouse=True)
def timeouts_padrao(page):
    """Aplica os timeouts do config.py a cada pagina e ao expect()."""
    page.set_default_timeout(config.TIMEOUT_ACAO)
    page.set_default_navigation_timeout(config.TIMEOUT_NAVEGACAO)
    expect.set_options(timeout=config.TIMEOUT_ACAO)
