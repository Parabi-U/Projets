document.getElementById('Accueil').addEventListener('click', function() {
    document.getElementById('Accueil').scrollIntoView({ 
        behavior: 'smooth'  
    });
});

document.getElementById('Contact').addEventListener('click', function() {
    window.location.href ="Contact.html"
    });

document.getElementById('Retour').addEventListener('click', function() {
    window.location.href ="index.html"
    });

document.getElementById('prop').addEventListener('click', function() {
    document.getElementById('accordionExample').scrollIntoView({ 
        behavior: 'smooth'  
    });
});