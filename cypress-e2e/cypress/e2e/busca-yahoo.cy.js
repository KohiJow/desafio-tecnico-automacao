import { YahooBuscaPage } from '../pages/YahooBuscaPage'

// termo em minusculo: a validacao da URL compara com p=playwright
const TERMO = 'playwright'

describe('Busca no Yahoo', () => {
  // function (e nao arrow) para ter o this.skip() do mocha
  it(`Deve buscar "${TERMO}" pela sugestao e validar os resultados`, function () {
    const busca = new YahooBuscaPage().abrir()

    const resultados = busca.buscarPelaSugestao(TERMO)

    // Bloqueio do site real fica registrado como teste pulado, nao como falha
    resultados.seLimitado(() => this.skip())

    resultados
      .deveEstarNosResultadosDe(TERMO)
      .deveTerResultadoCitando(TERMO)
  })
})
