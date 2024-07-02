document.addEventListener('DOMContentLoaded', function() {
    // Form validation
    const registerForm = document.getElementById('register-form');
    const loginForm = document.getElementById('login-form');
    const searchForm = document.getElementById('search-form');
    const searchInput = document.getElementById('search-input');
    const lessonList = document.getElementById('lesson-list');

    if (registerForm) {
        registerForm.addEventListener('submit', function(event) {
            if (!validateRegisterForm()) {
                event.preventDefault();
            }
        });
    }

    if (loginForm) {
        loginForm.addEventListener('submit', function(event) {
            if (!validateLoginForm()) {
                event.preventDefault();
            }
        });
    }

    if (searchForm && searchInput && lessonList) {
        searchInput.addEventListener('keyup', function() {
            const keyword = searchInput.value.toLowerCase();
            filterLessons(keyword);
        });
    }

    function validateRegisterForm() {
        const username = registerForm.username.value.trim();
        const email = registerForm.email.value.trim();
        const password = registerForm.password.value.trim();
        const confirmPassword = registerForm.confirm_password.value.trim();

        if (username.length < 2 || username.length > 20) {
            alert('Username must be between 2 and 20 characters.');
            return false;
        }

        if (!validateEmail(email)) {
            alert('Invalid email address.');
            return false;
        }

        if (password.length < 8 || password.length > 30) {
            alert('Password must be between 8 and 30 characters.');
            return false;
        }

        if (password !== confirmPassword) {
            alert('Passwords do not match.');
            return false;
        }

        return true;
    }

    function validateLoginForm() {
        const email = loginForm.email.value.trim();
        const password = loginForm.password.value.trim();

        if (!validateEmail(email)) {
            alert('Invalid email address.');
            return false;
        }

        if (password.length < 8 || password.length > 30) {
            alert('Password must be between 8 and 30 characters.');
            return false;
        }

        return true;
    }

    function validateEmail(email) {
        const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return re.test(email);
    }

    function filterLessons(keyword) {
        const lessons = lessonList.getElementsByTagName('li');
        Array.from(lessons).forEach(function(lesson) {
            const title = lesson.textContent.toLowerCase();
            if (title.indexOf(keyword) !== -1) {
                lesson.style.display = '';
            } else {
                lesson.style.display = 'none';
            }
        });
    }
});
