import re
from typing import List

from playwright.sync_api import Locator, Page, expect
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError

import config


class YahooBuscaPage:
    """Pagina inicial da busca do Yahoo BR: campo de busca e lista de sugestoes."""

    CAMINHO = "/?fr2=p:fprd,mkt:br"

    def __init__(self, page: Page):
        self.page = page
        self.campo_busca = page.locator('input[name="p"]')
        self.sugestoes = page.locator("ul.sa-list li.sa-item")
        # O aviso de privacidade vem num iframe de outro dominio (guce.yahoo.com),
        # por isso o botao nao aparece para um locator da pagina principal.
        self.aviso_privacidade = page.locator("#guce-inline-consent-iframe")
        self.botao_ok_aviso = page.frame_locator("#guce-inline-consent-iframe").get_by_role(
            "button", name="OK"
        )

    def abrir(self) -> "YahooBuscaPage":
        self.page.goto(config.YAHOO_BASE_URL + self.CAMINHO)
        self.fechar_aviso_privacidade()
        return self

    def fechar_aviso_privacidade(self) -> None:
        """
        O aviso aparece de forma intermitente, conforme regiao e cookies.
        Espera alguns segundos pelo botao e segue em frente se ele nao vier.
        """
        try:
            self.botao_ok_aviso.click(timeout=config.TIMEOUT_AVISO)
        except PlaywrightTimeoutError:
            return
        expect(self.aviso_privacidade).to_be_hidden()

    def sugestao_com(self, termo: str) -> Locator:
        return self.sugestoes.filter(has_text=re.compile(re.escape(termo), re.IGNORECASE)).first

    def buscar_pela_sugestao(self, termo: str) -> "YahooResultadosPage":
        expect(self.campo_busca).to_be_visible()
        self.campo_busca.fill(termo)

        sugestao = self.sugestao_com(termo)
        expect(sugestao).to_be_visible()
        sugestao.click()
        return YahooResultadosPage(self.page)


class YahooResultadosPage:
    """Pagina de resultados da busca: lista de resultados organicos e seus titulos."""

    def __init__(self, page: Page):
        self.page = page
        self.resultados = page.locator("#web div.algo")
        self.titulos = self.resultados.locator("h3.title")
        # Pagina que o Yahoo devolve no lugar dos resultados quando recebe buscas
        # demais em sequencia: "Ocorreram problemas temporarios na busca...".
        self.aviso_problema_temporario = page.get_by_text(
            re.compile("problemas tempor", re.IGNORECASE)
        ).first

    def esperar_resultados_de(self, termo: str) -> "YahooResultadosPage":
        self.page.wait_for_url(re.compile(r"[?&]p=" + re.escape(termo), re.IGNORECASE))
        expect(self.resultados.first.or_(self.aviso_problema_temporario)).to_be_visible()
        if self.aviso_problema_temporario.is_visible():
            raise AssertionError(
                "O Yahoo devolveu a pagina de problemas temporarios em vez dos resultados: "
                "oscilacao do site, nao seletor quebrado"
            )
        return self

    def textos_dos_titulos(self) -> List[str]:
        return self.titulos.all_inner_texts()
