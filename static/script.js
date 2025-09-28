document.addEventListener('DOMContentLoaded', function () {
    var toggleButton = document.querySelector('.menu-toggle');
    var navMenu = document.querySelector('.nav-menu');

    if (!toggleButton || !navMenu) return;

    toggleButton.addEventListener('click', function () {
        var isOpen = navMenu.classList.toggle('open');
        toggleButton.setAttribute('aria-expanded', String(isOpen));
    });
});

let usuariologado = false;

function verifyLogin(usuariologado) {
    
    if (usuariologado == true) {
        // envia a mensagem pra tela de chat
    } else {
        window.location.href = './login/index.html';
    }
}

