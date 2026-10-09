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

  // Pagina que o Yahoo devolve no lugar dos resultados quando limita as buscas
  // de um IP (comum nos runners compartilhados do GitHub): "Ocorreram problemas
  // temporarios na busca de paginas da Web". Quem chama decide o que fazer.
  seLimitado(acao) {
    cy.url().should('match', /[?&]p=/)
    cy.get('body').then(($body) => {
      if (/problemas tempor/i.test($body.text())) acao()
    })
    return this
  }

  deveTerResultadoCitando(termo) {
    const padrao = new RegExp(termo, 'i')
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
