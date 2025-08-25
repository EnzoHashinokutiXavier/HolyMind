

// Código para interagir com a API e mostrar a resposta da IA na tela




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



// Código para popular os selects de livros, capítulos e versículos da bíblia




let versiculos = [];
let versiculosDoCapitulo = [];

fetch('/static/bibles/biblia.json') // busca o arquivo JSON no servidor
  .then(res => res.json()) // converte a resposta em JSON
  .then(data => { // armazena os dados na variável global
    versiculos = data; // array de versículos
    popularLivros(); // chama a função para popular os livros no select
  })
    .catch(err => console.error("Erro no fetch:", err));

function popularLivros() { // popula o select de livros
  const livroSelect = document.getElementById('livro-select'); // pega o select do HTML

  // gera lista única de livros usando livro_id como valor e livro como label
  const livros = [...new Map(versiculos.map(v => [v.livro_id, v.livro])).entries()]; // array de arrays [id, nome]

  livroSelect.innerHTML = `<option value="" disabled selected>Selecione o Livro</option>`;
  livros.forEach(([id, nome]) => { // para cada livro, cria uma opção no select
    const opt = document.createElement('option'); // cria o elemento option
    opt.value = id;          // usar id único para o value
    opt.textContent = nome;  // mostrar nome do livro
    livroSelect.appendChild(opt); // adiciona a opção ao select
  });

  livroSelect.addEventListener('change', () => { // quando o livro mudar
    const livroId = livroSelect.value; // pega o id do livro selecionado
    const capituloSelect = document.getElementById('capitulo-select'); // pega o select de capítulos

    // pega todos os capítulos desse livro
    const capitulos = [...new Set(
      versiculos.filter(v => v.livro_id === livroId).map(v => String(v.capitulo)) // array único de capítulos
    )];

    capituloSelect.innerHTML = `<option value="" disabled selected>Capítulo</option>`; 
    capitulos.forEach(cap => { // para cada capítulo, cria uma opção no select
      const opt = document.createElement('option'); // cria o elemento option
      opt.value = cap;
      opt.textContent = cap;
      capituloSelect.appendChild(opt);
    });

    capituloSelect.onchange = () => { // quando o capítulo mudar
      const cap = capituloSelect.value; // pega o capítulo selecionado
      const versiculoSelect = document.getElementById('versiculo-select'); // pega o select de versículos

      // pega todos os versículos do capítulo
      const vers = versiculos
        .filter(v => v.livro_id === livroId && String(v.capitulo) === String(cap)) // filtra por livro e capítulo
        .map(v => String(v.versiculo)); // array de versículos

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

function buscarVersiculo() { // busca o versículo selecionado e mostra no HTML
  const livroId = document.getElementById('livro-select').value;
  const cap = document.getElementById('capitulo-select').value;
  const vers = document.getElementById('versiculo-select').value;

  const resultado = versiculos.find(v => // encontra o versículo exato
    v.livro_id === livroId && // filtra por livro
    String(v.capitulo) === String(cap) && // filtra por capítulo
    String(v.versiculo) === String(vers) // filtra por versículo
  );

  document.getElementById('referencia').textContent = `${resultado.livro} ${cap}:${vers}`; // mostra a referência
  document.getElementById('texto').textContent = resultado?.texto || 'Não encontrado'; // mostra o texto do versículo

  // Guarda todos os versículos do capítulo (pra "mostrar mais")
  versiculosDoCapitulo = versiculos.filter(v =>
    v.livro_id === livroId && String(v.capitulo) === String(cap) // filtra por livro e capítulo
  );

  document.getElementById('mais-btn').style.display = 'inline-block'; // mostra o botão "mostrar mais"
  document.getElementById('mais-versiculos').innerHTML = ''; // limpa a área de mais versículos
}

function mostrarMais() { // mostra mais versículos a partir do selecionado
  const versSelecionado = document.getElementById('versiculo-select').value;
  const container = document.getElementById('mais-versiculos');
  container.innerHTML = '';

  let iniciou = false; // flag para começar a mostrar versículos
  versiculosDoCapitulo.forEach(v => { // percorre os versículos do capítulo
    if (String(v.versiculo) === String(versSelecionado)) iniciou = true; // começa a mostrar a partir do versículo selecionado
    if (iniciou) { // se já iniciou, mostra o versículo
      const p = document.createElement('p'); 
      p.textContent = `${v.capitulo}:${v.versiculo} — ${v.texto}`; // formata o texto
      container.appendChild(p); // adiciona ao container
    }
  });

  container.scrollIntoView({ // rola a página até os versículos mostrados
    behavior: "smooth", // animação suave
    block: "start" // alinha ao topo
  });
}

// Código para abrir e fechar a sidebar de PDF

function toggleSidebar() {
  const sidebar = document.querySelector('.sidebar');
  const togglebtn = document.querySelector('.openbtn'); // agora pega pela classe

  sidebar.classList.toggle('open');

  if (sidebar.classList.contains('open')) {
    togglebtn.classList.add('open');   // some o botão
  } else {
    togglebtn.classList.remove('open'); // aparece de novo
  }
}