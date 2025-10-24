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