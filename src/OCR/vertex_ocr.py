import json

from google.api_core.client_options import ClientOptions
from google.cloud import documentai_v1 as documentai
from google.oauth2 import service_account
from PIL import Image

with open('src/config.json', 'r') as config_file:
    config = json.load(config_file)

google_var = config['google_cloud']

google_project_id = google_var['project_id']
google_location = google_var['location']
google_processor = google_var['processor']


def vertex_ocr(file_path):
    """
    Fonction qui prend en paramètre le chemin d'un fichier image et qui retourne le texte contenu dans l'image
    en utilisant l'API de Google Document AI, le texte est écrit dans un fichier texte nommé ocr.txt
    :param file_path: Chemin du fichier image
    """


    # Spécifiez le chemin vers votre fichier de clés de compte de service
    json_credentials_path = "src/google.json"

    # Chargez explicitement les informations d'identification à partir du fichier JSON
    credentials = service_account.Credentials.from_service_account_file(json_credentials_path)


    # Initialise les options client avec l'endpoint et les informations d'identification
    opts = ClientOptions(api_endpoint=f"{google_location}-documentai.googleapis.com")
    client = documentai.DocumentProcessorServiceClient(client_options=opts, credentials=credentials)

    # Chemin d'accès complet pour le processeur de documents
    name = client.processor_path(google_project_id, google_location, google_processor)

    # if file_path is an array, concatenate images
    if type(file_path) == list:
        with open("concatenated_image.jpg", "wb") as f:
            for image in file_path:
                with open(image, "rb") as img:
                    f.write(img.read())
        file_path = "concatenated_image.jpg"

    with open(file_path, "rb") as image:
        image_content = image.read()

    # Déterminez le type MIME en fonction de l'extension du fichier
    if file_path.endswith('.jpg') or file_path.endswith('.jpeg'):
        mime_type = "image/jpeg"
    elif file_path.endswith('.png'):
        mime_type = "image/png"
    # Ajoutez d'autres formats d'image si nécessaire
    else:
        raise ValueError("Format de fichier non pris en charge")

    raw_document = documentai.RawDocument(
        content=image_content,
        mime_type=mime_type
    )


    # Préparez la requête pour le traitement du document
    request = documentai.ProcessRequest(name=name, raw_document=raw_document)

    # Appelez l'API Document AI pour traiter le document
    result = client.process_document(request=request)

    # Le document traité est maintenant dans `result.document`
    document = result.document

    # Affichez le texte extrait du document
    print("The document contains the following text:")
    print(document.text)

    # Enregistrez le texte extrait dans un fichier
    with open("ocr.txt", "w", encoding="utf-8") as f:
        f.write(document.text)


def concat_images(image_path1, image_path2, output_path):
    # Ouvrir les images
    image1 = Image.open(image_path1)
    image2 = Image.open(image_path2)

    # Calculer les dimensions pour la nouvelle image
    width = image1.width + image2.width
    height = max(image1.height, image2.height)

    # Créer une nouvelle image avec les dimensions appropriées
    new_image = Image.new('RGB', (width, height))

    # Coller les images dans la nouvelle image
    new_image.paste(image1, (0, 0))
    new_image.paste(image2, (image1.width, 0))

    # Enregistrer la nouvelle image
    new_image.save(output_path)