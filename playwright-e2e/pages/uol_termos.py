from typing import Optional

from playwright.sync_api import Page

import config

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


class UolTermosPage:
    """Pagina de Termos de Uso da UOL."""

    def __init__(self, page: Page):
        self.page = page

    def abrir(self) -> Optional[int]:
        """Abre a pagina e devolve o status HTTP, para o teste decidir o que fazer com bloqueio."""
        # A pagina carrega muitos anuncios e rastreadores; o dado vem do HTML,
        # entao basta o DOM pronto, sem esperar o load completo.
        resposta = self.page.goto(config.UOL_TERMOS_URL, wait_until="domcontentloaded")
        return resposta.status if resposta is not None else None

    def data_atualizacao(self) -> Optional[str]:
        # Espera o bloco de dados estruturados existir, em vez de dormir um tempo fixo.
        # wait_for_function usa o timeout de acao se nao receber um, e a pagina e pesada.
        self.page.wait_for_function(DADOS_ESTRUTURADOS_CARREGADOS, timeout=config.TIMEOUT_NAVEGACAO)
        return self.page.evaluate(EXTRAI_DATE_MODIFIED)
