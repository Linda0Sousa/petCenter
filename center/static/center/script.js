//this is for the landing page forms

window.addEventListener('DOMContentLoaded', function() {
    document.getElementById('signup-btn').addEventListener('click', function(event) {
        event.preventDefault(); 
        document.getElementById('signup-form').style.display = 'block';
        document.getElementById('landing-page').style.display = 'none';
        document.getElementById('login-form').style.display = 'none';
        document.getElementById('verify-number').style.display = 'none';
        document.getElementById('verify-email').style.display = 'none';
    });

});