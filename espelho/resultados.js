// Resultados organicos montados a partir do termo da URL, na estrutura que os
// page objects leem (#web div.algo h3.title). O titulo da aba leva o termo,
// como no site real.
const termo = new URLSearchParams(location.search).get('p') || ''
document.title = termo + ' - Busca (espelho local)'

const MODELOS = [
  (t) => t + ': documentacao oficial',
  (t) => 'Primeiros passos com ' + t,
  (t) => 'Como escrever testes estaveis com ' + t,
  (t) => t + ' em projetos reais: boas praticas',
]
const web = document.getElementById('web')
for (const modelo of MODELOS) {
  const algo = document.createElement('div')
  algo.className = 'algo'
  const titulo = document.createElement('h3')
  titulo.className = 'title'
  titulo.textContent = modelo(termo)
  algo.append(titulo)
  web.append(algo)
}
