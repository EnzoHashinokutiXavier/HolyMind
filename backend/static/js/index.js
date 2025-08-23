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