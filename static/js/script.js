// Off Screen  Menu 
document.addEventListener('DOMContentLoaded', function() {
    const burgerMenu = document.querySelector('.burger-menu');
    const offScreenMenu = document.querySelector('.off-screen-menu');
    const menuOverlay = document.querySelector('.menu-overlay');

    const toggleMenu = () => {
        offScreenMenu.classList.toggle('active');
        menuOverlay.style.display = offScreenMenu.classList.contains('active') ? 'block' : 'none';
        document.body.style.overflow = offScreenMenu.classList.contains('active') ? 'hidden' : '';
    };

    burgerMenu.addEventListener('click', (e) => {
        e.stopPropagation();
        toggleMenu();
    });

    menuOverlay.addEventListener('click', toggleMenu);
    document.addEventListener('keydown', (e) => e.key === 'Escape' && toggleMenu());
    
    offScreenMenu.querySelectorAll('a').forEach(item => {
        item.addEventListener('click', toggleMenu);
    });
});