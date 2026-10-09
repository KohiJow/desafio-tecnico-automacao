// Pagina de resultados da busca: lista de resultados organicos e seus titulos.
export class YahooResultadosPage {
  resultados() {
    return cy.get('#web div.algo')
  }

  titulos() {
    return cy.get('#web div.algo h3.title')
  }

  deveEstarNosResultadosDe(termo) {
    cy.url().should('match', new RegExp(`[?&]p=${termo}`, 'i'))
    cy.title().should('match', new RegExp(termo, 'i'))
    return this
  }

  deveTerResultadoCitando(termo) {
    const padrao = new RegExp(termo, 'i')
    // Pagina que o Yahoo devolve no lugar dos resultados quando recebe buscas
    // demais em sequencia: "Ocorreram problemas temporarios na busca...".
    cy.get('body').then(($body) => {
      expect(
        $body.text(),
        'o Yahoo devolveu a pagina de problemas temporarios em vez dos resultados (oscilacao do site, nao seletor quebrado)'
      ).not.to.match(/problemas tempor/i)
    })
    this.resultados().should('have.length.greaterThan', 0)
    // should com funcao reexecuta ate passar ou estourar o timeout
    this.titulos().should(($titulos) => {
      const textos = [...$titulos].map((el) => el.innerText.trim())
      expect(
        textos.some((texto) => padrao.test(texto)),
        `algum titulo de resultado cita "${termo}" (titulos: ${textos.join(' | ')})`
      ).to.be.true
    })
    return this
  }
}
