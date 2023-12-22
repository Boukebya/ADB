from customtkinter import *
from PIL import Image
import json
import unidecode
import logging
import csv

logging.basicConfig(filename='historique.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Chargement des images pour les boutons
img_add = Image.open("src/add_icon.png")
img_edit = Image.open("src/edit_icon.png")
img_delete = Image.open("src/delete_icon.png")
img_log = Image.open("src/log_icon.png")
img_export = Image.open("src/export_icon.png")
img_refresh = Image.open("src/refresh_icon.png")

# Configuration du style de l'application
app = CTk()
app.geometry("600x400")
app.title("Gestionnaire d'articles")

# Création du gestionnaire d'onglets
tabview = CTkTabview(master=app)
tabview.pack(fill="both", expand=True, padx=10, pady=10)

# Variables globales pour les messages d'erreur et de succès
done = None
error_none = None
error_already_exists = None

# Widgets pour l'onglet 'Modifier un article'
edit_new_box_name = None
edit_new_box_ref = None
edit_new_validation_button = None
text_1 = None


# def log_view(self):
#     log_file = 'logs/historique.log'  # Nom du fichier log
#     try:
#         with open(log_file, 'r') as f:
#             self.log_display.insert('1.0', f.read())
#     except FileNotFoundError:
#         self.log_display.insert('1.0', 'Aucun log trouvé.')



# Cette fonction permet de récupérer le fichier json et d'en faire un fichier CSV
def export_file():
    global done

    if done is not None:
        done.destroy()
        done = None

    with open("annuaire.json", "r") as f:
        data = json.load(f)

    with open("annuaire.csv", "w", newline='') as f:
        writer = csv.writer(f, delimiter=";")
        for entity in data:
            writer.writerow([entity["reference"], entity["texte"]])

    done = CTkLabel(master=tabview.tab("Ajouter un article"), text="Le fichier a bien été exporté", text_color="green")

    logging.info("Exportation du fichier en CSV")

def import_file():
    global done

    if done is not None:
        done.destroy()
        done = None

    entities = []
    with open("annuaire.csv", "r") as f:
        data = csv.reader(f, delimiter=";")
        for row in data:
            entities.append({"texte": row[1], "reference": row[0]})

    with open("annuaire.json", "w") as f:
        json.dump(entities, f, indent=4)

    done = CTkLabel(master=tabview.tab("Ajouter un article"), text="Le fichier a bien été mis à jour", text_color="green")

    logging.info("Mise à jour du fichier json")



def add_item():
    # Réinitialisation des messages d'erreur et de succès
    global error_none, error_already_exists, done

    # Suppression des messages d'erreur précédents, si présents
    if error_none is not None:
        error_none.destroy()
        error_none = None

    if error_already_exists is not None:
        error_already_exists.destroy()
        error_already_exists = None

    if done is not None:
        done.destroy()
        done = None

    # Vérification des champs de saisie
    if add_entry_name.get() == "" or add_entry_ref.get() == "":
        # Si les champs 'Nom' ou 'Référence' sont vides, affiche un message d'erreur
        if error_none is None:  # Crée le message d'erreur s'il n'existe pas déjà
            error_none = CTkLabel(master=tabview.tab("Ajouter un article"), text="Veuillez remplir les deux champs", text_color="red")
            error_none.pack(padx=20, pady=5)
    else:
        # Si les champs ne sont pas vides
        if error_none is not None:  # Supprime le message d'erreur s'il existe
            error_none.destroy()
            error_none = None

        # Ouverture et lecture du fichier JSON contenant les articles existants
        with open("annuaire.json", "r") as f:
            data = json.load(f)

        # Vérification de l'unicité de la référence de l'article
        for entity in data["entities"]:
            if entity["reference"] == add_entry_ref.get():
                # Si la référence existe déjà, affiche un message d'erreur et arrête la fonction
                if error_already_exists is None:
                    error_already_exists = CTkLabel(master=tabview.tab("Ajouter un article"), text="La référence existe déjà", text_color="red")
                    error_already_exists.pack(padx=20, pady=5)
                return
        # Si la référence n'existe pas, supprime le message d'erreur s'il existe
        if error_already_exists is not None:
            error_already_exists.destroy()
            error_already_exists = None

        # Ajout du nouvel article au fichier JSON
        data["entities"].append({"texte": unidecode.unidecode(add_entry_name.get()), "reference": unidecode.unidecode(add_entry_ref.get())})
        # Enregistrement des modifications dans le fichier JSON
        with open("annuaire.json", "w") as f:
                json.dump(data, f, indent=4)

        # Affichage d'un message de succès pour confirmer l'ajout de l'article
        done = CTkLabel(master=tabview.tab("Ajouter un article"), text="L'article a bien été ajouté", text_color="green")
        done.pack(padx=20, pady=5)

        logging.info(f"Ajout de l'article : Nom={add_entry_name.get()}, Référence={add_entry_ref.get()}")


def clear_edit():
    global edit_new_box_name, edit_new_box_ref, edit_new_validation_button, text_1
    # Nettoyage de l'interface utilisateur après la mise à jour
    text_1.destroy()  # Supprime le texte d'explication
    text_1 = None

    edit_new_box_name.destroy()  # Supprime le champ d'entrée du nouveau nom
    edit_new_box_name = None

    edit_new_box_ref.destroy()  # Supprime le champ d'entrée de la nouvelle référence
    edit_new_box_ref = None

    edit_new_validation_button.destroy()  # Supprime le bouton de validation
    edit_new_validation_button = None


def edit_item_validation():
    # Déclaration des variables globales utilisées dans la fonction
    global error_none, error_already_exists, done, edit_new_box_name, edit_new_box_ref, edit_new_validation_button, text_1

    # Suppression des messages d'erreur et de confirmation existants, s'ils existent
    if error_none is not None:
        error_none.destroy()
        error_none = None

    if error_already_exists is not None:
        error_already_exists.destroy()
        error_already_exists = None

    if done is not None:
        done.destroy()
        done = None

    # Validation des champs de saisie
    if edit_new_box_name.get() == "" and edit_new_box_ref.get() == "":
        # Si aucun champ n'est rempli, afficher un message d'erreur
        if error_none is None:
            error_none = CTkLabel(master=tabview.tab("Modifier un article"), text="Veuillez renseigner au moins un champ", text_color="red")
            error_none.pack(padx=20, pady=5)

    elif edit_new_box_name.get() == "" and edit_new_box_ref.get() != "":
        # Si seul le champ de référence est rempli, mise à jour de la référence de l'article
        with open("annuaire.json", "r") as f:
            data = json.load(f)

        # Parcours des entités pour trouver celle à modifier
        for entity in data["entities"]:
            if entity["reference"] == unidecode.unidecode(edit_entry_ref.get()):
                entity["reference"] = unidecode.unidecode(edit_new_box_ref.get())
                old_name = entity["texte"]
                with open("annuaire.json", "w") as f:
                    json.dump(data, f, indent=4)

                logging.info(f"Modification de l'article : Ancienne Référence={edit_entry_ref.get()}, Ancien Nom={old_name}, Nouveau Nom={edit_new_box_name.get()}, Nouvelle Référence={edit_new_box_ref.get()}")

                # Nettoyage de l'interface utilisateur
                clear_edit()

                # Affichage du message de confirmation
                if error_already_exists is None:
                    error_already_exists = CTkLabel(master=tabview.tab("Modifier un article"), text="L'article a bien été modifié", text_color="green")
                    error_already_exists.pack(padx=20, pady=5)

                return

    elif edit_new_box_name.get() != "" and edit_new_box_ref.get() == "":
        # Ce bloc est exécuté si le champ du nouveau nom est rempli mais pas celui de la nouvelle référence

        with open("annuaire.json", "r") as f:
            # Ouvre le fichier JSON en mode lecture pour charger les données existantes
            data = json.load(f)

        # Parcourt toutes les entités dans les données chargées
        for entity in data["entities"]:
            # Vérifie si la référence actuelle de l'entité correspond à celle saisie par l'utilisateur
            if entity["reference"] == unidecode.unidecode(edit_entry_ref.get()):
                # Si oui, met à jour le nom de l'entité avec la nouvelle valeur saisie par l'utilisateur
                old_name = entity["texte"]
                entity["texte"] = unidecode.unidecode(edit_new_box_name.get())

                with open("annuaire.json", "w") as f:
                    # Sauvegarde les données mises à jour dans le fichier JSON
                    json.dump(data, f, indent=4)

                logging.info(f"Modification de l'article : Ancienne Référence={edit_entry_ref.get()}, Ancien Nom={old_name}, Nouveau Nom={edit_new_box_name.get()}, Nouvelle Référence={edit_new_box_ref.get()}")

                # Nettoyage de l'interface utilisateur après la mise à jour
                clear_edit()

                # Affiche un message de confirmation de la mise à jour
                if error_already_exists is None:
                    error_already_exists = CTkLabel(master=tabview.tab("Modifier un article"),
                                                    text="L'article a bien été modifié", text_color="green")
                    error_already_exists.pack(padx=20, pady=5)

                return  # Quitte la fonction après la mise à jour


    elif edit_new_box_name.get() != "" and edit_new_box_ref.get() != "":
        # Ce bloc est exécuté si l'utilisateur a rempli à la fois le nouveau nom et la nouvelle référence

        with open("annuaire.json", "r") as f:
            # Ouvre le fichier annuaire.json en mode lecture pour charger les données
            data = json.load(f)

        # Parcours des entités dans le fichier JSON
        for entity in data["entities"]:
            # Vérifie si l'entité courante correspond à la référence entrée par l'utilisateur
            if entity["reference"] == unidecode.unidecode(edit_entry_ref.get()):
                # Met à jour le nom et la référence de l'entité avec les nouvelles valeurs saisies
                old_name = entity["texte"]
                entity["texte"] = unidecode.unidecode(edit_new_box_name.get())
                entity["reference"] = unidecode.unidecode(edit_new_box_ref.get())

                with open("annuaire.json", "w") as f:
                    # Sauvegarde les données mises à jour dans le fichier annuaire.json
                    json.dump(data, f, indent=4)

                logging.info(f"Modification de l'article : Ancienne Référence={edit_entry_ref.get()}, Ancien Nom={old_name}, Nouveau Nom={edit_new_box_name.get()}, Nouvelle Référence={edit_new_box_ref.get()}")

                # Nettoyage de l'interface utilisateur après la mise à jour
                clear_edit()

                # Affiche un message de confirmation indiquant que l'article a été modifié avec succès
                if error_already_exists is None:
                    error_already_exists = CTkLabel(master=tabview.tab("Modifier un article"),
                                                    text="L'article a bien été modifié", text_color="green")
                    error_already_exists.pack(padx=20, pady=5)

                return


def edit_item():
    # Déclaration des variables globales utilisées dans la fonction
    global error_none, error_already_exists, done, edit_new_box_name, edit_new_box_ref, edit_new_validation_button, text_1

    # Réinitialisation des messages d'erreur et de succès
    # Ces lignes suppriment les messages d'erreur ou de confirmation précédents s'ils existent
    if error_none is not None:
        error_none.destroy()
        error_none = None

    if error_already_exists is not None:
        error_already_exists.destroy()
        error_already_exists = None

    if done is not None:
        done.destroy()
        done = None

    # Réinitialisation des champs de saisie et des boutons s'ils ont été précédemment créés
    if edit_new_box_name is not None:
        edit_new_box_name.destroy()
        edit_new_box_name = None

    if edit_new_box_ref is not None:
        edit_new_box_ref.destroy()
        edit_new_box_ref = None

    if edit_new_validation_button is not None:
        edit_new_validation_button.destroy()
        edit_new_validation_button = None

    if text_1 is not None:
        text_1.destroy()
        text_1 = None

    # Validation de l'entrée de la référence
    if edit_entry_ref.get() == "":
        # Si le champ de la référence est vide, afficher un message d'erreur
        if error_none is None:
            error_none = CTkLabel(master=tabview.tab("Modifier un article"), text="Veuillez renseigner la référence",
                                  text_color="red")
            error_none.pack(padx=20, pady=5)
    else:
        # Si une référence est entrée, ouvrir et lire le fichier annuaire.json
        with open("annuaire.json", "r") as f:
            data = json.load(f)

        # Recherche de l'article correspondant à la référence
        for entity in data["entities"]:
            if entity["reference"] == unidecode.unidecode(edit_entry_ref.get()):
                # Si l'article est trouvé, créer des champs pour entrer le nouveau nom et/ou la nouvelle référence
                text_1 = CTkLabel(master=tabview.tab("Modifier un article"),
                                  text="Veuillez renseigner le nouveau nom et/ou la nouvelle référence de l'article \n Si vous souhaitez ne modifier qu'un élément sur les deux, laissez l'autre vide",
                                  text_color="white")
                text_1.pack(padx=20, pady=5)

                edit_new_box_name = CTkEntry(master=tabview.tab("Modifier un article"),
                                             placeholder_text="Nouveau nom")
                edit_new_box_name.pack(padx=20, pady=5)

                edit_new_box_ref = CTkEntry(master=tabview.tab("Modifier un article"),
                                             placeholder_text="Nouvelle référence")
                edit_new_box_ref.pack(padx=20, pady=5)

                edit_new_validation_button = CTkButton(master=tabview.tab("Modifier un article"),
                                                       text="Valider",
                                                       command=edit_item_validation)
                edit_new_validation_button.pack(padx=20, pady=5)

                return  # Sortir de la fonction après la création des champs

        # Si la référence entrée n'existe pas, afficher un message d'erreur
        if error_already_exists is None:
            error_already_exists = CTkLabel(master=tabview.tab("Modifier un article"),
                                            text="La référence n'existe pas", text_color="red")
            error_already_exists.pack(padx=20, pady=5)



def delete_item():
    # Déclaration des variables globales pour accéder et modifier les messages d'erreur et de confirmation
    global error_none, error_already_exists, done

    # Suppression des messages d'erreur et de confirmation existants, s'ils existent
    if error_none is not None:
        error_none.destroy()
        error_none = None

    if error_already_exists is not None:
        error_already_exists.destroy()
        error_already_exists = None

    if done is not None:
        done.destroy()
        done = None

    # Vérification si le champ de saisie de la référence est vide
    if delete_entry_ref.get() == "":
        # Si le champ est vide, afficher un message d'erreur
        if error_none is None:  # Crée le label s'il n'existe pas déjà
            error_none = CTkLabel(master=tabview.tab("Supprimer un article"), text="Veuillez remplir le champ",
                                  text_color="red")
            error_none.pack(padx=20, pady=5)
    else:
        # Si le champ de référence n'est pas vide
        if error_none is not None:  # Détruit le label d'erreur s'il existe
            error_none.destroy()
            error_none = None  # Réinitialise la variable error_none

        # Ouvre le fichier JSON contenant les données de l'annuaire
        with open("annuaire.json", "r") as f:
            data = json.load(f)

        # Parcours les entités pour chercher celle à supprimer
        for entity in data["entities"]:
            if entity["reference"] == delete_entry_ref.get():
                # Si l'entité est trouvée, affiche un message de succès
                if error_already_exists is None:
                    error_already_exists = CTkLabel(master=tabview.tab("Supprimer un article"),
                                                    text="Article supprimé avec succès", text_color="green")
                    error_already_exists.pack(padx=20, pady=5)
                    logging.info(f"Suppression de l'article : Référence={delete_entry_ref.get()}")
                    # Supprime l'entité de la liste
                    data["entities"].remove(entity)
                    # Sauvegarde les données mises à jour dans le fichier JSON
                    with open("annuaire.json", "w") as f:
                        json.dump(data, f, indent=4)
                return  # Sort de la fonction après la suppression

        # Si la référence n'est pas trouvée dans le fichier JSON, affiche un message d'erreur
        if error_already_exists is not None:
            error_already_exists.destroy()
            error_already_exists = None

        done = CTkLabel(master=tabview.tab("Supprimer un article"), text="La référence n'existe pas", text_color="red")
        done.pack(padx=20, pady=5)



# Ajout des onglets au Tabview
tabview.add("Ajouter un article")
tabview.add("Modifier un article")
tabview.add("Supprimer un article")



# # accès à l'historique des modifications
# log_btn = CTkButton(master=app, text="Historique des modifications", image=CTkImage(dark_image=img_log, light_image=img_log), command=log_view)
# log_btn.pack(padx=20, pady=5)


# Création d'un frame pour centrer les boutons
center_frame = CTkFrame(master=app)
center_frame.pack(expand=True)

# Bouton d'exportation
export_btn = CTkButton(master=center_frame, text="exporter le fichier en CSV", image=CTkImage(dark_image=img_export, light_image=img_export), command=export_file)
export_btn.pack(side="left", padx=10, pady=10, expand=True)

# Bouton d'importation
import_btn = CTkButton(master=center_frame, text="mettre à jour le fichier", image=CTkImage(dark_image=img_refresh, light_image=img_refresh), command=import_file)
import_btn.pack(side="left", padx=10, pady=10, expand=True)



# Configuration des widgets pour l'onglet 'Ajouter un article'
label_1 = CTkLabel(master=tabview.tab("Ajouter un article"), text="Ajout d'un article")
label_1.pack(padx=20, pady=5)

add_entry_name = CTkEntry(master=tabview.tab("Ajouter un article"), placeholder_text="Nom de l'article")
add_entry_name.pack(padx=20, pady=5)

add_entry_ref = CTkEntry(master=tabview.tab("Ajouter un article"), placeholder_text="Référence de l'article")
add_entry_ref.pack(padx=20, pady=5)

add_btn_submit = CTkButton(master=tabview.tab("Ajouter un article"), text="Ajouter un article", image=CTkImage(dark_image=img_add, light_image=img_add), command=add_item)
add_btn_submit.pack(padx=20, pady=5)






# Configuration des widgets pour l'onglet 'Modifier un article'
label_2 = CTkLabel(master=tabview.tab("Modifier un article"), text="Entrez la référence de l'article à modifier")
label_2.pack(padx=20, pady=5)

edit_entry_ref = CTkEntry(master=tabview.tab("Modifier un article"), placeholder_text="Référence de l'article")
edit_entry_ref.pack(padx=20, pady=5)

edit_btn_submit = CTkButton(master=tabview.tab("Modifier un article"), text="vérifier", command=edit_item)
edit_btn_submit.pack(padx=20, pady=5)





# Configuration des widgets pour l'onglet 'Supprimer un article'
label_3 = CTkLabel(master=tabview.tab("Supprimer un article"), text="Supprimer un article")
label_3.pack(padx=20, pady=5)

delete_entry_ref = CTkEntry(master=tabview.tab("Supprimer un article"), placeholder_text="Référence de l'article")
delete_entry_ref.pack(padx=20, pady=5)

delete_btn_submit = CTkButton(master=tabview.tab("Supprimer un article"), text="Supprimer un article", image=CTkImage(dark_image=img_delete, light_image=img_delete), command=delete_item)
delete_btn_submit.pack(padx=20, pady=5)






# Boucle principale de l'application
app.mainloop()