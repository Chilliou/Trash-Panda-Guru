const express = require('express');
const app = express();
const mysql = require('mysql');
const path = require('path');
const cors = require('cors'); // Importez le module CORS

app.use(express.static(path.join(__dirname, '../public')));

// Connexion à la base de données MySQL
const connection = mysql.createConnection({
  host: 'localhost',
  user: 'root',
  password: 'YourRootPassword',
  database: 'gogoRaccoon',
  port: 4448
});

connection.connect((err) => {
  if (err) throw err;
  console.log('Connected to MySQL database');
});

// Utilisez le middleware CORS pour gérer les autorisations CORS
app.use(cors());

// Route API pour la recherche
app.get('/api/search', (req, res) => {
  const searchTerm = req.query.q;
  const query = `SELECT si.siteID, si.siteUrl FROM SiteMots s join Mots m on m.motID=s.motID join Site si on si.siteID=s.siteID WHERE m.mot LIKE '%${searchTerm}%' order by s.tfidf limit 10`;

  console.log('Recherche pour :', searchTerm);

  connection.query(query, (err, results) => {
    if (err) {
      console.error('Erreur lors de la requête SQL :', err);
      throw err;
    }

    console.log('Résultats :', results);
    res.json(results);
  });
});

app.listen(3000, () => {
  console.log('Server is running on port 3000');
});
