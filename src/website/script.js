// Appel des fonctions de l'API Flask
document.getElementById('apiButton2').addEventListener('click', () => call_vertex("src/website/uploads/file.jpg","toutes classes"));
// Appel de la fonction pour enregistrer l'image dans le serveur
document.getElementById('uploadButton').addEventListener('click', uploadFile);


//afficher la tab OCR par défaut
document.getElementById("defaultOpen").click();

// Fonction pour afficher les tabs
function openTab(evt, tabName) {

  var i, tabcontent, tablinks;
  tabcontent = document.getElementsByClassName("tabcontent");
  // Hide tabs
  for (i = 0; i < tabcontent.length; i++) {
    tabcontent[i].style.display = "none";
  }
  tablinks = document.getElementsByClassName("tablinks");
  // Remove active class
  for (i = 0; i < tablinks.length; i++) {
    tablinks[i].className = tablinks[i].className.replace(" active", "");
  }
  // Show tab
  document.getElementById(tabName).style.display = "block";
  evt.currentTarget.className += " active";
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


// Fonction pour appeler l'API pour utiliser Vertex
function call_vertex(path, classe) {
fetch(`http://127.0.0.1:5000/use_vertex/${path}/${classe}`, {
    method: 'GET'
})
    .then(response => response.json())
    .then(data => {
        console.log(data);
        document.getElementById('time').innerHTML = data.execution_time;
        document.getElementById('result').innerHTML = data.content_ocr;
        document.getElementById('result_extraction').innerHTML = data.result_extraction;
        document.getElementById('result_matching').innerHTML = data.matching;

    })
    .catch(error => {
        console.error(error);
        console.log("Erreur lors de l'appel de l'API (script.js)");
    });
}