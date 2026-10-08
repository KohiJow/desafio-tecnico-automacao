"""
Configuracao central da suite: URLs, timeouts e identidade do navegador.
Tudo que depende de ambiente fica aqui, nunca espalhado pelos testes.
"""
import os

# As URLs aceitam sobrescrita por variavel de ambiente, para apontar a suite
# para um espelho ou um stub local sem mexer no codigo.
YAHOO_BASE_URL = os.environ.get("YAHOO_BASE_URL", "https://br.search.yahoo.com")
UOL_TERMOS_URL = os.environ.get(
    "UOL_TERMOS_URL", "https://noticias.uol.com.br/regras/termos-de-uso/"
)

LOCALE = "pt-BR"
TIMEZONE = "America/Sao_Paulo"

# Timeouts em milissegundos. Sites de terceiro respondem mais devagar que
# uma aplicacao local, por isso os valores sao maiores que o padrao do Playwright.
TIMEOUT_ACAO = 10_000  # expect(), click, fill
TIMEOUT_NAVEGACAO = 30_000  # goto, wait_for_url, wait_for_function
TIMEOUT_AVISO = 5_000  # aviso de privacidade do Yahoo, que nem sempre aparece
