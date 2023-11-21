// Appel des fonctions de l'API Flask
document.getElementById('apiButton1').addEventListener('click', () => call_opencv("website/uploads/file.png"));
document.getElementById('apiButton2').addEventListener('click', () => call_vertex("website/uploads/file.png"));
document.getElementById('apiButton3').addEventListener('click', () => call_gpt4("website/uploads/file.png"));
// Appel de la fonction pour enregistrer l'image dans le serveur
document.getElementById('uploadButton').addEventListener('click', uploadFile);
document.getElementById('compare').addEventListener('click',load_compare);


// Fonctions pour appeler l'API pour openCV, Vertex et GPT-4
function call_opencv(path) {
    fetch(`http://127.0.0.1:5000/use_opencv/${path}`, {
        method: 'GET'
    })
    .then(response => response.json())
    .then(data => {
        console.log(data);
        getText(); // Appelle getText() après que la réponse a été traitée avec succès.
        document.getElementById('time').innerHTML = data.execution_time;

    })

    .catch(error => {
        console.error(error);
    });
}

function call_vertex(path) {
fetch(`http://127.0.0.1:5000/use_vertex/${path}`, {
        method: 'GET'
    })
    .then(response => response.json())
    .then(data => {
        console.log(data);
        getText(); // Appelle getText() après que la réponse a été traitée avec succès.
        document.getElementById('time').innerHTML = data.execution_time;

    })
    .catch(error => {
        console.error(error);
    });
}

function call_gpt4(path) {
fetch(`http://127.0.0.1:5000/use_gpt4/${path}`, {
        method: 'GET'
    })
    .then(response => response.json())
    .then(data => {
        console.log(data);
        getText(); // Appelle getText() après que la réponse a été traitée avec succès.
        document.getElementById('time').innerHTML = data.execution_time;
    })
    .catch(error => {
        console.error(error);
    });
}

// Fonction pour récupérer le texte de l'OCR
function getText() {
    console.log("Fonction getText exécutée");
    fetch('http://127.0.0.1:5000/get-text')
    .then(response => {
        console.log("Réponse reçue");
        return response.json(); // Convertit la réponse en JSON
    })
    .then(data => {
    // Remplace les sauts de ligne par des balises <br> pour l'affichage HTML
    const formattedText = data.text.replace(/\n/g, '<br>');
    document.getElementById('result').innerHTML = formattedText;
})
    .catch(error => console.error("Erreur lors de la récupération des données :", error));
}

// Fonction pour télécharger le fichier sur le serveur
function uploadFile() {
    const fileInput = document.getElementById('fileInput');
    if (fileInput.files.length === 0) {
        alert('Veuillez sélectionner un fichier.');
        return;
    }

    const file = fileInput.files[0];
    const formData = new FormData();
    formData.append('file', file);

    fetch('http://127.0.0.1:5000/upload', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        console.log(data);
        alert('Fichier téléchargé avec succès.');
    })
    .catch(error => {
        console.error(error);
        alert('Erreur lors du téléchargement du fichier.');
    });
}

// Fonction pour comparer les résultats
function load_compare() {
    fetch('http://127.0.0.1:5000/compare')
    .then(response => {
        if (!response.ok) {
            throw new Error('Erreur réseau'); // Gère les réponses non-200
        }
        return response.json(); // Convertit la réponse en JSON
    })
    .then(data => {
        // Assurez-vous que "score" est bien une clé dans "data"
        const score = data.score;
        document.getElementById('score').innerHTML = score;
    })
    .catch(error => {
        console.error('Erreur lors de la récupération des données:', error);
        // Gérer l'erreur, par exemple en affichant un message à l'utilisateur
    });
}

