import re
import os

def extraire_nom_film(nom_fichier):
    # Utilisation d'une expression régulière pour extraire le nom du film
    # On suppose que le nom du film est composé de caractères alphabétiques, des espaces et des chiffres.
    # Les autres caractères sont supprimés.
    nom_film, extension = os.path.splitext(nom_fichier)
    nom_film = re.sub(r'[^a-zA-Z0-9\s]', '', nom_film)
    return f"{nom_film}"  # Conservez l'extension
# Exemple d'utilisation :
nom_fichier = "Avatar.2.La.Voie.de.l'eau.2023.$$$.$@2@@.avi"
nom_du_film = extraire_nom_film(nom_fichier)
print(nom_du_film)