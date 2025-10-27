document.addEventListener('DOMContentLoaded', async function () {
    // -----------------------------------------------------------------
    // 1. Lógica do Menu Toggle
    // -----------------------------------------------------------------
    var toggleButton = document.querySelector('.menu-toggle');
    var navMenu = document.querySelector('.nav-menu');

    if (toggleButton && navMenu) {
        toggleButton.addEventListener('click', function () {
            var isOpen = navMenu.classList.toggle('open');
            toggleButton.setAttribute('aria-expanded', String(isOpen));
        });
    }

    // -----------------------------------------------------------------
    // 2. Funções de Autenticação
    // -----------------------------------------------------------------
    async function isUserLoggedIn() {
        try {
            const resp = await fetch('/auth/status');
            const data = await resp.json();
            return data.logado; 
        } catch (e) {
            console.error("Erro ao checar status de login: ", e);
            return false;
        }
    }
    
    async function handleLogout() {
        try {
            const resp = await fetch('/auth/logout', {
                method: 'POST',
                credentials: 'include'
            });

            if (resp.ok) {
                console.log("Cookie de sessão removido com sucesso.");

                await updateUIForLoginState(false);
            }
        } catch (error) {
            console.error("Erro ao chamar endpoint logout", error);
        }

        window.location.href = '/'; 
    }

    // -----------------------------------------------------------------
    // 3. Função de Atualização da UI
    // -----------------------------------------------------------------
    async function updateUIForLoginState() {
        const accountDiv = document.querySelector('.account');
        if (!accountDiv) return;

        if (await isUserLoggedIn()) {
            
            accountDiv.innerHTML = ''; 

            const profileButton = document.createElement('button');
            profileButton.className = 'signin';
            profileButton.textContent = 'Perfil';
            profileButton.onclick = () => { window.location.href = '/perfil.html'; }; 
            
            const logoutButton = document.createElement('button');
            logoutButton.className = 'signin';
            logoutButton.textContent = 'Log Out';
            
            logoutButton.onclick = handleLogout; 
            
            accountDiv.appendChild(profileButton);
            accountDiv.appendChild(logoutButton);
            
            const apresentationH1 = document.querySelector('.apresentation h1');
            if (apresentationH1) {
                apresentationH1.textContent = "Bem-vindo de volta! 👋";
            }
            
        }
    }

    // -----------------------------------------------------------------
    // 4. Inicialização
    // -----------------------------------------------------------------
    await updateUIForLoginState();
    
    window.verifyLogin = async function() {
        if (await isUserLoggedIn()) {
            console.log("Usuário logado. Abrindo chat...");
        } else {
            window.location.href = '/static/auth/index.html';
        }
    }
});