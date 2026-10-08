from playwright.sync_api import Page

# A data nao esta renderizada na tela: ela vem do campo dateModified dentro do
# bloco de dados estruturados (JSON-LD) da pagina.
DADOS_ESTRUTURADOS_CARREGADOS = """() => Array.from(document.querySelectorAll('script'))
    .some(tag => tag.textContent && tag.textContent.includes('dateModified'))"""

EXTRAI_DATE_MODIFIED = r"""() => {
    for (const tag of document.querySelectorAll('script')) {
        const conteudo = tag.textContent;
        if (conteudo && conteudo.includes('dateModified')) {
            const achou = conteudo.match(/"dateModified":\s*"([^"]+)"/);
            if (achou) return achou[1];
        }
    }
    return null;
}"""


def test_uol_termos_data_atualizacao(page: Page):
    """
    Captura a data de atualização dos Termos de Uso da UOL.
    """
    page.goto("https://noticias.uol.com.br/regras/termos-de-uso/")

    # Espera o bloco de dados estruturados existir, em vez de dormir um tempo fixo
    page.wait_for_function(DADOS_ESTRUTURADOS_CARREGADOS, timeout=30000)

    date_modified = page.evaluate(EXTRAI_DATE_MODIFIED)

    assert date_modified, "dateModified não encontrado na página de termos da UOL"

    print(f"\nData de atualização dos Termos de Uso da UOL: {date_modified}")
