import json
import pandas as pd
import re
import unidecode
data = pd.read_excel('Mini Catalogue V2.xlsx',
                     skiprows=1).reset_index(drop=True)
L = 312
print(data["Désignation"][L])
print(data["N°"][L])

# clean the bdd function


def clean(data):

    data = data.lower()  # lower caracter
    data = unidecode.unidecode(data)

    data = re.sub(r"(ndeg) *", r"\1", data)
    data = re.sub(r"22,100", r"22, 100", data)  # pour la ref 03163U20

    data = re.sub(r"quadrille", r"", data)
    data = re.sub(r"normalise", r"", data)
    data = re.sub(r"5 *x *5", r"petitcarreau", data)
    data = re.sub(r"carton a dessin", r"sacoche dessin", data)
    data = re.sub(
        r"([0-9]{2})(,[0-9])* *[\*x] *([0-9]{2})(,[0-9])*( *cm)*", r"\1\2x\3\4cm ", data)

    data = re.sub(r" *x ", "x", data)
    data = re.sub(r"ux", "ux ", data)

    data = re.sub(r" cm", "cm", data)
    data = re.sub(r" mm", "mm", data)
    data = re.sub(r" m\b", "m ", data)
    # we remove the "s" at the end of the word
    data = re.sub(r"([a-z])s\b", r"\1 ", data)
    data = re.sub(r"epaisseur", "", data)
    data = re.sub(r" rond", " rond ", data)
    data = re.sub(r"porte bloc", "porte-bloc ", data)
    data = re.sub(r" porte bloc ", " porte-bloc ", data)

    data = re.sub(r" top file *\+ ", " topfile+ ", data)
    data = re.sub(r" - ", r" ", data)
    data = re.sub(r" *:( *)", r"\1", data)
    data = re.sub(r" *\.( *)", r"\1", data)
    data = re.sub(r" *[(]( *)", r" \1", data)
    data = re.sub(r" *[)]( *)", r"\1", data)

    data = re.sub(r"[ldscj]\'", " ", data)

    data = re.sub(r" g\b", "g", data)

    data = re.sub(r" \bcouverture", "", data)
    data = re.sub(r" format", "", data)
    data = re.sub(r"([a-z]),([a-z0-9])", r"\1 \2", data)
    data = re.sub(r", ", " ", data)

    data = re.sub(r"marqueur permanent indelebile",
                  r"marqueur permanent", data)
    data = re.sub(r"stylo bille bic", r"stylo bic", data)
    data = re.sub(r"stylo bille", r"stylo bic", data)
    data = re.sub(r"roller effacable", r"feutre effacable", data)
    data = re.sub(r"machine a calculer", r"calculatrice", data)
    data = re.sub(r"rouleau adhesif scotch", r"scotch", data)
    data = re.sub(r"couvre livre", r"couvre-livre", data)
    data = re.sub(r"rouleau adhesif", r"scotch", data)
    data = re.sub(r"dessin c", r"papier canson", data)
    data = re.sub(r"feutre effacable sec",
                  r"marqueur effacable sec Velleda", data)
    data = re.sub(r" page", "page", data)
    data = re.sub(r"piqure", "cahier", data)
    data = re.sub(r"noir,", "noir", data)
    data = re.sub(r"surligneur", "stabilo", data)
    data = re.sub(r"integrale", "", data)
    data = re.sub(r"spirale", "reliure", data)
    data = re.sub(r"peinture", "gouache", data)
    data = re.sub(r"chemise", "pochette", data)
    data = re.sub(r"fourre-tout", "trousse", data)
    data = re.sub(r"protege ", r"protege-", data)

    data = re.sub(r"([0-9]) (vue)", r"\1\2", data)
    data = re.sub(r"([0-9]) (feuille)", r"\1\2", data)
    data = re.sub(r"copie  double", r" copiedouble", data)
    data = re.sub(r"copie  simple", r" copiesimple", data)
    data = re.sub(r"feuille  double", r" copiedouble", data)
    data = re.sub(r"feuille  simple", r" copiesimple", data)
    data = re.sub(r"feuillet  mobile", r" copiesimple", data)
    data = re.sub(r"seye", r"grandcarreau", data)

    return data

# split the BDD


def spliter(char):
    char = char.split(" ")
    return char


df = pd.DataFrame(data=data["Désignation"])
df2 = pd.DataFrame(data=data[["N°", "Code catégorie"]])
df["Désignation"] = df["Désignation"].apply(clean)
df["Désignation"] = df["Désignation"].apply(spliter)

# little dictionnary to filter
dicto = {
    "a": "",
    "6eme": "",
    "5eme": "",
    "4eme": "",
    "3eme": "",
    'sixieme': "",
    'troisieme': "",
    'cinquieme': "",
    'quatrieme': "",
    "fermeture": "",
    "par": "",
    "de": "",
    "en": "",
    "ce": "",
    "avec": "",
    "et": "",
    "pour": "",
    "la": "",
    "do": "",
}

# function to execute the filter dicto


def filter_dicto(df, dic):
    t = []
    for w in df:
        if w != "":
            if w not in dic.keys():
                t.append(w)

    return t


df["Désignation"] = df["Désignation"].apply(filter_dicto, dic=dicto)

df3 = pd.concat([df["Désignation"], df2], axis=1)
df3 = df3.dropna(axis=0)

df3.to_csv('Liste.csv', index=False)
a = pd.read_csv('Liste.csv')

df_list = list(df["Désignation"].explode().unique())


jsonString = json.dumps(df_list)
with open('white_liste.json', 'w') as f:
    f.write(jsonString)
