const { defineConfig } = require('cypress')

module.exports = defineConfig({
  e2e: {
    // Pode ser sobrescrita por variavel de ambiente: CYPRESS_BASE_URL=https://...
    baseUrl: 'https://br.search.yahoo.com',
    specPattern: 'cypress/e2e/**/*.cy.js',
    supportFile: 'cypress/support/e2e.js',
    // Os testes batem em site real, entao vale um timeout maior que o padrao de 4s.
    defaultCommandTimeout: 10000,
    pageLoadTimeout: 60000,
    // Busca em site externo oscila. No modo headless (cypress run, CI) o teste
    // e refeito ate duas vezes antes de contar como falha; no modo interativo nao.
    retries: {
      runMode: 2,
      openMode: 0,
    },
    screenshotOnRunFailure: true,
    video: false,
  },
})
