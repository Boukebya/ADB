# ADB

## implementation de gpt4 et vertex

Dans les 2 cas, créer une fonction qui prend en entrée le chemin de l'image (ici le chemin est src/uploads/file.png)
Ensuite dans api.py il y'a 2 fonction préfaite, il faut juste mettre votre fonction dans la ligne indiquée avec du coup
en paramètre "file_path" en entrée. Votre output doit être enregistrée dans src/recognized.txt, c'est ce fichier qui
est lu sur le site web. N'hésitez pas à me demander de l'aide si vous avez du mal à lancer l'application.
 
## Previous code analysis

- Need to implement it with the website, the input of the image is just a path right now.

Call OCR function (input is a path), It will concatenate image if needed :
 If concatenation is needed : first get_concat_h, save image.
 Then, use render_doc_text(path_image)

 render_doc_text create client google vision , and use it to detect text, it will create a file "data.txt" with all the detected text by google vision
