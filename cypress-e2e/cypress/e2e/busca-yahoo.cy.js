// termo em minusculo: a validacao da URL compara com p=playwright
const TERMO = 'playwright'

describe('Busca no Yahoo', () => {
  it(`Deve buscar "${TERMO}" no Yahoo e validar resultados`, () => {
    cy.visit('https://br.search.yahoo.com/?fr2=p:fprd,mkt:br')

    // Preenche e busca
    cy.get('input[name="p"]')
      .should('be.visible')
      .type(TERMO, { delay: 50 })

    // Espera a sugestao aparecer antes de clicar
    cy.get('#sa-item0 > .sa-item-title')
      .should('be.visible')
      .click()

    // Validação 1: URL mudou (busca foi executada)
    cy.url().should('include', `p=${TERMO}`)

    // Validação 2: o termo aparece na página de resultados
    cy.contains(new RegExp(TERMO, 'i')).should('be.visible')

    // Validação 3: h3.title é o título de cada resultado
    cy.get('h3.title')
      .should('have.length.greaterThan', 0)
      .first()
      .invoke('text')
      .should('match', new RegExp(TERMO, 'i'))
  })
})
