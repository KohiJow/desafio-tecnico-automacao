import re

from playwright.sync_api import Page, expect
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError


# termo da busca em minusculo: a assercao da URL compara com p=playwright
TERMO = "playwright"


def fechar_aviso_privacidade(page: Page) -> None:
    """
    O Yahoo mostra um aviso de privacidade de forma intermitente.
    Espera o botao por alguns segundos e segue em frente se ele nao aparecer.
    """
    botao = page.get_by_role("button", name="OK")
    try:
        botao.wait_for(state="visible", timeout=3000)
    except PlaywrightTimeoutError:
        return
    botao.click()


def test_busca_no_yahoo(page: Page):
    # 1. Abre Yahoo BR
    page.goto("https://br.search.yahoo.com/?fr2=p:fprd,mkt:br")

    # 2. Digita o termo de busca
    campo_busca = page.get_by_placeholder("Buscar na Web")
    expect(campo_busca).to_be_visible()
    campo_busca.fill(TERMO)

    # 3. Clica na sugestão com o termo
    sugestao = page.get_by_text(TERMO).first
    expect(sugestao).to_be_visible()
    sugestao.click()

    # 4. Fecha o aviso de privacidade se ele aparecer
    fechar_aviso_privacidade(page)

    # 5. Valida que a URL é a de resultados para o termo
    expect(page).to_have_url(re.compile(r"p=" + TERMO, re.IGNORECASE))

    # 6. Garante que o termo aparece na página de resultados
    expect(page.get_by_text(re.compile(TERMO, re.IGNORECASE)).first).to_be_visible()

    # 7. Garante que há resultados (links principais com data-matarget="algo")
    resultados = page.locator('[data-matarget="algo"]')
    expect(resultados.first).to_be_visible()
    assert resultados.count() > 0, "Nenhum resultado de busca encontrado no Yahoo"

    # 8. Valida que algum resultado cita o termo pesquisado
    textos = resultados.all_text_contents()
    assert any(TERMO in texto.lower() for texto in textos), \
        f"Nenhum resultado contem '{TERMO}' no texto visivel"
