document.addEventListener('DOMContentLoaded', (event) => {
    const userMenuButton = document.getElementById('user-menu-button');
    const userDropdown = document.getElementById('user-dropdown');

    userMenuButton.addEventListener('click', () => {
        const isExpanded = userMenuButton.getAttribute('aria-expanded') === 'true';
        userMenuButton.setAttribute('aria-expanded', !isExpanded);
        userDropdown.classList.toggle('hidden');
    });

    document.addEventListener('click', (event) => {
        if (!userMenuButton.contains(event.target) && !userDropdown.contains(event.target)) {
            userMenuButton.setAttribute('aria-expanded', 'false');
            userDropdown.classList.add('hidden');
        }
    });
});
