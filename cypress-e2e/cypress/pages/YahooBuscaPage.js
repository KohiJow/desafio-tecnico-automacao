import { YahooResultadosPage } from './YahooResultadosPage'

// Pagina inicial da busca do Yahoo BR: campo de busca e lista de sugestoes.
export class YahooBuscaPage {
  static CAMINHO = '/?fr2=p:fprd,mkt:br'

  campoBusca() {
    return cy.get('input[name="p"]')
  }

  sugestaoCom(termo) {
    return cy.contains('ul.sa-list li.sa-item', new RegExp(termo, 'i'))
  }

  abrir() {
    cy.visit(YahooBuscaPage.CAMINHO)
    return this
  }

  buscarPelaSugestao(termo) {
    this.campoBusca().should('be.visible').type(termo, { delay: 50 })
    this.sugestaoCom(termo).should('be.visible').click()
    return new YahooResultadosPage()
  }
}
