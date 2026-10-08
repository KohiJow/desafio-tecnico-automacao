import re

from playwright.sync_api import Page, expect

from pages.yahoo import YahooBuscaPage

# termo da busca em minusculo: a assercao da URL compara com p=playwright
TERMO = "playwright"


def test_busca_no_yahoo_pela_sugestao(page: Page):
    busca = YahooBuscaPage(page).abrir()

    resultados = busca.buscar_pela_sugestao(TERMO).esperar_resultados_de(TERMO)

    # A busca aconteceu: URL e titulo da aba sao os da pagina de resultados do termo
    expect(page).to_have_url(re.compile(r"[?&]p=" + TERMO, re.IGNORECASE))
    expect(page).to_have_title(re.compile(TERMO, re.IGNORECASE))

    # Ha resultados e pelo menos um titulo cita o termo pesquisado
    titulos = resultados.textos_dos_titulos()
    assert titulos, "Nenhum resultado de busca encontrado no Yahoo"
    assert any(TERMO in titulo.lower() for titulo in titulos), (
        f"Nenhum titulo de resultado contem '{TERMO}'. Titulos: {titulos}"
    )
