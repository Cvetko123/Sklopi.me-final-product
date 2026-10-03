// Autor: Aleksandar Cvetković
const passwordRequirements = {
    minLength: 8,
    hasUppercase: /[A-Z]/,
    hasLowercase: /[a-z]/,
    hasNumber: /[0-9]/
};


function validatePassword(password) {
    const requirements = {
        minLength: password.length >= passwordRequirements.minLength,
        hasUppercase: passwordRequirements.hasUppercase.test(password),
        hasLowercase: passwordRequirements.hasLowercase.test(password),
        hasNumber: passwordRequirements.hasNumber.test(password)
    };

    return requirements;
}


function isPasswordValid(requirements) {
    return Object.values(requirements).every(req => req === true);
}


function doPasswordsMatch(password, confirmPassword) {
    return password === confirmPassword && password.length > 0;
}


function updatePasswordFeedback(password) {
    const feedbackElement = document.getElementById('passwordFeedback');
    if (!feedbackElement) return;

    const requirements = validatePassword(password);

    let feedbackHTML = '<div class="password-feedback">';
    feedbackHTML += '<p class="feedback-title">Šifra mora sadržati:</p>';
    feedbackHTML += '<ul class="feedback-list">';
    feedbackHTML += `<li class="${requirements.minLength ? 'valid' : 'invalid'}">Minimum  karaktera</li>`;
    feedbackHTML += `<li class="${requirements.hasUppercase ? 'valid' : 'invalid'}">Barem jedno veliko slovo</li>`;
    feedbackHTML += `<li class="${requirements.hasLowercase ? 'valid' : 'invalid'}">Barem jedno malo slovo</li>`;
    feedbackHTML += `<li class="${requirements.hasNumber ? 'valid' : 'invalid'}">Barem jedan broj</li>`;
    feedbackHTML += '</ul>';
    feedbackHTML += '</div>';

    feedbackElement.innerHTML = feedbackHTML;
}


function updatePasswordMatchFeedback(password, confirmPassword) {
    const matchElement = document.getElementById('passwordMatchFeedback');
    if (!matchElement) return;

    if (confirmPassword.length === 0) {
        matchElement.innerHTML = '';
        return;
    }

    const matches = doPasswordsMatch(password, confirmPassword);
    const matchHTML = `<div class="password-match ${matches ? 'valid' : 'invalid'}">
        ${matches ? '✓ Šifre se poklapaju' : '✗ Šifre se ne poklapaju'}
    </div>`;

    matchElement.innerHTML = matchHTML;
}


function handleRegisterSubmit() {

    const username = document.getElementById('username').value.trim();
    const email = document.getElementById('email').value.trim();
    const password = document.getElementById('password').value;
    const confirmPassword = document.getElementById('confirmPassword').value;


    if (!username) {
        alert('Molim vas unesite korisničko ime');
        return;
    }

    if (!email) {
        alert('Molim va unesite email');
        return;
    }

    const passwordReqs = validatePassword(password);
    if (!isPasswordValid(passwordReqs)) {
        alert('Šifra ne zadovoljava sve zahteve');
        return;
    }

    if (!doPasswordsMatch(password, confirmPassword)) {
        alert('Šifre se ne poklapaju');
        return;
    }


    alert('Uspešno ste napravili nalog!');

    console.log('Form data:', { username, email, password });



    window.location.href = 'login.html';

}


function handleLoginSubmit(event) {
    event.preventDefault();

    const email = document.getElementById('email').value.trim();
    const password = document.getElementById('password').value;

    if (!email) {
        alert('Molim vas unesite email');
        return;
    }

    if (!password) {
        alert('Molim vas unesite password');
        return;
    }

    alert('Uspesno ste se ulogovali!');

    console.log('Login data:', { email, password });


    window.location.href = 'account.html';

}


document.addEventListener('DOMContentLoaded', function() {
    const registerForm = document.getElementById('registerForm');
    const loginForm = document.getElementById('loginForm');
    const passwordInput = document.getElementById('password');
    const confirmPasswordInput = document.getElementById('confirmPassword');


    if (registerForm) {
        registerForm.addEventListener('submit', handleRegisterSubmit);

        if (passwordInput) {
            passwordInput.addEventListener('input', function() {
                updatePasswordFeedback(this.value);
                if (confirmPasswordInput && confirmPasswordInput.value) {
                    updatePasswordMatchFeedback(this.value, confirmPasswordInput.value);
                }
            });
        }

        if (confirmPasswordInput) {
            confirmPasswordInput.addEventListener('input', function() {
                if (passwordInput) {
                    updatePasswordMatchFeedback(passwordInput.value, this.value);
                }
            });
        }
    }


    if (loginForm) {
        loginForm.addEventListener('submit', handleLoginSubmit);
    }
});

