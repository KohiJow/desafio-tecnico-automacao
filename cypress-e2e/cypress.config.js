const { defineConfig } = require('cypress')

module.exports = defineConfig({
  e2e: {
    specPattern: 'cypress/e2e/**/*.cy.js',
    supportFile: 'cypress/support/e2e.js',
    // Os testes batem em site real, entao vale um timeout maior que o padrao de 4s.
    defaultCommandTimeout: 10000,
    pageLoadTimeout: 60000,
    video: false,
  },
})
