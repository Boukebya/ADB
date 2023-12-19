# ADB

## Content
<details>

<summary>
click to expand

</summary>

 - [Installation](#installation)
 - [OCR](#ocr)
 - [Extraction](#extraction)
 - [Matching](#matching)
 - [Statistics](#statistics)
 - [Tools](#tools)
 - [Code](#code)
 - [Diagram](#diagram)

</details>


# <a id="installation" />Installation

## Create vertex account

Prerequisites

Before you can use Document AI, you need to make sure that you have a Google Cloud Platform project, the Document AI API enabled, a document processor created, and service account credentials downloaded.

Instructions

- Create a Google Cloud Platform project. To do this, go to the Google Cloud Console and click on the "Créer un projet" button.

- Enable the Document AI API. To do this, go to the "APIs & Services" page of the Google Cloud Console and search for Document AI. Click on the "Enable" button.

- Create a document processor. To do this, go to the "Processeurs de documents" page of the Google Cloud Console and click on the "Créer un processeur button".

- Download the service account credentials. To do this, go to the "Clés d'API" page of the Google Cloud Console and click on the "Créer une clé" button. Select "Clé JSON" and click on "Créer".

You can find more details and the links to directly do this tasks in the following tutorials :

- Set up the Document AI API : https://cloud.google.com/document-ai/docs/setup
- Use Enterprise Document OCR to process documents : https://cloud.google.com/document-ai/docs/process-documents-ocr



## Create OpenAI account

- Create an account on OpenAI website
- Create an API key in API keys section of your account
- Copy the API key and paste it in the following file : "src/config.json" in openai, api_key field

Manage the funds of your account in the billing section of your account, a minimal amount of 5$ is required to use the API.

## init project

Clone project and install dependencies
```bash
git clone https://github.com/Boukebya/ADB.git
cd adb
pip install -r requirements.txt
```
After that, you should be able to run the following command without any error
```bash
python src/api.py
```
If the API is running, then you can call it using it's path :
http://127.0.0.1:5000/use_vertex/${path_img}



# <a id="ocr" />OCR

OCR is the process of converting images of text into machine-encoded text.
To convert our supply list image into text, we use the OCR API of google, google vision, which is a google cloud service.
It is important to change config file with your own google vision api key.
When using the API, the image will be transfered to google cloud, and the result will be returned as a json file in "ocr.txt"

# <a id="extraction" />Extraction

Extraction is the process of extracting the information from the text, basically, we want to extract the name of the product,
the quantity and all useful information from the text, like weight, dimensions, etc.
To do that, we use the OpenAI API, which is a cloud service that uses machine learning to extract information from text.
We use GPT-3.5 model, which is a model that is trained on a large dataset of text, and is able to extract information from text.
The result of the extraction is returned as a json file in "ocr.txt"
We can also input "classe", which corresponds to the school level of the supplies that we want to extract.
The output of extraction will be made with the following fields : "name", which is the name of the information 
that we found with all information, "article", which is the name of the product, "quantity", which is the quantity of the product.

# <a id="matching" />Matching

Matching is made by using the extracted information from the text, and matching it with the information in the database, called "annuaire.json".
This database can be modified and contains "texte" and "reference" fields.
We compare our output from extraction with all our products in the database, and we return the product that has the highest score.
The score is calculated by using a similarity function, the levenstein distance, which is a function that calculates the distance between two strings,
and a custom methods that work with points based on the similarity of the words between the two strings.
Some custom methods are also made do determine the good product, for example for books or paper.

# <a id="statistics" />Statistics

Here is a resume of results of the project :
## TODO : add detailled statistics image

# <a id="tools" />Tools

Some tools can still be used to custom the project :
- One interface to modify database
- One methods to preprocess a database

# <a id="code" />Code

# <a id="diagram" />Code diagram


