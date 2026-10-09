# Desafio tecnico: testes E2E em Playwright e Cypress

Resolucao de um desafio tecnico de automacao de testes. Duas atividades, a
primeira feita nas duas ferramentas, para comparar a abordagem de cada uma.
As duas suites rodam no GitHub Actions: a cada push contra um espelho local do
fluxo, e toda semana contra os sites reais.

## As atividades

**1. Busca no Yahoo.** Abrir o Yahoo BR, digitar um termo, clicar na sugestao
que contem o termo e validar que a busca realmente aconteceu: a URL e o titulo
da aba passam a ser os da pagina de resultados do termo, ha resultados
organicos e pelo menos um titulo cita o termo. O termo fica numa constante no
topo de cada teste (`TERMO`), porque todas as validacoes dependem dele.

**2. Termos de Uso da UOL.** Acessar a pagina de termos e extrair a data da
ultima atualizacao. O dado nao esta no texto visivel: vem do `dateModified`
dentro de um bloco de dados estruturados (JSON-LD), entao o teste le o DOM por
JavaScript. Essa atividade so existe em Playwright.

## Estrutura

```
playwright-e2e/
  config.py                        URLs, navegador, locale, fuso e timeouts: tudo que e ambiente
  conftest.py                      aplica o config ao navegador e ao expect
  pytest.ini                       pasta dos testes e relatorio HTML
  requirements.txt
  pages/
    yahoo.py                       YahooBuscaPage e YahooResultadosPage
    uol_termos.py                  UolTermosPage
  tests/
    test_busca_yahoo.py            atividade 1
    test_termos_uol.py             atividade 2
espelho/                           copia minima do fluxo do Yahoo e da pagina da UOL, para o CI
cypress-e2e/
  cypress.config.js                baseUrl, timeouts e retries
  cypress/pages/                   YahooBuscaPage.js e YahooResultadosPage.js
  cypress/e2e/busca-yahoo.cy.js    atividade 1 em Cypress
.github/workflows/testes.yml       roda as duas suites no espelho e no site real
```

## Rodando o Playwright

Precisa de Python 3.9 ou mais novo.

```bash
cd playwright-e2e
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
playwright install chromium
pytest
```

O relatorio sai em `playwright-e2e/reports/relatorio.html` a cada execucao
(pytest-html, arquivo unico, com o motivo de cada falha ou skip).

Outras formas de rodar:

```bash
pytest -v --headed                      # ve o navegador abrindo
pytest tests/test_termos_uol.py -s      # imprime a data lida da UOL
pytest --reruns 2 --reruns-delay 5      # refaz teste que falhou, como no CI
UOL_TERMOS_URL=http://localhost:8000/termos.html pytest tests/test_termos_uol.py
```

A ultima linha mostra a sobrescrita de URL por variavel de ambiente
(`YAHOO_BASE_URL` e `UOL_TERMOS_URL`), que e como a suite roda contra o espelho
local, igual ao CI faz a cada push:

```bash
python3 -m http.server 8080 --directory ../espelho &
YAHOO_BASE_URL=http://127.0.0.1:8080 UOL_TERMOS_URL=http://127.0.0.1:8080/uol-termos.html pytest
```

## Rodando o Cypress

```bash
cd cypress-e2e
npm install
npm run cy:open      # modo interativo
npm run cy:run       # headless, relatorio spec do proprio Cypress no terminal
npm run cy:run:ci    # headless, mais o XML JUnit em cypress/results/ (usado no CI)
```

Em falha no modo headless o Cypress salva screenshot em `cypress/screenshots/`,
um por tentativa. A `baseUrl` pode ser trocada por variavel de ambiente, que e
como ele roda contra o espelho local:
`CYPRESS_BASE_URL=http://127.0.0.1:8080 npm run cy:run`.

## Page Objects

Cada pagina tem uma classe que concentra seletores e acoes; o teste so descreve
o fluxo e as assercoes. Nas duas suites a leitura e a mesma: `YahooBuscaPage`
abre a busca e `buscar_pela_sugestao(termo)` devolve `YahooResultadosPage`, que
sabe onde estao os resultados e os titulos. No Cypress os metodos de validacao
(`deveEstarNosResultadosDe`, `deveTerResultadoCitando`) devolvem `this` para
encadear. Quando o Yahoo mudar o layout, o ajuste fica num unico lugar por suite.

## Decisoes de teste

**Configuracao num lugar so.** No Playwright, `config.py` guarda URLs, canal
do navegador, locale, fuso e timeouts; o `conftest.py` aplica tudo ao
navegador, ao contexto, a cada pagina e ao `expect()`. No Cypress,
`cypress.config.js` guarda `baseUrl`, timeouts e retries. Nenhum teste tem URL
ou numero de timeout embutido.

**Sem sleep fixo.** Nenhum teste usa espera por tempo. No Playwright a espera e
por condicao (`expect`, `wait_for_url`, `wait_for_function`); no Cypress e o
retry do proprio `cy.get` com `should`. Teste que dorme um numero fixo de
segundos ou falha sem motivo em maquina lenta, ou gasta tempo de graca.

**Navegador headless.** Dois bloqueios aparecem so quando o Chromium roda sem
tela. O Yahoo responde HTTP 500 com corpo vazio quando o user agent traz
`HeadlessChrome`; sem tratar isso o teste nem passa do `page.goto`. O
`conftest.py` le o user agent real do navegador e troca so essa marca por
`Chrome`, mantendo versao e sistema coerentes com o binario em uso. A UOL
responde 403 "Access Denied" ao headless shell, o Chromium reduzido que o
Playwright abre por padrao, mesmo com o user agent trocado: os client hints
(`sec-ch-ua`) desse binario continuam anunciando `HeadlessChrome`. Por isso a
suite abre o Chromium completo em modo headless novo (`CHROMIUM_CHANNEL` em
`config.py`), cujos client hints sao os mesmos do modo com tela. Com as duas
medidas os dois testes passam headless, inclusive de um servidor. O Cypress,
rodando no Electron, nao sofre o bloqueio do Yahoo; a UOL tambem o recusa.

**Aviso de privacidade do Yahoo.** Ele aparece de forma intermitente, conforme
regiao e cookies, e vem num iframe de outro dominio (`guce.yahoo.com`): um
locator da pagina principal nunca encontra o botao OK. O page object usa
`frame_locator`, espera o botao por ate 5 segundos e segue em frente se ele nao
vier. No Cypress o aviso nao cobre o campo de busca nem as primeiras
sugestoes, e o teste clica na primeira que contem o termo, entao nao precisa
fecha-lo.

**Data da UOL.** Em vez de depender de um seletor de tela, o page object espera
o bloco de dados estruturados carregar e le o campo `dateModified`, que e a
fonte real do dado. Como o dado vem do HTML, o `goto` espera so o
`domcontentloaded`: a pagina carrega muitos anuncios e esperar o load completo
so deixa o teste lento e sujeito a timeout.

**403 da UOL.** Se a UOL ainda recusar o acesso (navegador que ela reconheca
como automatizado, rede bloqueada), o teste trata o caso de forma explicita:
com status 403 ele e marcado como pulado, com o motivo no relatorio, porque
isso e indisponibilidade do ambiente e nao defeito da pagina. Qualquer outro
status diferente de 200 falha normalmente.

**Comparacao de texto sem depender de maiuscula.** O titulo do resultado vem do
Yahoo com a capitalizacao que ele quiser, entao a comparacao e por expressao
regular com flag de ignorar caso, nas duas suites.

**Timeouts.** Playwright: 10s para acao e `expect`, 30s para navegacao e para
a espera pelo JSON-LD da UOL, 5s para o aviso de privacidade, todos em
`config.py`. Cypress: 10s por comando e 60s para load da pagina, em
`cypress.config.js`. O padrao das ferramentas (5s e 4s) e curto para site de
terceiro.

**Retries.** Busca em site externo oscila: ranking, sugestoes e latencia mudam
de uma execucao para outra. Contra o site real o pytest roda com
`--reruns 2 --reruns-delay 20` (plugin `pytest-rerunfailures`) e o Cypress com
`retries.runMode = 2`. Fora do CI o Playwright roda sem retry por padrao, para
a oscilacao aparecer, e no `cypress open` o retry e zero.

**Limite de buscas do Yahoo.** O Yahoo limita as buscas de IPs que buscam
demais e, no lugar dos resultados, devolve "Ocorreram problemas temporarios na
busca de paginas da Web". Os runners do GitHub usam IPs compartilhados por
muita gente, entao isso acontece no CI sem nenhum excesso deste repositorio: num
mesmo run, o job do Playwright pegou a pagina nas tres tentativas enquanto o do
Cypress, em outra maquina, passou. Retry nao resolve, porque o limite e do IP. As
duas suites reconhecem a pagina e marcam o teste como pulado, com o motivo no
relatorio, do mesmo jeito que o 403 da UOL: e o site que nao respondeu, nao a
suite que quebrou.

**Espelho local.** `espelho/` tem uma copia minima do fluxo: a pagina de busca
com o campo `name="p"`, a lista de sugestoes e o aviso de privacidade num
iframe, a pagina de resultados com `#web div.algo h3.title`, e a pagina de
termos da UOL que injeta o JSON-LD com atraso de proposito, para provar que a
espera e por condicao. Nao e o Yahoo: e o contrato que os page objects esperam
dele. A cada push as duas suites rodam ali, sem rede externa, e o resultado e
deterministico. Mudanca de layout dos sites reais e pega pela execucao semanal.

## CI

`.github/workflows/testes.yml` tem dois modos:

- **Espelho local**, a cada push na `main`, em pull request e por disparo
  manual: sobe `espelho/` com o `http.server` do Python no proprio runner e roda
  as duas suites contra ele. Vermelho aqui e defeito de verdade.
- **Site real**, toda segunda as 12h UTC e por disparo manual: as mesmas suites
  contra o Yahoo e a UOL, com retries. Serve para pegar mudanca de layout dos
  sites; limite de buscas do Yahoo aparece como teste pulado.

Commit que so mexe em texto (`*.md` e `docs/`) nao dispara os testes, e um push
novo cancela o run anterior do mesmo ramo. Cada job publica artefatos: o
relatorio HTML do pytest e o JUnit do Cypress com os screenshots de falha, e tem
limite de tempo, para site travado nao deixar o run pendurado. No runner do
GitHub os dois testes do Playwright passam contra o site real, inclusive o da
UOL, que com o headless shell era pulado por 403.

## Limitacoes conhecidas

O espelho local cobre o contrato que os page objects esperam, nao o site real:
mudanca de layout do Yahoo ou da UOL so aparece na execucao semanal (ou num
disparo manual), e quebra os seletores, que ficam concentrados em `pages/`. A atividade 2 so
existe em Playwright: a UOL recusa o Electron do Cypress com 403. Os bloqueios
a navegador headless e o tratamento do 403 estao descritos acima.
