document.addEventListener('DOMContentLoaded', () => {
    const loginForm = document.querySelector('.login');
    const registerForm = document.querySelector('.register');
    const registerLink = document.querySelector('.login .auth-sign-up a');
    const loginLink = document.querySelector('.register .auth-sign-up a');
    
    registerLink.addEventListener('click', (e) => {
        e.preventDefault(); 
        loginForm.classList.add('hidden');
        registerForm.classList.remove('hidden');
        registerForm.classList.add('active');
    });

    loginLink.addEventListener('click', (e) => {
        e.preventDefault();
        registerForm.classList.add('hidden');
        loginForm.classList.remove('hidden');
        loginForm.classList.add('active');
    });
});

async function auth(type, event) {
    if (type == 'login') {
        
        if (event) event.preventDefault(); 
        
        const username = document.getElementById('login-username').value.trim();  
        const password = document.getElementById('login-password').value.trim();  
        const respostatela = document.getElementById('sucess')

        if (!username || !password)
            return mostrarErro(respostatela, "Preencha todos os campos!");

        await sendRequest("login", {username, password}, respostatela);
    }
        
    if (type == 'register') {
        if (event) event.preventDefault(); 

        const username = document.getElementById('register-username').value.trim();
        const password = document.getElementById('register-password').value.trim();
        const confirm = document.getElementById('register-password-confirm').value.trim();
        const birthDate = document.getElementById('register-date').value.trim();
        
        const respostatela = document.getElementById('error') 

        if (!username  || !password || !birthDate || !confirm) 
            return mostrarErro(respostatela, "Preencha todos os campos!");
        

        if (password.length < 8) 
            return mostrarErro(respostatela, "Senha deve ter pelo menos 8 digitos!");

        if (password != confirm) 
            return mostrarErro(respostatela, "As senhas inseridas devem ser iguais!");
        
        
        await sendRequest("register", {username, password, birthDate}, respostatela);
        
        
    }
}


async function sendRequest(endpoint, body, resposta) {
    try {
        const resp = await fetch(`/auth/${endpoint}`, {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify(body),
            credentials: "include",
        });

        const data = await resp.json();
        
        if (resp.ok) {
            if (endpoint === 'login') {
                resposta.style.color = "green";
                resposta.innerText = "Login realizado com sucesso! Redirecionando...."; 

                setTimeout(window.location.href = '/', 1000000);
                return;
            }
            
            resposta.style.color = "green";
            resposta.innerText = "Operação realizada com sucesso!";
            
            setTimeout(window.location.reload(), 4000);
        } else { 
            // Lógica para erros (400, 401, etc.)
            resposta.style.color = "red";
            resposta.innerText = data.detail
                ? `Erro: ${data.detail}`
                : "Erro inesperado na API.";
        }
    } catch (err) {
        // Este bloco só deve ser atingido por erros de rede ou de JSON
        console.error("Erro na requisição ou no parse JSON:", err); 
        resposta.style.color = "red";
        resposta.innerText = "Erro de rede ou formato de resposta inesperado.";
    }
}

function mostrarErro(iderrorHTML, msg) {
    iderrorHTML.style.color = "red";
    iderrorHTML.innerText = msg;
}