import pandas as pd
import re
import nltk
from nltk.corpus import stopwords
from functools import reduce
import json
import random

dict_colors = ["blanc",
               "noir",
               "bleu",
               "vert",
               "jaune",
               "orange",
               "rose",
               "violet",
               "rouge",
               "gris"]



def extract_cahier_info(description, color_list):
    """
    Extract the information from the description of a book product
    :param description: description of the product
    :param color_list: list of colors
    :return: a dictionary containing the information
    """
    dimensions_match = re.search(r'(\d+(\,\d+)?)\s*[xX]\s*(\d+(\,\d+)?)\s*(cm|centimètres|\w+)', description, re.IGNORECASE)
    dimensions = f"{dimensions_match.group(1).replace(',', '.')} x {dimensions_match.group(3).replace(',', '.')} cm" if dimensions_match else None

    pages_match = re.search(r'(\d+)\s*(p\.|p|pages?)', description, re.IGNORECASE)
    number_of_pages = int(pages_match.group(1)) if pages_match else None

    weight_match = re.search(r'(\d+(\.\d+)?)\s*(?!\s*grands?)\s*(g|grammes?)', description)
    weight = float(weight_match.group(1)) if weight_match else None

    # Extract color using the color list
    color = None
    for word in description.split():
        if word.lower() in color_list:
            color = word.lower()
            break

    cover = False
    if("protege" in description):
        cover = True

    return {'desc': description, 'd': dimensions, 'w': weight, 'p': number_of_pages, 'c': color, 'cover': cover}


def extract_paper_info(description, color_list):
    """
    Extract the information from the description of a paper product
    :param description: description of the product
    :param color_list: list of colors
    :return: a dictionary containing the information
    """
    dimensions_match = re.search(r'(\d+(\,\d+)?)\s*[xX]\s*(\d+(\,\d+)?)\s*(cm|centimètres|\w+)', description, re.IGNORECASE)
    dimensions = f"{dimensions_match.group(1).replace(',', '.')} x {dimensions_match.group(3).replace(',', '.')} cm" if dimensions_match else None

    if('a4' in description or "21 x 29.7 cm" == dimensions):
        dimensions = "A4"

    pages_match = re.search(r'(\d+)\s*(p\.|p|pages?)', description, re.IGNORECASE)
    number_of_pages = int(pages_match.group(1)) if pages_match else None

    weight_match = re.search(r'(\d+(\.\d+)?)\s*(?!\s*grands?)\s*(g|grammes?)', description)
    weight = float(weight_match.group(1)) if weight_match else None

    # Extract color using the color list
    color = None
    for word in description.split():
        if word.lower() in color_list:
            color = word.lower()
            break

    double = False
    if("doubl" in description):
        double = True

    perf = False
    if("perf" in description):
        perf = True

    if("non perf" in description):
        perf = False

    draw = False
    if("dessin" in description):
        draw = True

    return {'desc': description, 'd': dimensions, 'w': weight, 'p': number_of_pages, 'c': color, 'double': double, 'perf': perf, 'draw': draw}


def match_paper(product):
    """
    Match a paper product with the catalog
    :param product: product to match
    :return: the corresponding in catalog
    """
    df_paper = pd.read_json("data_paper.json")

    extract = extract_paper_info(product, dict_colors)

    conditions = []

    if extract["d"] is not None:
        conditions.append(df_paper["d"] == extract["d"])

    if extract["w"] is not None:
        conditions.append(df_paper["w"] == extract["w"])

    if extract["p"] is not None:
        conditions.append(df_paper["p"] == extract["p"])

    if extract["c"] is not None:
        conditions.append(df_paper["c"] == extract["c"])

    if extract["double"] is not None:
        conditions.append(df_paper["double"] == extract["double"])

    if extract["perf"] is not None:
        conditions.append(df_paper["perf"] == extract["perf"])

    if extract["draw"] is not None:
        conditions.append(df_paper["draw"] == extract["draw"])

    if conditions:
        corresponding_products = df_paper.loc[reduce(lambda x, y: x & y, conditions)]
    else:
        # Aucune information disponible, peut-être afficher un message ou traiter d'une autre manière
        corresponding_products = None

    # if multiple products match, we take the first one
    if corresponding_products is not None:
        # convert pandas to list
        list = corresponding_products.values.tolist()
        # get a random element from the list
        corresponding_products = random.choice(list)
        return corresponding_products


def match_book(product):
    """
    Match a product with the database
    :param product: product to match
    :return: the corresponding in catalog
    """

    df = pd.read_json('data.json')
    extract = extract_cahier_info(product, dict_colors)

    conditions = []

    if extract["d"] is not None:
        conditions.append(df["d"] == extract["d"])

    if extract["w"] is not None:
        conditions.append(df["w"] == extract["w"])

    if extract["p"] is not None:
        conditions.append(df["p"] == extract["p"])

    if extract["c"] is not None:
        conditions.append(df["c"] == extract["c"])

    if extract["cover"] is not None:
        conditions.append(df["cover"] == extract["cover"])

    if conditions:
        corresponding_products = df.loc[reduce(lambda x, y: x & y, conditions)]
    else:
        # Aucune information disponible, peut-être afficher un message ou traiter d'une autre manière
        corresponding_products = None

    # if multiple products match, we take the first one
    if corresponding_products is not None:
        #convert pandas to list
        list = corresponding_products.values.tolist()
        # get a random element from the list
        corresponding_products = random.choice(list)
        return corresponding_products


product = "cahier a4 96 pages 90g grands carreaux couverture polypro "
# product = "copie simple perforées format  à grands carreaux"
corresponding_products = match_book(product)

# print desc
print(corresponding_products[0])
