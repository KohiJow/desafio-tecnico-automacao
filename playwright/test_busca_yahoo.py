import re
from playwright.sync_api import Page, expect


def test_pacto_solucoes_yahoo(page: Page):
    # 1. Abre Yahoo BR
    page.goto("https://br.search.yahoo.com/?fr2=p:fprd,mkt:br")

    # 2. Digita o termo de busca
    page.get_by_placeholder("Buscar na Web").fill("Pacto Soluções")

    # 3. Clica na sugestão com o texto
    page.get_by_text("Pacto Soluções").first.click()

    # 4. Fecha o modal de privacidade se aparecer
    page.wait_for_timeout(2000)
    try:
        page.get_by_role("button", name="OK").click()
    except Exception:
        pass

    # 5. Valida que a URL é de resultados para "pacto"
    expect(page).to_have_url(re.compile(r"p=pacto"))

    # 6. Garante que algum resultado com "Pacto Soluções" está visível
    expect(page.get_by_text("Pacto Soluções").first).to_be_visible()

    # 7. Garante que há resultados (links principais com data-matarget="algo")
    results = page.locator('[data-matarget="algo"]')
    count = results.count()
    assert count > 0, "Nenhum resultado de busca encontrado em Yahoo"

    # 8. Valida que aparece resultados na pesquisa referente a empresa
    all_results = results.all_text_contents()
    assert any("Pacto" in text.lower() for text in all_results), \
        "Nenhum resultado contém 'Pacto' no texto visível"