import pandas as pd
import json
import numpy as np

#use the jaccard distance algoritm to evaluate the difference between two list of words
def jaccard(phrase1,phrase2):
    return len(list(set(phrase1).intersection(phrase2)))

def custom_read_csv(path):
    df = pd.read_csv(path,on_bad_lines='skip')
    df['Désignation'] = df['Désignation'].apply(custom_tolist)
    return df


def custom_tolist(a): ##remove parentheses in order to be able to save a dataframe containing list
    newstr = a.replace("[\'", "")
    newstr = newstr.replace(" ", "")
    newstr = newstr.replace("\']", "")
    #newstr = newstr.replace("'", "")
    a = newstr.split('\',\'')
    return a

def get_favourite_ref(list_ref,dic_fav_ref): #some categories of school supplies have a prefered reference over the other
    if(len(list_ref)==1):
        return list_ref.iloc[0]
    if list_ref['Code catégorie'].iloc[0] in dic_fav_ref:
        ref = dic_fav_ref[list_ref['Code catégorie'].iloc[0]]
        if ref in list(list_ref["N°"]):
            return ref
    return list_ref.iloc[0]


 # fonction for comparing a phrase of the list with the bdd and keep the best one
def get_best_reference(phrase,df_bdd,dict_pref):
    phrase_2 = phrase.copy() #in order to not modify the "phrase" variable
    seuil = 0.5
    quantite = 1
    best_accuracy = 0
    index_best_ref = [-1]
    if(type(phrase_2[0]) == int): #the first word will often be a quantity
        quantite = phrase_2[0]
        phrase_2.pop(0)
    for i in range(len(df_bdd)): # get the distance between each database designation and the phrase with jaccard
        accuracy = jaccard(df_bdd["Désignation"].iloc[i],phrase_2)
        if(accuracy > best_accuracy): #if we find a best accuracy than the previous one we forget the old one and keep the designation in mind
            best_accuracy = accuracy
            index_best_ref = [i]
        elif ((accuracy > 0) and (accuracy== best_accuracy)):
            index_best_ref.append(i) #keep multiple indexes if they have the same accuracy
    if((best_accuracy)/(len(phrase_2)) <= seuil):
        quantite = 0
    list_ref = df_bdd.iloc[index_best_ref]
    get_favourite_ref(list_ref,dict_pref)#to choose the best index between multiple reference
    return (quantite,df_bdd.iloc[index_best_ref[0]])


def panier_excel():
    # Database of school supplies
    df_bdd = custom_read_csv(r"list_analyse\Liste.csv")

    # Output of image processing
    f = open(r"list_analyse\liste_filtered.json",encoding="utf8")
    liste_filtered = json.load(f)

    # ref and code of the prefered reference for each category
    list_result = []
    dict_pref = pd.read_excel('list_analyse\code_prio.xlsx', skiprows=0).reset_index(drop=True)

    # For each element in liste_filtered, we get the best reference
    for phrase in liste_filtered:
        (qt,ref) = get_best_reference(phrase,df_bdd,dict_pref)
        list_result.append((qt,ref["N°"],ref["Désignation"],ref["Page scolaire"]))

    # Create a dataframe with the result and save it in an excel file
    out_df = pd.DataFrame(np.array(list_result),columns=['quantite','reference','designation','page-scolaire'])
    out_df.to_excel('output.xlsx', index = False)