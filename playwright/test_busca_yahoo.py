import re

from playwright.sync_api import Page, expect
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError


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


def test_pacto_solucoes_yahoo(page: Page):
    # 1. Abre Yahoo BR
    page.goto("https://br.search.yahoo.com/?fr2=p:fprd,mkt:br")

    # 2. Digita o termo de busca
    campo_busca = page.get_by_placeholder("Buscar na Web")
    expect(campo_busca).to_be_visible()
    campo_busca.fill("Pacto Soluções")

    # 3. Clica na sugestão com o texto
    sugestao = page.get_by_text("Pacto Soluções").first
    expect(sugestao).to_be_visible()
    sugestao.click()

    # 4. Fecha o aviso de privacidade se ele aparecer
    fechar_aviso_privacidade(page)

    # 5. Valida que a URL é de resultados para "pacto"
    expect(page).to_have_url(re.compile(r"p=pacto"))

    # 6. Garante que algum resultado com "Pacto Soluções" está visível
    expect(page.get_by_text("Pacto Soluções").first).to_be_visible()

    # 7. Garante que há resultados (links principais com data-matarget="algo")
    resultados = page.locator('[data-matarget="algo"]')
    expect(resultados.first).to_be_visible()
    assert resultados.count() > 0, "Nenhum resultado de busca encontrado no Yahoo"

    # 8. Valida que algum resultado cita a empresa pesquisada
    textos = resultados.all_text_contents()
    assert any("pacto" in texto.lower() for texto in textos), \
        "Nenhum resultado contém 'Pacto' no texto visível"
