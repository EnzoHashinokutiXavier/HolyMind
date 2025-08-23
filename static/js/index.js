async function sendRequest(type) { // Função para requisitar a resposta da IA, mandando a entrada do usuario para a API
    const entrada = document.getElementById('entrada').value.trim(); 
    const respostaIA = document.getElementById('resposta');

    if (!entrada) {
        respostaIA.innerText = "DIGITA ALGUMA COISA AI NÉ CARA"; // Texto para caso o usuario não digite nada
        return;
    }

    respostaIA.innerText = "Carregando espera ai..."; // Texto para loading

    try {
        const resp = await fetch(`/${type}`, { // mandando a requisição
            method: "POST", // tipo da requisição
            headers: {"Content-Type": "application/json"}, // tipo de conteudo da requisição
            body: JSON.stringify({text: entrada}) // corpo em json do conteudo a ser recebido da API
        });

        if (resp.ok) { // Se a resposta da api for OK
            const data = await resp.json(); // Data vai esperar um json
            respostaIA.innerText = data.explanation; // O json vai ser mostrado no html diretamente na div de ID resposta da IA
        } else { 
            const dataErro = await resp.json(); // Caso responda fora da condição, o erro esperado ser gerado vai ser exibido na div de ID resposta
            respostaIA.innerText = dataErro.detail
                ? `Erro: ${dataErro.detail}`
                : "Error fetching explanation.";
        }  
    } catch (error) {
        respostaIA.innerText = "Internet ta ruim ou o servidor caiu :("
    }
}


let versiculos = [];
let versiculosDoCapitulo = [];

fetch('/static/bibles/biblia.json')
  .then(res => res.json())
  .then(data => {
    versiculos = data;
    popularLivros();
  })
    .catch(err => console.error("Erro no fetch:", err));

function popularLivros() {
  const livroSelect = document.getElementById('livro-select');

  // gera lista única de livros usando livro_id como valor e livro como label
  const livros = [...new Map(versiculos.map(v => [v.livro_id, v.livro])).entries()];

  livroSelect.innerHTML = `<option value="" disabled selected>Selecione o Livro</option>`;
  livros.forEach(([id, nome]) => {
    const opt = document.createElement('option');
    opt.value = id;          // usar id único
    opt.textContent = nome;  // mostrar nome
    livroSelect.appendChild(opt);
  });

  livroSelect.addEventListener('change', () => {
    const livroId = livroSelect.value;
    const capituloSelect = document.getElementById('capitulo-select');

    // pega todos os capítulos desse livro
    const capitulos = [...new Set(
      versiculos.filter(v => v.livro_id === livroId).map(v => String(v.capitulo))
    )];

    capituloSelect.innerHTML = `<option value="" disabled selected>Capítulo</option>`;
    capitulos.forEach(cap => {
      const opt = document.createElement('option');
      opt.value = cap;
      opt.textContent = cap;
      capituloSelect.appendChild(opt);
    });

    capituloSelect.onchange = () => {
      const cap = capituloSelect.value;
      const versiculoSelect = document.getElementById('versiculo-select');

      // pega todos os versículos do capítulo
      const vers = versiculos
        .filter(v => v.livro_id === livroId && String(v.capitulo) === String(cap))
        .map(v => String(v.versiculo));

      versiculoSelect.innerHTML = `<option value="" disabled selected>Versículo</option>`;
      vers.forEach(v => {
        const opt = document.createElement('option');
        opt.value = v;
        opt.textContent = v;
        versiculoSelect.appendChild(opt);
      });
    };
  });
}

function buscarVersiculo() {
  const livroId = document.getElementById('livro-select').value;
  const cap = document.getElementById('capitulo-select').value;
  const vers = document.getElementById('versiculo-select').value;

  const resultado = versiculos.find(v =>
    v.livro_id === livroId &&
    String(v.capitulo) === String(cap) &&
    String(v.versiculo) === String(vers)
  );

  document.getElementById('referencia').textContent = `${resultado.livro} ${cap}:${vers}`;
  document.getElementById('texto').textContent = resultado?.texto || 'Não encontrado';

  // Guarda todos os versículos do capítulo (pra "mostrar mais")
  versiculosDoCapitulo = versiculos.filter(v =>
    v.livro_id === livroId && String(v.capitulo) === String(cap)
  );

  document.getElementById('mais-btn').style.display = 'inline-block';
  document.getElementById('mais-versiculos').innerHTML = '';
}

function mostrarMais() {
  const versSelecionado = document.getElementById('versiculo-select').value;
  const container = document.getElementById('mais-versiculos');
  container.innerHTML = '';

  let iniciou = false;
  versiculosDoCapitulo.forEach(v => {
    if (String(v.versiculo) === String(versSelecionado)) iniciou = true;
    if (iniciou) {
      const p = document.createElement('p');
      p.textContent = `${v.capitulo}:${v.versiculo} — ${v.texto}`;
      container.appendChild(p);
    }
  });

  container.scrollIntoView({
    behavior: "smooth",
    block: "start"
  });
}