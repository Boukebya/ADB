# ADB
 
## Previous code analysis

- Need to implement it with the website, the input of the image is just a path right now.

Call OCR function (input is a path), It will concatenate image if needed :
 If concatenation is needed : first get_concat_h, save image.
 Then, use render_doc_text(path_image)

 render_doc_text create client google vision , and use it to detect text, it will create a file "data.txt" with all the detected text by google vision
