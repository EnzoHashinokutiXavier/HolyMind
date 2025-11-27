

function closeSetup() {
    const setupOverlay = document.querySelector('.setup');
    if (setupOverlay) {
        setupOverlay.classList.remove('active');

        const ANIMATION_DURATION = 400; // 400ms

        setTimeout(() => {
            if (setupOverlay.parentNode) {
                setupOverlay.parentNode.removeChild(setupOverlay);
            }
        }, ANIMATION_DURATION);
    }
}


function toggleSelection(clickedBtn, container) {
    const siblings = container.querySelectorAll('button');
    siblings.forEach(btn => btn.classList.remove('selected'));
    clickedBtn.classList.add('selected');
}

function showSetup() {
    if (document.querySelector('.setup')) {
        console.warn('O setup já está visível na tela, evitando duplicação.');
        return;
    }

    

    const setupOverlay = document.createElement('div')
    setupOverlay.className = 'setup'
    setupOverlay.addEventListener('click', function(e) {
        if (e.target === setupOverlay) {
            closeSetup();
        }
    });


    // Card
    const setupCard = document.createElement('div')
    setupCard.className = 'setup-card'

    // -- Card - Seção 1
    const headerDiv = document.createElement('div')

    const h2 = document.createElement('h2')
    h2.textContent = 'Personalize sua jornada'

    const subtitle = document.createElement('p')
    subtitle.className = 'subtitle'
    subtitle.textContent = 'Responda ao questionario para receber uma experiência adequada ao seu aprendizado'

    headerDiv.appendChild(h2)
    headerDiv.appendChild(subtitle)

    // -- Card - Seção 2

    const denomDiv = document.createElement('div')
    const denomLabel = document.createElement('label')
    denomLabel.textContent = 'Qual sua denominação?'

    const chipContainer = document.createElement('div')
    chipContainer.className = 'chip-container'

    const denominations = [
        'Católico', 'Evangélico tradicional', 'Evang. pentecostal',
        'Neopentecostal', 'Protestante histórico', 'Adventista',
        'Ortodoxo', 'Não-denominacional', 'Outro'
    ];

    denominations.forEach(text => {
        const btn = document.createElement('button');
        btn.className = 'chip';
        btn.textContent = text;
        btn.addEventListener('click', function() {
            toggleSelection(this, chipContainer);
        });
        chipContainer.appendChild(btn);
    });

    denomDiv.appendChild(denomLabel);
    denomDiv.appendChild(chipContainer);

    // -- Card -- Seção 3

    const levelDiv = document.createElement('div')
    const levelLabel = document.createElement('label')
    levelLabel.textContent = 'Seu nível de conhecimento:'

    const levelContainer = document.createElement('div')
    levelContainer.className = 'level-container'

    const levels = ['Baixo', 'Médio', 'Grande'];

    levels.forEach(text => {
        const btn = document.createElement('button');
        btn.className = 'level-btn';
        btn.textContent = text;
        btn.addEventListener('click', function() {
            toggleSelection(this, levelContainer);
        });
        levelContainer.appendChild(btn);
    });

    levelDiv.appendChild(levelLabel);
    levelDiv.appendChild(levelContainer);

    // -- Card -- Seção 4

    modeSetup = 0;
    var denominationValue = 'none'
    var levelValue = 'none'

    const actionsDiv = document.createElement('div');
    actionsDiv.className = 'actions';

    const confirmBtn = document.createElement('button');
    confirmBtn.className = 'btn-primary';
    confirmBtn.textContent = 'Confirmar Personalização';

    const skipBtn = document.createElement('button');
    skipBtn.className = 'btn-link';
    skipBtn.textContent = 'Pular este passo';
    skipBtn.addEventListener('click', function() {

        updateSetup({modeSetup, denominationValue, levelValue})

    });

    confirmBtn.addEventListener('click', function() { 
        modeSetup = 1;
        const selectedDenomBtn = chipContainer.querySelector('.chip.selected');
        const selectedLevelBtn = levelContainer.querySelector('.level-btn.selected');
        
        denominationValue = selectedDenomBtn ? selectedDenomBtn.textContent : null;
        levelValue = selectedLevelBtn ? selectedLevelBtn.textContent : null;

        if (!denominationValue || !levelValue) {
            alert("Por favor, selecione uma opção em ambos os campos.");
            return;
        }

        

        const userResponse = {
            modeSetup,
            denominationValue,
            levelValue
        };

        updateSetup(userResponse);
    });

    

    actionsDiv.appendChild(confirmBtn);
    actionsDiv.appendChild(skipBtn);

    // fim do card

    // estrutura
    setupCard.appendChild(headerDiv);
    setupCard.appendChild(denomDiv);
    setupCard.appendChild(levelDiv);
    setupCard.appendChild(actionsDiv);

    setupOverlay.appendChild(setupCard);

    document.body.appendChild(setupOverlay);
    
    setTimeout(() => {
        setupOverlay.classList.add('active');
    }, 10);
}

async function updateSetup(body) {
    try {
            const response = await fetch('/auth/save-setup', { 
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                credentials: "include",
                body: JSON.stringify(body)
            });

            if (response.ok) {
                console.log("Configurações salvas com sucesso!");
                closeSetup();
            } else {
                const errorData = await response.json();
                console.error("Erro ao salvar configurações:", errorData);
                alert("Erro ao salvar suas preferências. Tente novamente.");
            }
        } catch (error) {
            console.error("Erro na requisição de salvar configurações:", error);
            alert("Não foi possível conectar ao servidor para salvar suas preferências.");
        }
}

// 2. Lógica Principal (DOMContentLoaded)

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
    async function getAuthStatus() {
        try {
            const resp = await fetch('/auth/status', {
                method: "GET",
                credentials: "include" // VERY IMPORTANT para enviar cookie HttpOnly
            });
            const data = await resp.json(); // { logado: true/false, setup: "no"/"yes" }
            return data;
        } catch (e) {
            console.error("Erro ao checar status auth:", e);
            return { logado: false, setup: "no" };
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

        const status = await getAuthStatus();

        if (status.logado) {
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
            
            if (status.setup === "no" || status.setup === "false" || status.setup === false) {
                

                showSetup(); 
            }

        } else {
            console.log("Usuário não logado. Exibindo botões de login/cadastro.");
            
        }
    }

    // -----------------------------------------------------------------
    // 4. Inicialização
    // -----------------------------------------------------------------
    await updateUIForLoginState();
    
    window.verifyLogin = async function() {
        if (await isUserLoggedIn()) { // isUserLoggedIn não está definida aqui
            console.log("Usuário logado. Abrindo chat...");
        } else {
            window.location.href = '/static/auth/index.html';
        }
    }

});