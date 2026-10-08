# Desafio tecnico: testes E2E em Playwright e Cypress

Entrega do desafio de automacao de testes da Pacto Solucoes. Duas atividades,
resolvidas nas duas ferramentas, para comparar a abordagem de cada uma.

## As atividades

**1. Busca no Yahoo.** Abrir o Yahoo BR, pesquisar por "Pacto Solucoes", clicar
na sugestao e validar que a busca realmente aconteceu: a URL muda para a pagina
de resultados e o termo aparece na pagina.

**2. Termos de Uso da UOL.** Acessar a pagina de termos e extrair a data da
ultima atualizacao. O dado nao esta no texto visivel: vem do `dateModified`
dentro de um bloco de dados estruturados, entao o teste le o DOM por JavaScript.

## Estrutura

```
playwright/
  test_busca_yahoo.py     atividade 1
  test_termos_uol.py      atividade 2
cypress-e2e/
  cypress/e2e/busca-yahoo.cy.js   atividade 1 em Cypress
```

## Rodando o Playwright

```bash
pip install playwright pytest-playwright
playwright install
pytest playwright/ -v
```

Para ver o navegador abrindo: `pytest playwright/ -v --headed`

## Rodando o Cypress

```bash
cd cypress-e2e
npm install
npx cypress open     # modo interativo
npx cypress run      # modo headless
```

## Notas sobre os testes

O Yahoo mostra um modal de privacidade de forma intermitente, dependendo de
regiao e cookies. O teste em Playwright trata isso sem quebrar: tenta fechar o
modal e segue adiante se ele nao aparecer.

Na atividade 2 a data nao esta renderizada na tela. Em vez de depender de um
seletor fragil, o teste busca o campo `dateModified` nos scripts da pagina, que
e a fonte real do dado.
