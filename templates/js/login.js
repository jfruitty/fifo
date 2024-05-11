function LoginForm(){
    document.addEventListener('DOMContentLoaded', () => {
        const loginForm = document.querySelector('.login-form');
        loginForm.addEventListener('submit', async function(event) {
            event.preventDefault();
            const email = document.querySelector('#email').value;
            const password = document.querySelector('#password').value;
            const userIsLoggedIn = await eel.login(email, password)();
            if (userIsLoggedIn) {
                sessionStorage.setItem("userid", userIsLoggedIn.userid);
                window.location.href = 'locationStock.html';
            } else {
                alert('Login failed. Please check your email and password.');
            }

        });

        const goToRegisterButton = document.getElementById('go-to-register');
        if(goToRegisterButton) {
            goToRegisterButton.addEventListener('click', function() {
                window.location.href = 'register.html';
            });
        }


    });
}


LoginForm()

