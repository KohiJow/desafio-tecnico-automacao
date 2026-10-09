// A pagina real injeta o JSON-LD depois do carregamento; aqui ele chega com
// atraso de proposito, para a suite provar que espera por condicao e nao por tempo.
setTimeout(() => {
  const dados = document.createElement('script')
  dados.type = 'application/ld+json'
  dados.textContent = JSON.stringify({
    '@context': 'https://schema.org',
    '@type': 'WebPage',
    name: 'Termos de uso',
    dateModified: '2024-05-10T15:30:00-03:00',
  })
  document.head.append(dados)
}, 800)
