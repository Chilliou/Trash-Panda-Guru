// Tableau avec les chemins d'accès aux images
const raccoonImages = [
    'images/raccoon-background.jpg',
    'images/raccoon-background2.jpg',
    'images/raccoon-background3.jpg',
    'images/raccoon-background4.jpg',
    'images/raccoon-background5.jpg',
    // Ajoutez ici les autres chemins d'accès
];

// Fonction pour changer l'image de fond de manière aléatoire
function changeBackgroundImage() {
    const backgroundImageDiv = document.getElementById('background-image');
    const randomIndex = Math.floor(Math.random() * raccoonImages.length);
    const randomImageSrc = raccoonImages[randomIndex];
    backgroundImageDiv.style.backgroundImage = `url(${randomImageSrc})`;
}

// Changez l'image de fond au chargement de la page
window.onload = changeBackgroundImage;

// Changez l'image de fond toutes les 5 secondes (vous pouvez ajuster l'intervalle)
setInterval(changeBackgroundImage, 5000);