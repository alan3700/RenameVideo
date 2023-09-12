import subprocess
import json
import os
import re
import tkinter as tk
from tkinter import filedialog

def get_cleaned_video_title(filename):
    nom_film, extension = os.path.splitext(filename)
    nom_film = re.sub(r'[^a-zA-Z0-9\s]', '', nom_film)
    return f"{nom_film}"

def get_video_title_from_metadata(metadata):
    # Vérifier si les métadonnées contiennent un titre
    if 'title' in metadata:
        return metadata['title']
    return None

def get_video_metadata(file_path):
    # Utiliser ffprobe pour obtenir les métadonnées de la vidéo
    cmd = ["ffprobe", "-v", "quiet", "-print_format", "json", "-show_format", "-show_streams", file_path]
    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    if result.returncode == 0:
        # Analyser la sortie JSON
        metadata = json.loads(result.stdout)
        return metadata
    else:
        print(f"Erreur lors de la lecture des métadonnées de {file_path}.")
        return None

def rename_videos_in_folder(folder_path):
    # Parcourir tous les fichiers dans le dossier
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)

        # Vérifier si le fichier est une vidéo en examinant son extension (vous pouvez ajouter plus d'extensions si nécessaire)
        if filename.lower().endswith(('.mp4', '.avi', '.mkv', '.mov')):
            # Obtenir les métadonnées de la vidéo
            metadata = get_video_metadata(file_path)

            if metadata:
                # Extraire le titre du fichier à partir des métadonnées s'il est disponible
                title = get_video_title_from_metadata(metadata)

                if title:
                    # Construire le nouveau nom de fichier avec le titre des métadonnées
                    file_dir, file_ext = os.path.splitext(file_path)
                else:
                    # Extraire le titre du nom de fichier en nettoyant
                    cleaned_title = get_cleaned_video_title(filename)
                    # Construire le nouveau nom de fichier avec le titre nettoyé
                    file_dir, file_ext = os.path.splitext(file_path)

                new_file_name = f"{cleaned_title}{file_ext}"
                new_file_path = os.path.join(folder_path, new_file_name)

                # Renommer le fichier
                try:
                    os.rename(file_path, new_file_path)
                    print(f"Le fichier {filename} a été renommé en : {new_file_name}")
                except Exception as e:
                    print(f"Erreur lors du renommage du fichier {filename} : {e}")

def select_folder():
    root = tk.Tk()
    root.withdraw()  # Cacher la fenêtre principale de tkinter
    folder_path = filedialog.askdirectory(title="Sélectionnez le dossier contenant les vidéos")
    if folder_path:
        rename_videos_in_folder(folder_path)
    else:
        print("Aucun dossier sélectionné.")

if __name__ == "__main__":
    select_folder()