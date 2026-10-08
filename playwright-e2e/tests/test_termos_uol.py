import pytest
from playwright.sync_api import Page

from pages.uol_termos import UolTermosPage


def test_uol_termos_data_atualizacao(page: Page):
    """Captura a data de atualizacao dos Termos de Uso da UOL."""
    termos = UolTermosPage(page)

    status = termos.abrir()
    if status == 403:
        # A UOL bloqueia IP de datacenter (CI, servidor). Nao e defeito da pagina,
        # entao o teste e pulado com o motivo em vez de falhar como se fosse.
        pytest.skip("UOL devolveu HTTP 403 (Access Denied): bloqueio de IP, rode de uma maquina local")
    assert status == 200, f"Pagina de termos da UOL respondeu HTTP {status}"

    data_atualizacao = termos.data_atualizacao()

    assert data_atualizacao, "dateModified nao encontrado na pagina de termos da UOL"
    print(f"\nData de atualizacao dos Termos de Uso da UOL: {data_atualizacao}")
