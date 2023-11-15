document.getElementById('apiButton1').addEventListener('click', () => callApi("uploads/file.png"));
document.getElementById('apiButton2').addEventListener('click', () => callApi(2));
document.getElementById('apiButton3').addEventListener('click', () => callApi(3));
document.getElementById('uploadButton').addEventListener('click', uploadFile);

function callApi(apiNumber) {
    const fileInput = document.getElementById('fileInput');
    if (fileInput.files.length === 0) {
        alert('Veuillez sélectionner un fichier.');
        return;
    }

    // Afficher le nom du fichier
    document.getElementById('filePathDisplay').innerText = `Fichier sélectionné : ${apiNumber}`;

    fetch(`http://127.0.0.1:5000/use/${apiNumber}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ apiNumber })
    })
    .then(response => response.json())
    .then(data => console.log(data))
    .catch(error => console.error(error));

}

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