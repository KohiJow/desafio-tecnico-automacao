import { YahooBuscaPage } from '../pages/YahooBuscaPage'

// termo em minusculo: a validacao da URL compara com p=playwright
const TERMO = 'playwright'

describe('Busca no Yahoo', () => {
  it(`Deve buscar "${TERMO}" pela sugestao e validar os resultados`, () => {
    const busca = new YahooBuscaPage().abrir()

    const resultados = busca.buscarPelaSugestao(TERMO)

    resultados
      .deveEstarNosResultadosDe(TERMO)
      .deveTerResultadoCitando(TERMO)
  })
})
