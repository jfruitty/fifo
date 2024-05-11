document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('register-form').addEventListener('submit', function(event) {
        event.preventDefault();
        const email = document.getElementById('email').value;
        const password = document.getElementById('password').value;
        const confirmPassword = document.getElementById('confirm-password').value;

        if (password !== confirmPassword) {
            alert('Passwords do not match.');
            return;
        }
        console.log(email, password)
        eel.register_user(email, password)(function(response) {
            if (response.status) {
                alert('Registration successful!');
                window.location.href = 'login.html';
            } else {
                alert(response.message);
            }
        });
    });
});