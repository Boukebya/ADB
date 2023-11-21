from google.api_core.client_options import ClientOptions
from google.cloud import documentai_v1 as documentai
from google.oauth2 import service_account

def vertex_ocr(file_path):
    # Spécifiez le chemin vers votre fichier de clés de compte de service
    json_credentials_path = "/google.json"

    # Chargez explicitement les informations d'identification à partir du fichier JSON
    credentials = service_account.Credentials.from_service_account_file(json_credentials_path)

    # Informations de votre projet et de l'API Document AI
    project_id = "teak-truck-404413"
    location = "eu"  # Format is "us" or "eu"
    processor_id = "6ac5684a8d5752ee"

    # Initialise les options client avec l'endpoint et les informations d'identification
    opts = ClientOptions(api_endpoint=f"{location}-documentai.googleapis.com")
    client = documentai.DocumentProcessorServiceClient(client_options=opts, credentials=credentials)

    # Chemin d'accès complet pour le processeur de documents
    name = client.processor_path(project_id, location, processor_id)

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
    with open("../recognized.txt", "w", encoding="utf-8") as f:
        f.write(document.text)
