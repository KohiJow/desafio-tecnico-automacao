import re
from playwright.sync_api import Page


def test_uol_termos_data_atualizacao(page: Page):
    """
    Captura a data de atualização dos Termos de Uso da UOL
    """
    
    # Acessa a página com user agent real
    page.goto("https://noticias.uol.com.br/regras/termos-de-uso/")
    
    # Espera um tempo fixo
    page.wait_for_timeout(5000)
    
    # Executa JavaScript para pegar dateModified direto do DOM
    date_modified = page.evaluate("""
        () => {
            const scripts = document.querySelectorAll('script');
            for (let script of scripts) {
                const text = script.textContent;
                if (text && text.includes('dateModified')) {
                    const match = text.match(/"dateModified":\s*"([^"]+)"/);
                    if (match) return match[1];
                }
            }
            return null;
        }
    """)
    
    if date_modified:
        print("\n" + "="*60)
        print("DATA DE ATUALIZACAO DOS TERMOS DE USO DA UOL")
        print("="*60)
        print(f"Data encontrada: {date_modified}")
        print("="*60)
    else:
        assert False, "dateModified nao encontrado"