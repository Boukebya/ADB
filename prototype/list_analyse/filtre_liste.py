import sys
from pathlib import Path
sys.path.append(str(Path.cwd())+'\project_env\Lib\site-packages')
import re
import unidecode
from os import listdir
from os.path import isfile, join
import json

#algorithm of levenstein to compare the proximity of two words
def levenshtein(mot1,mot2): #code plus rapide
    ligne_i = [ k for k in range(len(mot1)+1) ]
    for i in range(1, len(mot2) + 1):
        ligne_prec = ligne_i
        ligne_i = [i]*(len(mot1)+1)
        for k in range(1,len(ligne_i)):
            cout = int(mot1[k-1] != mot2[i-1])
            ligne_i[k] = min(ligne_i[k-1] + 1, ligne_prec[k] + 1, ligne_prec[k-1] + cout)
    return ligne_i[len(mot1)]/min(len(mot1),len(mot2))

#load the whitelist defined with the database and remove all the non string word
def set_whitelist():
    f = open(r'list_analyse/white_liste.json',encoding="utf8")#whitelist de la BDD
    whitelist = json.load(f)
    whitelist = set(whitelist)
    new_whitelist = []
    for mot in whitelist:
        try:
            val = int(mot)
            continue
        except ValueError:
            if(type(mot)!=float):
                new_whitelist.append(mot)
    return new_whitelist

## use of regex to reformat some expression to compare easily with the bdd

def clean(data):
    data=data.lower() #everything in lowercase
    data=unidecode.unidecode(data) #for weird character "° ..."
    data=re.sub(r"5 *x *5",r"petitcarreau",data) #synonymous
    data=re.sub(r"([0-9]{2})(,[0-9])* *[\*x] *([0-9]{2})(,[0-9])*( *cm)*",r"\1\2x\3\4cm ", data)#format every type of ex(21*29,7)
    data=re.sub(r"\* ([0-9])",r"\1", data)#remove the "*" of a quantity exemple (* 9 cahiers)
    data=re.sub(r"([a-z])s\b",r"\1 ", data) #remove s at the end of words
    data=re.sub(r"ux","u ", data) #remove x at the end of words
    data=re.sub(r" cm\b","cm", data) #stick the cm with the previous word (6 cm -> 6cm)
    data=re.sub(r" mm\b","mm", data)
    data=re.sub(r" m\b","m ", data)
    data=re.sub(r"epaisseur","", data)#useless word in the list
    data=re.sub(r" rond","rond ", data)
    data=re.sub(r" top file + ","topfile+ ", data)#standardize the format
    data = re.sub(r" top file + ","topfile+ ", data)#standardize the format
    data=re.sub(r"couvre livre",r"couvre-livre",data)#standardize the format
    data=re.sub(r"protege ",r"protege-",data)#standardize the format
    data=re.sub(r" : ","", data)#"":" is useless
    data=re.sub(r" g\b","g", data)#for grams (300g)
    data=re.sub(r" \bcouverture","", data) #useless word
    #data=re.sub(r" format","", data)
    data=re.sub(r"[ldscj]\'","",data)#remove the apostrophe
    data=re.sub(r"\t"," ",data) #for the pdf formats
    data=re.sub(r"([a-zA-Z]),([a-zA-Z0-9])",r"\1 \2", data)#replace the coma with a space when they are stick with words
    #data=re.sub(r"\n"," ", data)
    data=re.sub(r'millimetre?',"mm",data)
    data=re.sub(r'centimetre?',"cm",data)
    data=re.sub('plu',"+",data)#standardize + (plus)
    data=re.sub("porte bloc","porte-bloc",data)#standardize
    data=re.sub(' et '," + ",data)#standardize + (plus)
    data=re.sub(r"([0-9]) (page)",r"\1\2", data)#stick the number of page together to have only one word to process
    data=re.sub(r"([0-9]) (vue)",r"\1\2", data)#stick the number of vue together to have only one word to process
    data=re.sub(r"([0-9]) (feuille)",r"\1\2", data)#stick the number of feuille together to have only one word to process
    data=re.sub(r"feuille  double",r" copiedouble",data)#standadize
    data=re.sub(r"feuille  simple",r" copiesimple",data)#standadize
    data=re.sub(r"copie  double",r" copiedouble",data)#standadize
    data=re.sub(r"copie  simple",r" copiesimple",data)#standadize
    #data=re.sub(r"([0-9]) (copie)",r"\1\2", data)
    data=re.sub(r"surligneur","stabilo",data)#synonymous
    data=re.sub(r"piqure","cahier",data)#synonymous
    data=re.sub(r"spirale","reliure",data)#synonymous
    data=re.sub(r"peinture","gouache",data) #synonymous
    data=re.sub(r"chemise","pochette", data) #synonymous
    data=re.sub(r"fourre-tout","trousse", data)#synonymous
    data=re.sub(r"porte[- ]vue","protege-document",data)#synonymous (porte vue or porte-vue)
    data=re.sub(r"feuillet*  mobile",r" copiesimple",data)#synonymous
    data=re.sub(r"carton a dessin",r"sacoche dessin",data)#synonymous
    data=re.sub(r"seye",r"grandcarreau",data)#synonymous
    data=re.sub(r"petit  carreau",r"petitcarreau",data)#standardization
    data=re.sub(r"feutre velleda","marqueur velleda",data)#synonymous
    data=re.sub(r"grand  carreau",r"grandcarreau",data)#standardization
    data=re.sub(r"crayon a papier",r"crayon graphite",data)#synonymous
    data=re.sub(r"crayon gris",r"crayon graphite",data)#synonymous
    data=re.sub(r"grand format",r"",data)
    
    return data

#split the full list in a list of phrase and a list of word in each phrase
def spliter(char):
    splited_word = []
    phrases= char.split("\n")
    for phrase in phrases:
        if phrase == "":
            continue
        else :
            splited_word.append(phrase.split(" "))
    return splited_word

# we are removing the most common use useless word 
# (to gain in performance avoiding to compare those word to the full whitelist)

dicto_blacklist = {
    "a": "",
    "fermeture": "",
    "par": "", 
    "de": "",
    "en": "",
    "liste":"",
    "ce": "",
    "avec":"",
    "et":"",
    "pour":"",
    "la": "",
    "le": "",
    "les": "",
    "est":"",
    'dans':"",
    r'aux?':"",
    
    
}
dicto_whitelist = {
    
    
}

def filter_dicto(df, dic):
    t=[]
    for w in df:
        if w not in dic.keys():
            t.append(w)
    return t

#foor each word of the list check :
# 1) if the word is a int keep it
# 2) if this is a space skip it
# 3) if the word is in the blacklist skip
# 4) if the word is in the whitelist keep it
# 5) if the word is very close to a word of the whitelist (check with levenshtein) keep it
# 6) else skip the word
#if the number of word per phrase is 1 we remove it
#
def filter_the_list(seuil_leven,phraseListe,whitelist,blacklist,seuil_nombre_mot_cle):
    filtered_list = []
    for phrase in phraseListe:
        filtered_phrase = []
        n_mot_phrase = len(phrase)
        n_mot_cle = 0
        for mot in phrase:
            try:#permet de check si le string est un nombre qu'on va garder
                
                val = int(mot)
                filtered_phrase.append(val)
                n_mot_cle+=1
                continue
            except ValueError:
                pass 
            if(mot == ''):
                n_mot_phrase -=1
                continue
            if(mot in blacklist):#filtrer la liste des mots les plus courants.
                continue
            if mot in whitelist:
                filtered_phrase.append(mot)
                n_mot_cle+=1
                continue
            for mot2 in whitelist:
                if(mot[0] != mot2[0]):
                    continue
                if (len(mot2)>1 and len(mot)>1 and mot[1] != mot2[1]): #optimization to not go in levenstein if the beginnig of the two word are differents
                    continue
                leven = levenshtein(mot,mot2)
                if(leven > seuil_leven):
                    continue
                filtered_phrase.append(mot2)#we keep the word of the whitelist not the one in the list (standardization)
                n_mot_cle+=1
                break
            
        if(len(filtered_phrase)<=1):
            continue
        if(n_mot_cle/n_mot_phrase>seuil_nombre_mot_cle):#we want to remove the phrase that are not a list of fournitures 
            #(some part of the list could be explanation given by the college )
            filtered_list.append(filtered_phrase)   
    return filtered_list


def filter_list():
    file = str(Path.cwd())+r"/data.txt"
    data = ''
    with open(file,encoding="utf8") as f:
        line = f.readline()
        while line:
            line = f.readline()
            data+=line
    # read the liste from the save file (by the OCR)

    liste2 = clean(data)
    liste = spliter(liste2)
    SEUIL = 0.3
    new_whitelist = set_whitelist()
    filtered_list = filter_the_list(SEUIL,liste[:1000],new_whitelist,dicto_blacklist,0.3)
    # filter the list

    jsonString = json.dumps(filtered_list) 
    with open('list_analyse\liste_filtered.json', 'w') as f:
        f.write(jsonString)
    #save it as a json file