# Desafio tecnico: testes E2E em Playwright e Cypress

Resolucao de um desafio tecnico de automacao de testes. Duas atividades, a
primeira feita nas duas ferramentas, para comparar a abordagem de cada uma.

## As atividades

**1. Busca no Yahoo.** Abrir o Yahoo BR, pesquisar um termo, clicar na sugestao
e validar que a busca realmente aconteceu: a URL muda para a pagina de
resultados e o termo aparece nos titulos dos resultados.

**2. Termos de Uso da UOL.** Acessar a pagina de termos e extrair a data da
ultima atualizacao. O dado nao esta no texto visivel: vem do `dateModified`
dentro de um bloco de dados estruturados, entao o teste le o DOM por JavaScript.

## Estrutura

```
playwright/
  conftest.py                      locale pt-BR e fuso de Sao Paulo
  test_busca_yahoo.py              atividade 1
  test_termos_uol.py               atividade 2
cypress-e2e/
  cypress.config.js
  cypress/e2e/busca-yahoo.cy.js    atividade 1 em Cypress
```

## Rodando o Playwright

```bash
pip install playwright pytest-playwright
playwright install
pytest playwright/ -v
```

Para ver o navegador abrindo: `pytest playwright/ -v --headed`
Para ver a data impressa pelo teste da UOL: `pytest playwright/test_termos_uol.py -v -s`

## Rodando o Cypress

```bash
cd cypress-e2e
npm install
npm run cy:open    # modo interativo
npm run cy:run     # modo headless
```

## Decisoes de teste

**Sem sleep fixo.** Nenhum teste usa espera por tempo. No Playwright a espera e
por condicao (`expect`, `locator.wait_for`, `page.wait_for_function`); no Cypress
e o retry do proprio `cy.get` com `should`. Teste que dorme um numero fixo de
segundos ou falha sem motivo em maquina lenta, ou gasta tempo de graca.

**Aviso de privacidade do Yahoo.** Ele aparece de forma intermitente, dependendo
de regiao e cookies. O teste em Playwright espera o botao por 3 segundos e segue
adiante se ele nao aparecer, em vez de assumir que o aviso sempre existe.

**Data da UOL.** Em vez de depender de um seletor de tela, o teste espera o
bloco de dados estruturados carregar e le o campo `dateModified`, que e a fonte
real do dado.

**Timeouts do Cypress.** Ficam em `cypress-e2e/cypress.config.js`. O padrao de 4s
e curto para site de terceiro, por isso o comando padrao usa 10s e o load da
pagina, 60s.

## Limitacoes conhecidas

Os dois testes batem em sites reais, sem mock. Mudanca de layout do Yahoo ou da
UOL quebra os seletores. A atividade 2 so existe em Playwright.

Rodando de um IP de datacenter, os dois sites bloqueiam o acesso: o Yahoo
devolve HTTP 500 com corpo vazio e a UOL devolve 403 "Access Denied". Rode da
maquina local, com navegador instalado, e nao de um servidor.
