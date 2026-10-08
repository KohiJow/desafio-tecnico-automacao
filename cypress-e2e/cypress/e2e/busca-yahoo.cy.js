describe('Busca no Yahoo', () => {
  it('Deve buscar "Pacto Soluções" no Yahoo e validar resultados', () => {
    cy.visit('https://br.search.yahoo.com/?fr2=p:fprd,mkt:br')

    // Preenche e busca
    cy.get('input[name="p"]')
      .should('be.visible')
      .type('Pacto Soluções', { delay: 50 })

    // Espera a sugestao aparecer antes de clicar
    cy.get('#sa-item0 > .sa-item-title')
      .should('be.visible')
      .click()

    // Validação 1: URL mudou (busca foi executada)
    cy.url().should('include', 'p=pacto')

    // Validação 2: "Pacto Soluções" está visível nos resultados
    cy.contains('Pacto Soluções').should('be.visible')

    // Validação 3: h3.title é o título de cada resultado
    cy.get('h3.title')
      .should('have.length.greaterThan', 0)
      .first()
      .should('contain', 'Pacto')
  })
})
