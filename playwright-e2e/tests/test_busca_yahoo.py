import re

import pytest
from playwright.sync_api import Page, expect

from pages.yahoo import YahooBuscaPage, YahooLimitouBuscas

# termo da busca em minusculo: a assercao da URL compara com p=playwright
TERMO = "playwright"


def test_busca_no_yahoo_pela_sugestao(page: Page):
    busca = YahooBuscaPage(page).abrir()

    try:
        resultados = busca.buscar_pela_sugestao(TERMO).esperar_resultados_de(TERMO)
    except YahooLimitouBuscas as limite:
        # Mesmo tratamento do 403 da UOL: bloqueio do site, registrado como pulado
        # com o motivo no relatorio, em vez de uma falha que parece defeito.
        pytest.skip(str(limite))

    # A busca aconteceu: URL e titulo da aba sao os da pagina de resultados do termo
    expect(page).to_have_url(re.compile(r"[?&]p=" + TERMO, re.IGNORECASE))
    expect(page).to_have_title(re.compile(TERMO, re.IGNORECASE))

    # Ha resultados e pelo menos um titulo cita o termo pesquisado
    titulos = resultados.textos_dos_titulos()
    assert titulos, "Nenhum resultado de busca encontrado no Yahoo"
    assert any(TERMO in titulo.lower() for titulo in titulos), (
        f"Nenhum titulo de resultado contem '{TERMO}'. Titulos: {titulos}"
    )
