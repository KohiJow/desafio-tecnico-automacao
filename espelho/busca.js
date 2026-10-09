// Sugestoes geradas a partir do que foi digitado, como a lista do Yahoo:
// o primeiro item e o proprio termo e os outros completam a busca.
const campo = document.querySelector('input[name="p"]')
const lista = document.querySelector('ul.sa-list')
const COMPLEMENTOS = ['', ' tutorial', ' python', ' vs cypress']

campo.addEventListener('input', () => {
  const termo = campo.value.trim()
  lista.replaceChildren()
  lista.hidden = termo === ''
  for (const complemento of COMPLEMENTOS) {
    const texto = termo + complemento
    const item = document.createElement('li')
    item.className = 'sa-item'
    item.textContent = texto
    item.addEventListener('click', () => {
      location.href = 'search.html?p=' + encodeURIComponent(texto) + '&fr=sfp'
    })
    lista.append(item)
  }
})

// O aviso de privacidade fecha quando o botao OK do iframe avisa a pagina.
window.addEventListener('message', (evento) => {
  if (evento.data === 'aviso-ok') document.getElementById('guce-inline-consent-iframe').remove()
})
