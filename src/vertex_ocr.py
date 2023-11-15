from google.api_core.client_options import ClientOptions
from google.cloud import documentai_v1 as documentai  # type: ignore

# TODO(developer): Uncomment these variables before running the sample.
project_id = "composed-hash-404414"
location = "eu"  # Format is "us" or "eu"
file_path = r"C:\Users\Jadid Harith\Desktop\Junia 5th year\Projet YES\600705 listes fournitures tous niveaux.pdf"
processor_display_name = "Autour du bureau" # Must be unique per project, e.g.: "My Processor"
processor_id = "c7d6213d975ce92a"


opts = ClientOptions(api_endpoint=f"{location}-documentai.googleapis.com")

client = documentai.DocumentProcessorServiceClient(client_options=opts)

name = client.processor_path(project_id, location, processor_id)

with open(file_path, "rb") as image:
    image_content = image.read()

raw_document = documentai.RawDocument(
    content=image_content,
    mime_type="application/pdf",  # Refer to https://cloud.google.com/document-ai/docs/file-types for supported file types
)

request = documentai.ProcessRequest(name=name, raw_document=raw_document)

result = client.process_document(request)

document= result.document
# %%
# Read the text recognition output from the processor
print("The document contains the following text:")
print(document.text)

#save in a txt file
with open("recognized.txt", "w", encoding="utf-8") as f:
    f.write(document.text)