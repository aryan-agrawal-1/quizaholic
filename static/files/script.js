document.addEventListener('DOMContentLoaded', function() {
    const burgerMenu = document.querySelector('.burger-menu');
    const offScreenMenu = document.querySelector('.off-screen-menu');
    const menuOverlay = document.querySelector('.menu-overlay');

    // Simple toggle function
    const toggleMenu = () => {
        offScreenMenu.classList.toggle('active');
        menuOverlay.style.display = offScreenMenu.classList.contains('active') ? 'block' : 'none';
        document.body.style.overflow = offScreenMenu.classList.contains('active') ? 'hidden' : '';
    };

    // Event listeners
    burgerMenu.addEventListener('click', (e) => {
        e.stopPropagation();
        toggleMenu();
    });

    menuOverlay.addEventListener('click', toggleMenu);
    document.addEventListener('keydown', (e) => e.key === 'Escape' && toggleMenu());
    
    // Close menu on any click inside
    offScreenMenu.querySelectorAll('a').forEach(item => {
        item.addEventListener('click', toggleMenu);
    });

});


