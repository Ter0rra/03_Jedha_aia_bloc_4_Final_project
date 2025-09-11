from datetime import datetime
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python import PythonOperator
import torchvision.transforms.v2 as transforms
import pandas as pd
import os
from PIL import Image

import cnn_lab


default_args = {
    'owner': 'airflow',
    'start_date': datetime(2024, 1, 1),
    'retries': 1
}

transform = transforms.Compose([
        transforms.Resize(256),
        transforms.CenterCrop(224)])


def traiter_images(dossier_a, dossier_b, transforme):
    """
    Applique une transformation sur toutes les images d'un dossier et les enregistre dans un autre dossier.

    :param dossier_a: Chemin du dossier source contenant les images
    :param dossier_b: Chemin du dossier destination où stocker les images transformées
    :param transforme: Fonction qui prend en entrée une image PIL et retourne une image transformée
    """

    # Extensions d'images communes
    extensions_valides = (".jpg", ".jpeg", ".png", ".bmp", ".tiff", ".gif")

    for nom_fichier in os.listdir(dossier_a):
        if nom_fichier.lower().endswith(extensions_valides):
            chemin_entree = os.path.join(dossier_a, nom_fichier)
            chemin_sortie = os.path.join(dossier_b, nom_fichier)

            try:
                # Ouvrir l'image
                with Image.open(chemin_entree) as img:
                    # Appliquer la transformation
                    img_trans = transforme(img)

                    # Sauvegarder l'image transformée
                    img_trans.save(chemin_sortie)
            except Exception as e:
                print(f"⚠ Erreur avec {nom_fichier}: {e}")
    

def label(proces_img):
    lab = pd.DataFrame(["img_name", "emo1", "emo2", "emo3", "emo4"])
    # => ligne de commande pour recupération du nom de proces_img
    emotion = cnn_lab.get_emotion(proces_img)
    # => ligne de commande pour implanter les labels dans le csv 
    lab.to_csv('../data/labeled_data/labels.csv')


with DAG(dag_id="Weekly_transformation", default_args=default_args, catchup=False) as dag:

    start_dag = BashOperator(task_id="start_dag", bash_command="echo 'Start!'")

    move_to_folder = BashOperator(task_id="move_to_folder", bash_command='''
                                cd ../../opt/airflow/
                                ''')
    
    weekly_transform = PythonOperator(task_id="weekly_transform", python_callable=traiter_images("data/raw_images", "data/processed", transform))
                            
    end_dag = BashOperator(task_id="end_dag", bash_command="echo 'End!'")

    start_dag >>  move_to_folder >> weekly_transform >> end_dag