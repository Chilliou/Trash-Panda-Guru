const searchInput = document.getElementById('search-input');
const resultsContainer = document.getElementById('results-container');

searchInput.addEventListener('keydown', (event) => {
  if (event.key === 'Enter') {
    const searchTerm = searchInput.value;
    fetchSearchResults(searchTerm);
  }
});

async function fetchSearchResults(searchTerm) {
  try {
    const response = await fetch(`http://localhost:3000/api/search?q=${searchTerm}`);
    const results = await response.json();
    displayResults(results);
  } catch (error) {
    console.error('Error fetching search results:', error);
  }
}

function displayResults(results) {
  const resultsContainer = document.getElementById('results-container');
  resultsContainer.innerHTML = ''; // Nettoyer le contenu précédent
  results.forEach(result => {
    const resultElement = document.createElement('div');
    resultElement.textContent = result.siteUrl; // Assurez-vous que "title" correspond à la propriété appropriée dans vos résultats
    resultsContainer.appendChild(resultElement);
  });
}

function displayResults(results) {
  const resultsContainer = document.getElementById('results-container');
  resultsContainer.innerHTML = ''; // Nettoyer le contenu précédent
  results.forEach(result => {
    // Créez un élément de type <div> pour chaque résultat
    const resultElement = document.createElement('div');
    resultElement.classList.add('result-item'); // Ajoutez une classe pour styliser les résultats

    // Créez un lien <a> avec l'URL du résultat comme href
    const linkElement = document.createElement('a');
    linkElement.textContent = result.siteID; // Utilisez le titre comme texte du lien
    linkElement.href = result.siteUrl; // Utilisez l'URL du résultat comme href du lien
    linkElement.target = '_blank'; // Ouvre le lien dans un nouvel onglet
    resultElement.appendChild(linkElement); // Ajoutez le lien à l'élément résultat

    // Ajoutez l'élément résultat à la zone de résultats
    resultsContainer.appendChild(resultElement);
  });
}
