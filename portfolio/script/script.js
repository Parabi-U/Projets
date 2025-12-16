document.addEventListener('DOMContentLoaded', function() {
    
    const darkBtn = document.getElementById('Dark');
    if (darkBtn) {
        if (localStorage.getItem('darkMode') === 'on') {
            document.body.classList.add('dark');
        }

    darkBtn.addEventListener('click', () => {
        document.body.classList.toggle('dark');
        localStorage.setItem('darkMode',
            document.body.classList.contains('dark') ? 'on' : 'off');
    });
}
    
    const contactBtn = document.getElementById('Contact');
    if (contactBtn) {
        contactBtn.addEventListener('click', function() {
            window.location.href = "Contact.html";
        });
    }

    const form = document.querySelector('form');
    if (form) {
        form.addEventListener('submit', e => {
            const mail = document.getElementById('mail');
            const tel  = document.getElementById('Télephone');
            mail.setCustomValidity('');
            tel.setCustomValidity('');
            let valide = true;
            if (!mail.checkValidity()) {
                mail.setCustomValidity('E-mail invalide');
                valide = false;
            }
            if (!tel.checkValidity()) {
                tel.setCustomValidity('Numéro invalide');
                valide = false;
            }
            if (!valide) {
                e.preventDefault();
                form.reportValidity();
            }
        });
    }
    
    const retourBtn = document.getElementById('Retour');
    if (retourBtn) {
        retourBtn.addEventListener('click', function() {
            window.location.href = "index.html";
        });
    }

    
    const levels = {         
    HTML: 90,
    CSS: 95,
    JavaScript: 70,
    Bootstrap: 80,
    C: 80,
    Assembleur: 65
    };

    const bar      = document.getElementById('skillBar');
    const barInner = bar?.querySelector('.skill-bar-inner');
    const barText  = bar?.querySelector('.skill-bar-text');

    document.querySelectorAll('.skill-tag').forEach(tag => {
    tag.addEventListener('mouseenter', () => {
        const lvl = levels[tag.dataset.skill] || 0;
        barInner.style.width = lvl + '%';
        barText.textContent  = lvl + ' %';
        bar.classList.remove('d-none');
    });
    tag.addEventListener('mouseleave', () => bar.classList.add('d-none'));
    });
    
    const propBtn = document.getElementById('prop');
    if (propBtn) {
        propBtn.addEventListener('click', function() {
            const accordion = document.getElementById('accordionExample');
            if (accordion) {
                accordion.scrollIntoView({ 
                    behavior: 'smooth'  
                });
            }
        });
    }

    
});