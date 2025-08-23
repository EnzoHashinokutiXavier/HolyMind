async function sendRequest(type) {
    const entrada = document.getElementById('entrada').value.trim();
    const respostaIA = document.getElementById('resposta');

    if (!entrada) {
        respostaIA.innerText = "DIGITA ALGUMA COISA AI NÉ CARA";
        return;
    }

    respostaIA.innerText = "Carregando espera ai...";

    try {
        const resp = await fetch(`/${type}`, {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({entrada: entrada})
        });

        if (resp.ok) { // Se a resposta da api for OK
            const data = await resp.json(); // Data vai esperar um json
            respostaIA.innerText = data.explanation; // O json vai ser mostrado no html diretamente na div de ID resposta da IA
        } else { 
            const DataErro = await resp.json(); // Caso responda fora da condição, o erro esperado ser gerado vai ser exibido na div de ID resposta
            respostaIA.innerText = errorData.detail
                ? `Erro: ${errorData.detail}`
                : "Error fetching explanation.";
        }  
    } catch (error) {
        respostaIA.innerText = "Internet ta ruim ou o servidor caiu :("
    }
}